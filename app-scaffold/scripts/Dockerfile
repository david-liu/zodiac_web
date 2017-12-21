FROM python:2.7-slim
#FROM tensorflow/tensorflow

MAINTAINER David Liu <willow990.cn@google.com>

RUN mkdir /opt/{app_name}
COPY requirements.txt /opt/{app_name}/requirements.txt
COPY {setup_whl_file} /opt/{app_name}/{setup_whl_file}

RUN pip install /opt/{app_name}/{setup_whl_file}
RUN pip --no-cache-dir install -r /opt/{app_name}/requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

RUN rm /opt/{app_name}/{setup_whl_file}

RUN mkdir /opt/{app_name}/logs

# Copy code 
ADD src /opt/{app_name}/src
ADD scripts /opt/{app_name}/scripts
COPY service.sh /opt/{app_name}/run_service.sh
RUN chmod +x /opt/{app_name}/run_service.sh

EXPOSE {port}

WORKDIR "/opt/{app_name}/"

CMD ["/opt/{app_name}/run_service.sh", "debug"]



