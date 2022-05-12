# -*- coding: utf-8 -*-
"""
This file contains operations about using pca to do dimension reduction to make visualizations

Created by Kunhong Yu(444447)
Date: 2022//04/27
"""
from sklearn.decomposition import PCA

class SimplePCA(object):
    """Define simple PCA model from sklearn's API"""
    def __init__(self, n_components = 2):

        self.model = PCA(n_components = n_components,
                         # below are defaults
                         copy = True,
                         whiten = False,
                         svd_solver = 'auto',
                         tol = 0.0,
                         iterated_power = 'auto',
                         random_state = None)

    def __forward(self, x):
        """Fit transform
        Args :
            --x: input
        return :
            --fit_transform results
        """
        x = self.model.fit_transform(x)

        return x

    def __get_params(self, param):
        """Get parameters
        Args :
            --param: 'components_'/'variance_ratio_'
        return:
            --corresponding parameter
        """
        res = {'components_' : self.model.components_,
               'variance_ratio_': sum(self.model.explained_variance_ratio_.tolist())}

        return res[param]

    def interpret(self, x = None, FUNC = 'forward', param = None):
        """All models operations
        Args :
            --x: input
            --FUNC: 'forward'/'get_param'
            --param: 'components_'/'variance_ratio_'
        return :
            --result: got results
        """
        if FUNC == 'forward':
            result = self.__forward(x)
        elif FUNC == 'get_param':
            assert param is not None
            result = self.__get_params(param)
        else:
            raise Exception('No other functions!')

        return result, self.model