FROM python:3.11

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1


WORKDIR /app
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y netcat-traditional postgresql-client
RUN pip install --upgrade pip
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
ADD . /app

ENTRYPOINT ["/app/docker/entrypoint.sh"]
