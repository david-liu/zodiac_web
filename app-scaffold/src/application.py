# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from zodiac_web import sequence_service

logger = logging.getLogger(__name__)


class TestApplication(object):
    def __init__(self):
        pass

    def train(self, re_training=False):
        pass

    @sequence_service(noun="test_app", verb="predict")
    def predict(self, top_k=2):
        """
        @api {get} api/v1/test_app/predict predict the model
        @apiName predict the model
        @apiParam {int=2}[top_k] retur the top k result
        @apiGroup Predict API
        """
        return {
            'top_k': top_k
        }
