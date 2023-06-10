FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt .
COPY deps/ deps/
RUN pip3 install -r ./requirements.txt --no-cache-di
RUN cd deps/English-to-IPA/ && python -m pip install .
COPY . .
CMD ["gunicorn", "english.wsgi:application", "--bind", "0:8000"]