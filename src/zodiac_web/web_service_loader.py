# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
import json
import logging
import optparse

from flask import request, jsonify, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import time

from zodiac_web.utils.rest_helper import success_response, fail_response, error_response
from zodiac_web import sequence_service

logger = logging.getLogger(__name__)


class WebServiceLoader(object):
    def __init__(self, app, log_file_path=None, version='v1'):
        self.app = app
        self._default_version = version

        self._log_file_path = log_file_path

        app.add_url_rule('/', 'index', self.index, methods=['GET'])
        app.add_url_rule('/api/inspect', 'service_inspect', self.api_inspect, methods=['GET'])
        app.add_url_rule('/api/<version>/<noun>/<verb>', 'service', self.service, methods=['POST', 'GET'])

        self.service_registry = {}

        self.register_service_method(self.show_logs)

    def get_command_line_options(self, default_host, default_port):
        """
        Takes a flask.Flask instance and runs it. Parses 
        command-line flags to configure the app.
        """

        # Set up the command-line options
        parser = optparse.OptionParser()
        parser.add_option("-H", "--host",
                          help="Hostname of the Flask app " + \
                               "[default %s]" % default_host,
                          default=default_host)
        parser.add_option("-P", "--port",
                          help="Port for the Flask app " + \
                               "[default %s]" % default_port,
                          default=default_port)

        # Two options useful for debugging purposes, but 
        # a bit dangerous so not exposed in the help message.
        parser.add_option("-d", "--debug",
                          action="store_true", dest="debug",
                          help=optparse.SUPPRESS_HELP)
        parser.add_option("-p", "--profile",
                          action="store_true", dest="profile",
                          help=optparse.SUPPRESS_HELP)

        options, _ = parser.parse_args()

        return options

    def start(self, default_host="0.0.0.0",
              default_port="5000"):
        logger.info("start app on %s:%s", default_host, default_port)

        self.app.run(
            debug=False,
            host=default_host,
            port=int(default_port)
        )

    def index(self):
        return 'Hello service'

    @sequence_service(noun="manage", verb="logs")
    def show_logs(self, reverse=False):
        """
        @api {get} api/manage/logs show all logs 
        @apiName Show logs
        @apiParam {bool=false}[reverse] show the log reversed
        @apiGroup Meta API
        """

        if self._log_file_path is None:
            return []
        else:
            logs = []
            with open(self._log_file_path, 'r') as outfile:
                for log_str in outfile:
                    try:
                        log = json.loads(log_str.strip())

                        if reverse:
                            logs.insert(0, log)
                        else:
                            logs.append(log)
                    except Exception as inst:
                        logger.error("find exception during load error: %s", inst)

            return logs

    def api_inspect(self):
        """
        @api {get} api/inspect inspect all API definition
        @apiName API Inspect
        @apiGroup Meta API
        """
        serivce_desc = {}
        for key, service_config in self.service_registry.items():
            url = '/api/' + "/".join(key.split('.'))

            parameters = {}

            for arg, config in service_config['required_args'].items():
                parameters_config = dict(config.items()[:])
                parameters_config["required"] = True

                # del parameters_config['default']
                if parameters_config["desc"] is None:
                    del parameters_config["desc"]

                if parameters_config["type"] is None:
                    del parameters_config["type"]

                parameters[arg] = parameters_config

            for arg, config in service_config['optional_args'].items():
                parameters_config = dict(config.items()[:])
                parameters_config["required"] = False

                if parameters_config["type"] is None:
                    parameters_config["type"] = type(parameters_config["default"]).__name__

                if parameters_config["desc"] is None:
                    del parameters_config["desc"]

                parameters[arg] = parameters_config

            serivce_desc[url] = {
                'desc': service_config['desc'],
                'parameters': parameters
            }

        return jsonify(serivce_desc)

    def service(self, version, noun, verb):

        logger.info('Get a request from [%s]: %s' % (request.remote_addr, request.url))
        if request.method == 'POST':

            if request.json:

                service_config = self._find_service_config(version, noun, verb)

                if not service_config:
                    return jsonify(fail_response('there is no service registed on /api/%s/%s' % (noun, verb)))

                return self._invoke_service(request.json, service_config)

            else:
                return jsonify(error_response("can not found any data"))
        elif request.method == 'GET':

            service_config = self._find_service_config(version, noun, verb)

            if not service_config:
                return jsonify(fail_response('there is no service registed on /api/%s/%s' % (noun, verb)))

            return self._invoke_service(request.args, service_config)

    def _invoke_service(self, request_data, service_config):
        requested_args = service_config['required_args']
        optional_args = service_config['optional_args']

        request_payload = {}
        input_error_messages = {}
        for arg in requested_args.keys():
            if arg in request_data:
                request_payload[arg] = request_data[arg]
            else:
                input_error_messages[arg] = 'the field [%s] is required' % arg

        for arg in optional_args.keys():
            if arg in request_data:
                request_payload[arg] = request_data[arg]

        if input_error_messages:
            return jsonify(fail_response(input_error_messages))
        else:
            service_fn = service_config['method']
            try:
                result = service_fn(**request_payload)

                return jsonify(success_response(result))

            # except ValueError as inst:
            #     return jsonify(fail_response(str(inst)))

            except Exception as inst:
                logger.error("find exception during evaluate: %s", inst)


                return jsonify(error_response(str(inst)))

    def register_service_object(self, obj):
        all_methods = inspect.getmembers(obj, predicate=inspect.ismethod)

        for name, method in all_methods:
            self.register_service_method(method)

    def register_service_method(self, method):
        if hasattr(method, '__service_config__'):
            service_config = method.__service_config__

            if service_config['version'] is None:
                version = self._default_version
            else:
                version = service_config['version']

            logger.debug("begin to register method: %s on [%s:%s:%s]" % (version,
                                                                         method.__name__, service_config['noun'],
                                                                         service_config['verb']))

            key = "%s.%s.%s" % (version, service_config['noun'], service_config['verb'])

            if key in self.service_registry:
                raise ValueError('there existed a service registered with:'
                                 ' version=%s, noun=%s, verb=%s' % (version,
                                                                    service_config['noun'],
                                                                    service_config['verb']))
            self.service_registry[key] = {
                'method': method,
                'desc': service_config['description'],
                'required_args': service_config['required_args'],
                'optional_args': service_config['optional_args']
            }

    def register_file_upload_method(self, upload_folder, allow_file_extensions, url_rule, endpoint, page_template=None,
                                    keep_file_name=True, callback_fn=None):
        self.app.config['UPLOAD_FOLDER'] = upload_folder

        if page_template is None:
            page_template = '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form method=post enctype=multipart/form-data action={0}>
              <p><input type=file name=file>
                 <input type=submit value=Upload>
            </form>
            '''
            page_template = page_template.format(url_rule)

        def allowed_file(filename):
            return '.' in filename and \
                   filename.rsplit('.', 1)[1].lower() in allow_file_extensions

        def upload_file():
            if request.method == 'POST':
                # check if the post request has the file part
                if 'file' not in request.files:
                    logger.error('No file part')
                    return redirect(request.url)
                file = request.files['file']
                # if user does not select file, browser also
                # submit a empty part without filename
                if file.filename == '':
                    logger.error('No selected file')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)

                    if not keep_file_name:
                        ext = filename.rsplit('.', 1)[1]  # 获取文件后缀
                        unix_time = int(time.time())
                        new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
                    else:
                        new_filename = filename

                    file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], new_filename))

                    if callback_fn:
                        return callback_fn(new_filename)
                    else:
                        return redirect(url_for(endpoint + '_uploaded_file',
                                                filename=new_filename))
            return page_template

        def uploaded_file(filename):
            return send_from_directory(self.app.config['UPLOAD_FOLDER'],
                                       filename)

        self.app.add_url_rule(url_rule, endpoint + '_upload_file', upload_file, methods=['GET', 'POST'])
        self.app.add_url_rule('/uploads/<filename>',  endpoint + '_uploaded_file', uploaded_file, methods=['GET'])

    def _find_service_config(self, version, noun, verb):
        key = "%s.%s.%s" % (version, noun, verb)
        if key in self.service_registry:
            return self.service_registry[key]
        else:
            return None
