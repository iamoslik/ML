import numpy as np
from collections import defaultdict

def kfold_split(num_objects, num_folds):
    """Split [0, 1, ..., num_objects - 1] into equal num_folds folds (last fold can be longer) and returns num_folds train-val 
       pairs of indexes.

    Parameters:
    num_objects (int): number of objects in train set
    num_folds (int): number of folds for cross-validation split

    Returns:
    list((tuple(np.array, np.array))): list of length num_folds, where i-th element of list contains tuple of 2 numpy arrays,
                                       the 1st numpy array contains all indexes without i-th fold while the 2nd one contains
                                       i-th fold
    """
    ans = []
    f_size = num_objects // num_folds
    for i in range(0, num_folds - 1):
        train_sample = np.arange(0, i * f_size)
        test_sample = np.arange((i + 1) * f_size, num_objects)
        val = np.arange(i * f_size, min((i + 1) * f_size, num_objects))
        ans.append((np.concatenate((train_sample, test_sample)), val))

    i = num_folds - 1
    train_sample = np.arange(0, i * f_size)
    val = np.arange(i * f_size, num_objects)
    ans.append((train_sample, val))
    print(ans)
    return ans

def knn_cv_score(X, y, parameters, score_function, folds, knn_class):
    """Takes train data, counts cross-validation score over grid of parameters (all possible parameters combinations) 

    Parameters:
    X (2d np.array): train set
    y (1d np.array): train labels
    parameters (dict): dict with keys from {n_neighbors, metrics, weights, normalizers}, values of type list,
                       parameters['normalizers'] contains tuples (normalizer, normalizer_name), see parameters
                       example in your jupyter notebook
    score_function (callable): function with input (y_true, y_predict) which outputs score metric
    folds (list): output of kfold_split
    knn_class (obj): class of knn model to fit

    Returns:
    dict: key - tuple of (normalizer_name, n_neighbors, metric, weight), value - mean score over all folds
    """
    dict = {}
    for neighbors in parameters['n_neighbors']:
        for metric in parameters['metrics']:
            for weight in parameters['weights']:
                for norm in parameters['normalizers']:
                    total = 0
                    for a, b in folds:
                        train = X[a]
                        test = X[b]
                        if norm[0] is not None:
                            w = norm[0]
                            w.fit(X[a])
                            train = w.transform(train)
                            test = w.transform(test)
                        model = knn_class(neighbors, metric=metric, weights=weight)
                        model.fit(train, y[a])
                        ans = model.predict(test)
                        total += score_function(y[b], ans)
                        tot = total / len(folds)
                    dict[tuple([norm[1], neighbors, metric, weight])] = tot
    return dict