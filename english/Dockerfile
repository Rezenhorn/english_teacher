FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update -y && apt-get install -y unzip
# RUN apt-get install gcc -y
RUN pip3 install -r ./requirements.txt --no-cache-di
COPY deps/ deps/
RUN cd deps/ && unzip English-to-IPA.zip && cd English-to-IPA-master/ && python -m pip install .
COPY . .
# CMD ["gunicorn", "english.wsgi:application", "--bind", "0:8000"]
# TODO: usgi сделать