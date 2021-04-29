FROM python:3.9-buster
RUN useradd -ms /bin/bash app_runner
USER app_runner

ENV PYTHONBUFFERED=1
ENV PATH "$PATH:/home/app_runner/.local/bin"

WORKDIR /home/app_runner/code

ADD requirements/ ./requirements
RUN pip install -r ./requirements/prod.txt
COPY . /home/app_runner/code/
USER root
RUN chown -R app_runner:app_runner *