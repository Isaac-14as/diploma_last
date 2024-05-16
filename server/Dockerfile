FROM python:3.11.8

RUN mkdir /diploma

WORKDIR /diploma

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN chmod a+x /diploma/docker/*.sh