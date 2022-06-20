# syntax=docker/dockerfile:1

FROM joyzoursky/python-chromedriver:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-u", "main.py"]