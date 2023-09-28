FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN apt-get update -y && apt-get install -y unzip
RUN pip3 install -r ./requirements.txt --no-cache-di
COPY deps/ deps/
RUN cd deps/ && unzip English-to-IPA.zip && cd English-to-IPA-master/ && python -m pip install .
COPY . .