# for VGG: reshape every image to size(224, 224, 3)

import os, sys
from os import walk
import skimage.io
import skimage.transform
import numpy as np
import matplotlib.pyplot as plt
from generate_label import get_id_path_dict
from generate_label import dict2array
from lxml import etree


def calc_dataset_mean(dataset, sample_num=100):
    print('calc_dataset_mean(dataset=%s)' % dataset)
    if dataset == 0:
        folder = 'data/PedestrianRetrieval_vali/vq_path'
    elif dataset == 1:
        folder = 'data/PedestrianRetrieval_vali/vr_path'
    elif dataset == 2:
        folder = 'data/new_online_vali_set_UPLOAD_VERSION/vq_path'
    elif dataset == 3:
        folder = 'data/new_online_vali_set_UPLOAD_VERSION/vr_path'
    else:
        print('no this data set')
        return

    rgb = []
    shape = []
    for dirpath, dirnames, filenames in walk(folder):
        print('image num: %s' % len(filenames))
        for filename in filenames[0:len(filenames):int(len(filenames) / sample_num)]:
            image_path = os.path.join(os.path.abspath(folder), filename)
            each_rgb = skimage.io.imread(image_path)
            rgb.append(np.mean(np.mean(each_rgb, 0), 0))
            shape.append(each_rgb.shape[:2])
    print('sample image num: %s' % len(rgb))
    rgb_np = np.array(rgb)
    shape_np = np.array(shape)
    print('mean rgb: ' + str(np.mean(rgb_np, 0)))
    plt.hist(rgb_np, bins=20)
    plt.show()
    print('mean shape: ' + str(np.mean(shape_np, 0)))
    plt.hist(shape_np, bins=20)
    plt.show()


def train_image_count():
    id_paths = get_id_path_dict()
    image_nums = []
    for id in id_paths:
        image_nums.append(len(id_paths[id]))
    image_nums_np = np.array(image_nums)
    plt.hist(image_nums_np, bins=30)
    plt.show()


def show_train_image(id_array, max_num):
    id_paths = get_id_path_dict()
    id_paths_array = dict2array(id_paths)
    for id_path_array in id_paths_array[id_array[0]:min(id_array[1], len(id_paths_array)):id_array[2]]:
        image_num = len(id_path_array) - 1
        print('id: %s, image number: %s' % (id_path_array[0], image_num))
        for image_path in id_path_array[1:min(max_num + 1, image_num + 1)]:
            print(image_path)
            image = skimage.io.imread(image_path)
            image = skimage.transform.resize(image, (224, 112))
            skimage.io.imshow(image)
            skimage.io.show()


def show_target_train_image(id):
    id = str(id)
    id_paths = get_id_path_dict()
    print('image number: %s' % len(id_paths[id]))
    for image_path in id_paths[id]:
        print(image_path)
        skimage.io.imshow(skimage.io.imread(image_path))
        skimage.io.show()


def xml_dict(path):
    data = etree.parse(os.path.abspath(path))
    # data = etree.parse(os.path.abspath('data/new_online_vali_set_UPLOAD_VERSION/example_result.xml'))

    root = data.getroot()
    predict_dict = {}

    for items in root:
        for item in items:
            probe_name = item.attrib['imageName']
            gallerys = []
            for order in range(200):
                gallerys.append(item.text[7 * order:7 * order + 6])
            predict_dict[probe_name] = gallerys
    return predict_dict


def show_predict_prob_gallery_result(path, top_n):
    predict_dict = xml_dict(path)
    for probe, gallerys in predict_dict.iteritems():
        print('probe: % s' % probe)
        probe_path = os.path.join(os.path.abspath('data/new_online_vali_set_UPLOAD_VERSION/vq_path'), probe + '.jpg')
        skimage.io.imshow(skimage.io.imread(probe_path))
        skimage.io.show()
        for gallery in gallerys[:top_n]:
            print('gallery: % s' % gallery)
            gallery_path = os.path.join(os.path.abspath('data/new_online_vali_set_UPLOAD_VERSION/vr_path'),
                                      gallery + '.jpg')
            skimage.io.imshow(skimage.io.imread(gallery_path))
            skimage.io.show()


def show_target_predict_prob_gallery_result(path, probe_image):
    probe_image = str(probe_image)
    print('probe: % s' % probe_image)
    probe_path = os.path.join(os.path.abspath('data/new_online_vali_set_UPLOAD_VERSION/vq_path'), probe_image + '.jpg')
    skimage.io.imshow(skimage.io.imread(probe_path))
    skimage.io.show()
    predict_dict = xml_dict(path)
    for gallery in predict_dict[probe_image]:
        print('gallery: % s' % gallery)
        gallery_path = os.path.join(os.path.abspath('data/new_online_vali_set_UPLOAD_VERSION/vr_path'),
                                  gallery + '.jpg')
        skimage.io.imshow(skimage.io.imread(gallery_path))
        skimage.io.show()


def show_target_gallery_result(gallery_image):
    gallery_image = str(gallery_image)
    print('gallery: % s' % gallery_image)
    gallery_path = os.path.join(os.path.abspath('data/new_online_vali_set_UPLOAD_VERSION/vr_path'), gallery_image + '.jpg')
    skimage.io.imshow(skimage.io.imread(gallery_path))
    skimage.io.show()


if __name__ == '__main__':
    # calc_dataset_mean(dataset=0, sample_num=2000)
    # calc_dataset_mean(dataset=1, sample_num=2000)
    # calc_dataset_mean(dataset=2, sample_num=2000)
    # calc_dataset_mean(dataset=3, sample_num=2000)
    # 0: train vq probe
    # 1: train vr gallery
    # 2: predict vq probe
    # 3: predict vr gallery

    # train_image_count()
    # show_train_image(id_array=[1,1000,11],max_num=10)
    # show_target_train_image('137452')

    # show_predict_prob_gallery_result('data/predict_result.xml', top_n=5)
    # show_target_predict_prob_gallery_result('data/predict_result.xml', '313223')
    show_target_gallery_result('037921')

    # show_predict_prob_gallery_result('data/predict_result2.xml', top_n=5)
    # show_target_predict_prob_gallery_result('data/predict_result2.xml', '323305')