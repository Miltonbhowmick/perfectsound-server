FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=core.settings.dev

RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin

WORKDIR /app/server/

COPY ./server /app/server/
COPY ./server/requirements /app/server/

RUN pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements/dev.txt
