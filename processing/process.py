# -*- coding: utf-8 -*-
"""
This file combines data preprocessing with PCA to visualize what we
scraped into 2 or 3 dimensions to make visualization

Created by Kunhong Yu(444447)
Date: 2022/04/27
"""
from processing.pca import SimplePCA
from processing.data_pre import preprocess
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

def procedure(mode = 'soup', for_author = False):
    """This function is used to do processing procedure
    Args :
        --mode: default is 'soup', 'soup'/'sscrapy'/'sselenium'
        --for_author: default is False, if True, then we need to visualize using
            'allauthorsinfo.csv'
    """
    # 1. Build PCA instances(2 or 3 dimensional)
    pca2 = SimplePCA(n_components = 2)
    pca3 = SimplePCA(n_components = 3)

    # 2. Preprocess data
    if mode == 'soup':
        path = './soup/data/'
    elif mode == 'sscrapy':
        path = './sscrapy/data/'
    else:
        path = './sselenium/data/'

    try:
        if for_author:
            data_path = path + 'allauthorsinfo.csv'
        else:
            data_path = path + 'allinfo.csv'
        data = pd.read_csv(data_path, sep = '#')
        flag = True
    except:
        # only used when used for Scrapy when scraping using command line
        path = '../../data/'
        if for_author:
            data_path = path + 'allauthorsinfo.csv'
        else:
            data_path = path + 'allinfo.csv'
        data = pd.read_csv(data_path, sep = '#')
        flag = False

    print('Processing...')
    if flag:
        X = preprocess(data)
    else:
        X = preprocess(data, path = '../../../processing/glove.6B.50d.txt')

    # 3. now run PCA
    print('Visualizing with running PCA...')
    X_trans2, _ = pca2.interpret(x = X, FUNC = 'forward', param = None)
    X_trans3, _ = pca3.interpret(x = X, FUNC = 'forward', param = None)

    # 4. now make visualization
    visualize(data, X_trans2, X_trans3, path, for_author)


def visualize(data, X_trans2, X_trans3, path, for_author):
    """This function is used to make visualization
    Args :
        --data: pandas DataFrame to make visualization
        --X_trans2/X_trans3: 2d/3d PCA transformed data
        --path: data path
        --for_author
    """
    labels = []
    colors = []
    if not for_author:
        for _, line in data.iterrows():
            labels.append(line['title'][:5]) # only append front 10 characters to make visualization easier
            colors.append(line['subsubsubject']) # to make visualization using this color
    else:
        for _, line in data.iterrows():
            labels.append(line['title'][:5]) # only append front 10 characters to make visualization easier
            colors.append(line['name']) # to make visualization using this color

    # 1. visualize 2d
    plot_embeddings(embeddings = X_trans2, labels = labels,
                    ori_colors = colors,
                    for_author = for_author,
                    colors = colors, mode = '2d')
    try:
        if for_author:
            plt.savefig(path + '2dallauthorsinfoPCA.png')
        else:
            plt.savefig(path + '2dallinfoPCA.png')
    except:
        # only used when used for Scrapy when scraping using command line
        path = '../../data/'
        if for_author:
            plt.savefig(path + '2dallauthorsinfoPCA.png')
        else:
            plt.savefig(path + '2dallinfoPCA.png')
    plt.close()

    # 2. 3d
    plot_embeddings(embeddings = X_trans3, labels = labels,
                    ori_colors = colors, for_author = for_author,
                    colors = colors, mode = '3d')
    try:
        if for_author:
            plt.savefig(path + '3dallauthorsinfoPCA.png')
        else:
            plt.savefig(path + '3dallinfoPCA.png')
    except:
        # only used when used for Scrapy when scraping using command line
        path = '../../data/'
        if for_author:
            plt.savefig(path + '3dallauthorsinfoPCA.png')
        else:
            plt.savefig(path + '3dallinfoPCA.png')
    plt.close()


def plot_embeddings(embeddings,
                    labels,
                    colors,
                    ori_colors,
                    for_author,
                    mode = '2d'):
    """This function is used to plot embeddings
    Args :
        --embeddings: all PCA embeddings in numpy array
        --labels: labels 'sssubject'
        --colors
        --ori_colors
        --mode: default is '2d', '2d'/'3d'
    """
    assert mode in ['2d', '3d']
    ori_labels = labels

    # normalize first
    embeddings = MinMaxScaler().fit_transform(embeddings)

    _, colors = np.unique(colors, return_inverse = True)
    _, labels = np.unique(labels, return_inverse = True)

    fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (24, 24))

    if mode == '3d': # 3d
        ax = fig.add_subplot(1, 1, 1, projection = '3d')
        for color in set(ori_colors):
            indices = np.where(np.array(ori_colors) == color)[0].tolist()
            ax.scatter(embeddings[indices, 0], embeddings[indices, 1], embeddings[indices, 2],
                       label = color)  # add scatter to add legend
            for i in indices:
                ax.text(embeddings[i, 0], embeddings[i, 1], embeddings[i, 2],
                        str(ori_labels[i]), color = plt.cm.Set1(colors[i] / 10),
                        fontdict = {'weight': 'bold', 'size': 15})

        plt.legend(title = 'subject' if not for_author else 'name',
                   loc = 'best', prop = {'size': 20})

    else: # 2d
        sns.scatterplot(x = embeddings[:, 0], y = embeddings[:, 1],
                        hue = ori_colors, ax = ax, s = 180)

        for ori_label, x1, x2 in zip(ori_labels, embeddings[:, 0], embeddings[:, 1]):
            ax.annotate(ori_label,
                        (x1, x2),
                        horizontalalignment = 'center',
                        verticalalignment = 'center',
                        size = 20)
        plt.legend(loc = 'best', title = 'subject' if not for_author else 'name',
                   prop = {'size': 20})

        # plt.show()


# unit test
if __name__ == '__main__':
    procedure(mode = 'soup', for_author = True)