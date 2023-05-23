import json
import numpy as np
import pandas as pd
import pyarrow as pa
import random
import os

from tqdm import tqdm
from glob import glob
from collections import defaultdict, Counter
from .glossary import normalize_word


def get_score(occurences):
    if occurences == 0:
        return 0.0
    elif occurences == 1:
        return 0.3
    elif occurences == 2:
        return 0.6
    elif occurences == 3:
        return 0.9
    else:
        return 1.0


def path2rest(path, split, annotations):
    iid = int(path.split("/")[-1].split("_")[-1][:-4])

    with open(path, "rb") as fp:
        binary = fp.read()

    _annot = annotations[split][iid]
    _annot = list(_annot.items())
    qids, qas = [a[0] for a in _annot], [a[1] for a in _annot]
    questions = [qa[0] for qa in qas]
    answers = [qa[1] for qa in qas] if "test" not in split else list(list())
    answer_labels = (
        [a["labels"] for a in answers] if "test" not in split else list(list())
    )
    answer_scores = (
        [a["scores"] for a in answers] if "test" not in split else list(list())
    )
    answer_type = (
        [a["answer_type"] for a in answers]
    )
    answers = (
        [[] for al in answer_labels]
        if "test" not in split
        else list(list())
    )
    is_adversarial = split in ["adversarial-train", "adversarial-val"]

    return [binary, questions, answers, answer_labels, answer_scores, iid, qids, answer_type, is_adversarial, split]


def make_arrow(root, dataset_root):
    # with open(f"{root}/vqa/v2_OpenEnded_mscoco_train2014_questions.json", "r") as fp:
    #     questions_train2014 = json.load(fp)["questions"]
    # with open(f"{root}/vqa/v2_OpenEnded_mscoco_val2014_questions.json", "r") as fp:
    #     questions_val2014 = json.load(fp)["questions"]
    # with open(f"{root}/vqa/v2_OpenEnded_mscoco_test2015_questions.json", "r") as fp:
    #     questions_test2015 = json.load(fp)["questions"]
    # with open(f"{root}/vqa/v2_OpenEnded_mscoco_test-dev2015_questions.json", "r") as fp:
    #     questions_test_dev2015 = json.load(fp)["questions"]

    # with open(f"{root}/vqa/v2_mscoco_train2014_annotations.json", "r") as fp:
    #     annotations_train2014 = json.load(fp)["annotations"]
    # with open(f"{root}/vqa/v2_mscoco_val2014_annotations.json", "r") as fp:
    #     annotations_val2014 = json.load(fp)["annotations"]

    with open(f"{root}/adversarial_vqa_v1_train.json", "r") as fp:
        adversarial_train = json.load(fp)
    with open(f"{root}/adversarial_vqa_v1_val.json", "r") as fp:
        adversarial_val = json.load(fp)

    annotations = dict()

    for split, questions in zip(
        ["adversarial-train", "adversarial-val"],
        [
            adversarial_train,
            adversarial_val,
        ],
    ):
        _annot = defaultdict(dict)
        for q in tqdm(questions):
            _annot[q["image_id"]][q["question_id"]] = [q["question"]]

        annotations[split] = _annot

    for split, annots in zip(
        ["adversarial-train", "adversarial-val"], [adversarial_train, adversarial_val],
    ):
        _annot = annotations[split]
        for q in tqdm(annots):
            answers = q["answers"]
            answer_count = {}
            for answer in answers:
                answer_count[answer] = answer_count.get(answer, 0) + 1

            labels = []
            scores = []
            
            answer_type = q['answer_type'][0]
            for t in q['answer_type']:
                if t != answer_type:
                    answer_type = np.minimum(np.array(answer_type) + np.array(t), 1).tolist()

            _annot[q["image_id"]][q["question_id"]].append(
                {"labels": labels, "scores": scores, "answer_type": answer_type, "is_adversarial": True}
            )

    for split in [
        "adversarial-train",
        "adversarial-val",
    ]:
        annot = annotations[split]
        split_name = {
            "adversarial-train": "val2014",
            "adversarial-val": "val2014",
        }[split]
        paths = list(glob(f"{root}/vqa/{split_name}/*.jpg"))
        random.shuffle(paths)
        annot_paths = [
            path
            for path in paths
            if int(path.split("/")[-1].split("_")[-1][:-4]) in annot
        ]

        if len(paths) == len(annot_paths):
            print("all images have caption annotations")
        else:
            print("not all images have caption annotations")
        print(
            len(paths), len(annot_paths), len(annot),
        )

        bs = [
            path2rest(path, split, annotations) for path in tqdm(annot_paths)
        ]

        dataframe = pd.DataFrame(
            bs,
            columns=[
                "image",
                "questions",
                "answers",
                "answer_labels",
                "answer_scores",
                "image_id",
                "question_id",
                "answer_type",
                "is_adversarial",
                "split",
            ],
        )

        table = pa.Table.from_pandas(dataframe)

        os.makedirs(dataset_root, exist_ok=True)
        with pa.OSFile(f"{dataset_root}/vqav2_{split}_adv_only.arrow", "wb") as sink:
            with pa.RecordBatchFileWriter(sink, table.schema) as writer:
                writer.write_table(table)
