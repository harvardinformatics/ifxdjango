# syntax=docker/dockerfile:experimental
FROM python:3.10-bookworm

EXPOSE 80
RUN apt-get update -y && apt-get install -y \
    nginx \
    supervisor \
    curl \
    gnupg \
    ca-certificates
RUN mkdir ~/.ssh && echo "Host git*\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY etc/nginx.conf /etc/nginx/sites-available/default
COPY etc/supervisor.conf /etc/supervisor/conf.d/app.conf

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

WORKDIR /app

COPY requirements.txt /app

RUN --mount=type=ssh pip install --upgrade pip && \
    pip install gunicorn && \
    pip install 'Django>4,<5' && \
    pip install certifi --upgrade --force && \
    pip install -r requirements.txt

ADD . /app

ENV PYTHONPATH /app:/app/ifxreport:/app/djvocab:/app/ifxurls:/app/nanites.client:/app/ifxuser:/app/ifxauth:/app/ifxmail.client:/app/ifxrequest:/app/fiine.client:/app/ifxbilling

RUN mkdir -p /app/media/reports
RUN rm -rf /app/frontend/dist/* && rm -rf /static/*
RUN cd frontend && yarn cache clean && yarn add harvardinformatics/ifxvue#ajk_deploy --network-timeout 100000 && yarn --check-files && yarn build
RUN mkdir -p /app/frontend/dist/static && ./manage.py collectstatic --noinput
RUN cp -r /app/frontend/dist/* /static

CMD ./manage.py migrate && /usr/bin/supervisord -n
