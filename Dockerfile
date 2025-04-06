# FROM jupyter/pyspark-notebook:latest
FROM jupyter/base-notebook:latest

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /requirements.txt