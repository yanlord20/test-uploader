FROM python:3.10-slim

WORKDIR /app

RUN python3 -m pip install --upgrade pip setuptools wheel

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN python3 -m pip check

COPY ./ /app

CMD ["python", "main.py"]