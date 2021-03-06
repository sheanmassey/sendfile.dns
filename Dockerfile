FROM python:3.9

WORKDIR /opt
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN mkdir /data
CMD python server.py
