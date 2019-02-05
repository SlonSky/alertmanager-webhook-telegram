FROM python:3.6

COPY docker/run.sh *.py requirements.txt /alertmanager-webhook-telegram/

WORKDIR /alertmanager-webhook-telegram

RUN pip install setuptools && \
    pip install -r requirements.txt ;\
    chmod +x run.sh

EXPOSE 9119

ENTRYPOINT ["./run.sh"]
