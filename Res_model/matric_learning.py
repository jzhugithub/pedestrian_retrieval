import sys
import os.path as osp
from argparse import ArgumentParser

import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import pairwise_distances

root = osp.join(osp.dirname(osp.abspath(__file__)), '..')
if root not in sys.path:
    sys.path.insert(0, root)
from res_cmc import cmc
from res_cmc import mean_ap

def _get_train_data():
    # Merge training and validation features and labels
    features = np.r_[np.load('result/test_features/train_200_gallery_features.npy'),
                     np.load('result/test_features/train_200_probe_features.npy')]
    labels = np.r_[np.load('result/test_features/train_200_gallery_labels.npy'),
                   np.load('result/test_features/train_200_probe_labels.npy')]
    # Reassign the labels to make them sequentially numbered from zero
    unique_labels = np.unique(labels)
    labels_map = {l: i for i, l in enumerate(unique_labels)}
    labels = np.asarray([labels_map[l] for l in labels])
    return features, labels


def _get_test_data():
    PX = np.load('result/test_features/valid_probe_features_step-30000.npy')
    PY = np.load('result/test_features/valid_probe_labels.npy')
    GX = np.load('result/test_features/valid_gallery_features_step-30000.npy')
    GY = np.load('result/test_features/valid_gallery_labels.npy')
    # Reassign the labels to make them sequentially numbered from zero
    unique_labels = np.unique(np.r_[PY, GY])
    labels_map = {l: i for i, l in enumerate(unique_labels)}
    PY = np.asarray([labels_map[l] for l in PY])
    GY = np.asarray([labels_map[l] for l in GY])
    return PX, PY, GX, GY


def _learn_pca(X, dim):
    pca = PCA(n_components=dim)
    pca.fit(X)
    return pca


def _learn_metric(X, Y, method):
    if method == 'euclidean':
        M = np.eye(X.shape[1])
    elif method == 'kissme':
        num = len(Y)
        X1, X2 = np.meshgrid(np.arange(0, num), np.arange(0, num))
        X1, X2 = X1[X1 < X2], X2[X1 < X2]
        matches = (Y[X1] == Y[X2])
        num_matches = matches.sum()
        num_non_matches = len(matches) - num_matches
        idxa = X1[matches]
        idxb = X2[matches]
        S = X[idxa] - X[idxb]
        C1 = S.transpose().dot(S) / num_matches
        p = np.random.choice(num_non_matches, num_matches, replace=False)
        idxa = X1[matches == False]
        idxb = X2[matches == False]
        idxa = idxa[p]
        idxb = idxb[p]
        S = X[idxa] - X[idxb]
        C0 = S.transpose().dot(S) / num_matches
        M = np.linalg.inv(C1) - np.linalg.inv(C0)
    return M


def _eval_cmc(PX, PY, GX, GY, M):
    D = pairwise_distances(GX, PX, metric='mahalanobis', VI=M, n_jobs=-2)
    C = cmc(D, GY, PY)
    print(mean_ap(D, GY, PY))
    return C

if __name__ == '__main__':
    method = 'kissme' # 'euclidean', 'kissme'

    X, Y = _get_train_data()
    PX, PY, GX, GY = _get_test_data()

    file_suffix = method
    # if args.pca is not None:
    #     S = _learn_pca(X, args.pca)
    #     X = S.transform(X)
    #     PX = S.transform(PX)
    #     GX = S.transform(GX)
    #     file_suffix += '_pca_{}'.format(args.pca)
    #     np.save(osp.join(args.result_dir, 'pca_' + file_suffix), S)

    M = _learn_metric(X, Y, method)
    C = _eval_cmc(PX, PY, GX, GY, M)
    np.save('metric_' + file_suffix, M)
    np.save('cmc_' + file_suffix, C)

    for topk in [1, 5, 10, 20]:
        print("{:8}{:8.1%}".format('top-' + str(topk), C[topk - 1]))
