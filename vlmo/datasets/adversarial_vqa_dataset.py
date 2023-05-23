from .base_dataset import BaseDataset


class AdversarialVQADataset(BaseDataset):
    def __init__(self, *args, split="", **kwargs):
        assert split in ["train", "val", "test"]
        self.split = split

        if split == "train":
            names = ["vqav2_train_adv", "vqav2_trainable_val_adv", "vqav2_adversarial-train_adv"]
        elif split == "val":
            names = ["vqav2_rest_val_adv", "vqav2_adversarial-val_adv"]
        elif split == "test":
            # names = ["vqav2_test_adv"]  # vqav2_test-dev for test-dev
            names = ["vqav2_rest_val_adv"]
            # names = ["vqav2_adversarial-val_adv"]
            # names = ["vqav2_rest_val_adv", "vqav2_adversarial-val_adv"]
            
        use_train_as_val = kwargs.pop("use_train_as_val", False);

        super().__init__(
            *args,
            **kwargs,
            names=names,
            text_column_name="questions",
            remove_duplicate=False,
        )

    def __getitem__(self, index):
        image_tensor = self.get_image(index)["image"]
        text = self.get_text(index)["text"]

        index, question_index = self.index_mapper[index]
        qid = self.table["question_id"][index][question_index].as_py()
        iid = self.table["image_id"][index].as_py()

        if self.split != "test":
            answers = self.table["answers"][index][question_index].as_py()
            labels = self.table["answer_labels"][index][question_index].as_py()
            scores = self.table["answer_scores"][index][question_index].as_py()
            answer_type_labels = self.table["answer_type"][index][question_index].as_py()
        else:
            # answers = list()
            # labels = list()
            # scores = list()
            # answer_type_labels = list()
            answers = self.table["answers"][index][question_index].as_py()
            labels = self.table["answer_labels"][index][question_index].as_py()
            scores = self.table["answer_scores"][index][question_index].as_py()
            answer_type_labels = self.table["answer_type"][index][question_index].as_py()

        return {
            "image": image_tensor,
            "text": text,
            "vqa_answer": answers,
            "vqa_labels": labels,
            "vqa_scores": scores,
            "answer_type_labels": answer_type_labels,
            "qid": qid,
            "iid": iid,
        }
