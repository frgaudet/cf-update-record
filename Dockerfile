FROM python:3

ADD requirements.txt check.sh check.py /

RUN pip install -r requirements.txt && \
    chmod 755 /check.sh

CMD /check.sh

LABEL version="0.0.3"
