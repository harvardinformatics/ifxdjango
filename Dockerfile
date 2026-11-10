# syntax=docker/dockerfile:experimental
FROM python:3.14-trixie as base

EXPOSE 80
RUN apt-get update -y && apt-get install -y psmisc \
    nginx \
    supervisor \
    curl \
    imagemagick
RUN mkdir ~/.ssh && echo "Host git*\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config

RUN curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && apt-get install -y nodejs

# Django REST backend
FROM base as drf

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install 'Django>4,<5' && \
    pip install gunicorn=='21.2.0' && \
    pip install -r requirements.txt

ADD . /app

ENV PYTHONPATH /app:/app/djvocab:/app/ifxurls:/app/nanites.client:/app/ifxuser:/app/ifxauth:/app/ifxmail.client:/app/ifxrequest:/app/ifxec:/app/fiine.client:/app/ifxbilling:/app/ifxlog:/app/ifxreservation:/app/ifxreport
ENV DJANGO_SETTINGS_MODULE {{project_name}}.settings

RUN mkdir -p /app/media/reports
RUN mkdir -p /app/media/uploads/tool_thumbs
RUN mkdir -p /app/media/uploads/tool_images
RUN mkdir -p /app/static

CMD ./wait-for-it.sh -t 120 {{project_name}}-db:3306 && \
    ./manage.py collectstatic --no-input && \
    ./manage.py makemigrations {{project_name}} && \
    ./manage.py migrate && \
    ./manage.py applyDevData && \
    ./manage.py runserver 0.0.0.0:80 --insecure

# Vue frontend
FROM base as ui

EXPOSE 8080
WORKDIR /app/frontend
CMD npm run dev

# Production
FROM drf as prod

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY etc/nginx.conf /etc/nginx/sites-available/default
COPY etc/supervisor.conf /etc/supervisor/conf.d/app.conf

RUN rm -rf /app/frontend/dist/* && rm -rf /static/*
RUN cd frontend && yarn cache clean && yarn add harvardinformatics/ifxvue#deploy --network-timeout 100000 && yarn --check-files && rm -f yarn.lock && (yarn build || yarn build)
RUN mkdir -p /app/frontend/dist/static && ./manage.py collectstatic --noinput
RUN cp -r /app/frontend/dist/* /static

CMD /usr/bin/supervisord -n
