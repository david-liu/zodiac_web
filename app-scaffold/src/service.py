# -*- coding: utf-8 -*-
import logging

from flask import Flask

from application import TestApplication
from zodiac_web import WebServiceLoader, sequence_service
from zodiac_web.utils import helper

logger = logging.getLogger(__name__)

app = Flask(__name__)


@sequence_service(noun="manage", verb="health")
def health():
    return "hello world"


def initialize_app(cfg_file, section=None):
    logger.info('initialize application with configuration file:%s(%s)', cfg_file, section)

    web_service_loader = WebServiceLoader(app,
                                          log_file_path=helper.convert_to_abspath(__file__, '../logs/app.log'))
    web_service_loader.register_service_method(health)

    # Please create a application to register
    test_app = TestApplication()
    web_service_loader.register_service_object(test_app)

    return web_service_loader


if __name__ == '__main__':
    CONFIG_FILE = helper.convert_to_abspath(__file__, 'APP.INI')

    service_loader = initialize_app(CONFIG_FILE)
    service_loader.start()
