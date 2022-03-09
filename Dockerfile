FROM python:3.9

RUN apt-get update
RUN apt-get install telnet

WORKDIR /deployment
COPY ./app ./app
COPY ./main.py .
COPY ./requirements.txt .
RUN mkdir wip
RUN pip install -r requirements.txt
ENV PYTHONPATH=/deployment

EXPOSE 5000/tcp

ENTRYPOINT ["python", "main.py"]