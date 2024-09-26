# syntax=docker/dockerfile:experimental
FROM python:3.10-bookworm as base

EXPOSE 80
RUN apt-get update -y && apt-get install -y psmisc \
    nginx \
    supervisor \
    curl \
    imagemagick
RUN mkdir ~/.ssh && echo "Host git*\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config

RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
         | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    NODE_MAJOR=16 && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" \
         | tee /etc/apt/sources.list.d/nodesource.list && \
   apt-get -qy update && \
   apt-get -qy install nodejs=16.20.2-1nodesource1

# Forcing install of these versions.  Goes haywire otherwise
RUN npm install -g @vue/cli@4.5.9 @vue/cli-service@4.5.9 eslint@7.32.0 n@7.0.0 node-gyp@7.1.2 npm@6.14.10 yarn@1.22.10 prettier@2.3.2

# Django REST backend
FROM base as drf

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install 'Django>4,<5' && \
    pip install gunicorn=='21.2.0' && \
    pip install -r requirements.txt

ADD . /app

ENV PYTHONPATH /app:/app/djvocab:/app/ifxurls:/app/nanites.client:/app/ifxuser:/app/ifxauth:/app/ifxmail.client:/app/ifxrequest:/app/ifxec:/app/fiine.client:/app/ifxbilling:/app/ifxlog
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
CMD npm run-script serve

# Production
FROM drf as prod

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY etc/nginx.conf /etc/nginx/sites-available/default
COPY etc/supervisor.conf /etc/supervisor/conf.d/app.conf

RUN rm -rf /app/frontend/dist/* && rm -rf /static/*
RUN cd frontend && yarn cache clean && yarn add harvardinformatics/ifxvue#ajk_deploy --network-timeout 100000 && yarn --check-files && rm -f yarn.lock && (yarn build || yarn build)
RUN mkdir -p /app/frontend/dist/static && ./manage.py collectstatic --noinput
RUN cp -r /app/frontend/dist/* /static

CMD ./manage.py migrate && /usr/bin/supervisord -n
