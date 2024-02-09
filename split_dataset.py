import json
import os
import secrets

def split(annotations, *param, random_shuffle=True):
    """Splits a dictionary of annotations into train, validation, and test sets.
    Parameters:
        - annotations (dict): A dictionary of annotations.
        - *param (dict): Optional parameters for specifying train and validation filenames.
        - random_shuffle (bool): Whether to randomly shuffle the annotations before splitting. Default is True.
    Returns:
        - train_ann (dict): A dictionary of annotations for the train set.
        - val_ann (dict): A dictionary of annotations for the validation set.
        - test_ann (dict): A dictionary of annotations for the test set.
    Processing Logic:
        - Randomly shuffles the annotations if random_shuffle is True.
        - Splits the annotations into train, validation, and test sets.
        - If random_shuffle is False, uses the filenames specified in param to split the annotations.
        - Returns three dictionaries containing the annotations for each set.
    Example:
        train_ann, val_ann, test_ann = split(annotations, random_shuffle=False, param={"train": ["image1.jpg", "image2.jpg"], "val": ["image3.jpg", "image4.jpg"]})
        # Returns train, validation, and test sets with annotations for the specified filenames."""
    
    train_ann = {}
    val_ann = {}
    test_ann = {}

    if random_shuffle == True:
        index = list(range(len(annotations)))
        secrets.SystemRandom().shuffle(index)
        num_train = round(len(annotations)*0.6)
        num_val = round(len(annotations)*0.2)
        train_index = index[:num_train]
        val_index = index[num_train:num_train+num_val]
        test_index = index[num_train+num_val:]
        for each in train_index:
            key = list(annotations.keys())[each]
            train_ann[key] = annotations[key]
        for each in val_index:
            key = list(annotations.keys())[each]
            val_ann[key] = annotations[key]
        for each in test_index:
            key = list(annotations.keys())[each]
            test_ann[key] = annotations[key]
        return train_ann, val_ann, test_ann
    else:
        keys = list(annotations.keys())
        train_names = param[0]["train"]
        val_names = param[0]["val"]

        for key in keys:
            filename = annotations[key]["filename"]
            if filename in train_names:
                train_ann[key] = annotations[key]
            elif filename in val_names:
                val_ann[key] = annotations[key]
            else:
                test_ann[key] = annotations[key]
        return train_ann, val_ann, test_ann

if __name__ == "__main__":
    dataset_dir = "/home/simon/deeplearning/git_surgery/data/surgery/train"
    annotations = json.load(open(os.path.join(dataset_dir, "via_region_data.json")))
    # if you want to specify train, val, test set with a dict, else just leave split_map as a empty dic
    split_map = {"train":["Picture 390.jpg"], "val":["Picture 392.jpg"], "test":[]}
    if len(split_map) == 0:
        train_ann, val_ann, test_ann = split(annotations)
    else:
        train_ann, val_ann, test_ann = split(annotations, split_map, random_shuffle=False)
