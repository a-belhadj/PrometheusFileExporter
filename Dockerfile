FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /opt/exporter/
WORKDIR /opt/exporter/
ADD requirements.txt .
RUN pip3 install -r requirements.txt
ADD src src
CMD python src/exporter.py
