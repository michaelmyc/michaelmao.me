from .base_dataset import BaseDataset


class VisualGenomeCaptionDataset(BaseDataset):
    def __init__(self, *args, split="", **kwargs):
        assert split in ["train", "val", "test"]
        if split == "test":
            split = "val"
            
        use_train_as_val = kwargs.pop("use_train_as_val", False);

        if split == "train":
            names = ["vg"]
        elif split == "val" and use_train_as_val:
            names = ["vg"]
        elif split == "val":
            names = []

        super().__init__(*args, **kwargs, names=names, text_column_name="caption")

    def __getitem__(self, index):
        return self.get_suite(index)
