# Email of the author: zjduan@pku.edu.cn
import numpy as np
import config
import os
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn import preprocessing

scale = ""
train_x_name = "train_x.npy"
train_y_name = "train_y.npy"

# numr_feat = []
Column = 13


def _load_data(_nrows=None, debug=False):

    train_x = pd.read_csv(
        config.TRAIN_X, header=None, sep=" ", nrows=_nrows, dtype=np.float
    )
    train_y = pd.read_csv(
        config.TRAIN_Y, header=None, sep=" ", nrows=_nrows, dtype=np.int32
    )

    # for i in range(11):
    #     print ("argmax feat %d = %d, max = %d" % (i, train_x[i].argmax(), train_x[i].max()))

    train_x = train_x.values
    train_y = train_y.values.reshape([-1])

    # print ("begin to scale")
    # if (scale == "minmax"):
    #     train_x = preprocessing.MinMaxScaler().fit_transform(train_x)

    # if (scale == "std"):
    #     train_x[:,0:12] = preprocessing.scale(train_x[:,0:12])
    #     train_x[:,0:12] += 1

    print("data loading done!")
    print("training data : %d" % train_y.shape[0])

    assert train_x.shape[0] == train_y.shape[0]

    return train_x, train_y


def save_x_y(fold_index, train_x, train_y):
    def _get(x, l): return [x[i] for i in l]
    for i in range(len(fold_index)):
        print("now part %d" % (i + 1))
        part_index = fold_index[i]
        Xv_train_, y_train_ = _get(
            train_x, part_index), _get(train_y, part_index)
        save_dir_Xv = config.DATA_PATH + "part" + str(i + 1) + "/"
        save_dir_y = config.DATA_PATH + "part" + str(i + 1) + "/"
        if os.path.exists(save_dir_Xv) == False:
            os.makedirs(save_dir_Xv)
        if os.path.exists(save_dir_y) == False:
            os.makedirs(save_dir_y)
        save_path_Xv = save_dir_Xv + train_x_name
        save_path_y = save_dir_y + train_y_name
        np.save(save_path_Xv, Xv_train_)
        np.save(save_path_y, y_train_)


# def save_test(test_x, test_y):
#     np.save("../data/test/test_x.npy", test_x)
#     np.save("../data/test/test_y.npy", test_y)


def save_i(fold_index):
    def _get(x, l): return [x[i] for i in l]
    train_i = pd.read_csv(
        config.TRAIN_I, header=None, sep=" ", nrows=None, dtype=np.int32
    )
    train_i = train_i.values
    feature_size = train_i.max() + 1
    print("feature_size = %d" % feature_size)
    feature_size = [feature_size]
    feature_size = np.array(feature_size)
    np.save(config.DATA_PATH + "feature_size.npy", feature_size)

    # pivot = 40000000

    # test_i = train_i[pivot:]
    # train_i = train_i[:pivot]

    # print("test_i size: %d" % len(test_i))
    print("train_i size: %d" % len(train_i))

    # np.save("../data/test/test_i.npy", test_i)

    for i in range(len(fold_index)):
        print("now part %d" % (i + 1))
        part_index = fold_index[i]
        Xi_train_ = _get(train_i, part_index)
        save_path_Xi = config.DATA_PATH + "part" + str(i + 1) + "/train_i.npy"
        np.save(save_path_Xi, Xi_train_)


def main():

    train_x, train_y = _load_data()
    print("loading data done!")

    folds = list(
        StratifiedKFold(
            n_splits=10, shuffle=True, random_state=config.RANDOM_SEED
        ).split(train_x, train_y)
    )

    fold_index = []
    for i, (train_id, valid_id) in enumerate(folds):
        fold_index.append(valid_id)

    print("fold num: %d" % (len(fold_index)))

    fold_index = np.array(fold_index)
    np.save(config.DATA_PATH + "fold_index.npy", fold_index)

    save_x_y(fold_index, train_x, train_y)
    print("save train_x_y done!")

    fold_index = np.load(config.DATA_PATH +
                         "fold_index.npy", allow_pickle=True)
    save_i(fold_index)
    print("save index done!")


if __name__ == "__main__":
    main()
