# syntax=docker/dockerfile:experimental
FROM python:3.6

EXPOSE 80
RUN apt-get update -y && apt-get install -y \
    nginx \
    supervisor \
    curl
RUN mkdir ~/.ssh && echo "Host git*\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY etc/nginx.conf /etc/nginx/sites-available/default
COPY etc/supervisor.conf /etc/supervisor/conf.d/app.conf

RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && apt-get install -y nodejs
RUN apt-get install npm -y
RUN npm install npm@6.14.11 -g
# Forcing install of these versions.  Goes haywire otherwise
RUN npm install -g @vue/cli@4.5.9 @vue/cli-service@4.5.9 eslint@7.9.0 n@7.0.0 node-gyp@7.1.2 npm@6.14.10 yarn@1.22.10 prettier@2.3.2

WORKDIR /app

ARG DJVOCAB_COMMIT=ad47dcbe7a75e9c3b70c4dec4c56399fd55de514
ARG IFXURLS_COMMIT=92c683c46683e71cd1259a60cca8ed5db104b1d7
ARG NANITES_CLIENT_COMMIT=8eebbe1536fc21f8c7baf362194a8dd90b4f0663
ARG IFXUSER_COMMIT=eecc611fa78f0c2ebf5f476ecff2cd5cabe80467
ARG IFXAUTH_COMMIT=82e0b691633ba79fcb6dd69bb4a29fb0207f7a9a
ARG IFXMAIL_CLIENT_COMMIT=cc1a9f9cc6cdb951828b6b912bc830c0172785f1
ARG IFXSEMANTICDATA_COMMIT=4c5271fac3ec43b694c04e01e865ad636f81d494
ARG IFXREQUEST_COMMIT=bae5ed1b87ac6ab146e855501c3b17236729d3eb
ARG IFXBILLING_COMMIT=f6c30fbda9586410802daae498e5c67f47fdb030

COPY requirements.txt /app

RUN --mount=type=ssh pip install --upgrade pip && \
    pip install gunicorn && \
    pip install 'Django>2.2,<3' && \
    pip install git+ssh://git@github.com/harvardinformatics/djvocab.git@${DJVOCAB_COMMIT} && \
    pip install git+ssh://git@github.com/harvardinformatics/ifxurls.git@${IFXURLS_COMMIT} && \
    pip install git+ssh://git@github.com/harvardinformatics/nanites.client.git@${NANITES_CLIENT_COMMIT} && \
    pip install git+ssh://git@github.com/harvardinformatics/ifxuser.git@${IFXUSER_COMMIT} && \
    pip install git+ssh://git@github.com/harvardinformatics/ifxauth.git@${IFXAUTH_COMMIT} && \
    pip install git+ssh://git@github.com/harvardinformatics/ifxmail.client.git@${IFXMAIL_CLIENT_COMMIT} && \
    pip install git+ssh://git@github.com/harvardinformatics/ifxsemanticdata.git@${IFXSEMANTICDATA_COMMIT} && \
    pip install git+ssh://git@github.com/harvardinformatics/ifxrequest.git@${IFXREQUEST_COMMIT} && \
    pip install git+ssh://git@gitlab-int.rc.fas.harvard.edu/informatics/ifxbilling.git@${IFXBILLING_COMMIT} && \
    pip install -r requirements.txt

ADD . /app

ENV PYTHONPATH /app

RUN rm -rf /app/frontend/dist/* && rm -rf /static/*
RUN cd frontend && yarn cache clean && yarn add harvardinformatics/ifxvue#ajk_deploy && yarn --check-files && yarn build
RUN mkdir -p /app/frontend/dist/static && ./manage.py collectstatic --noinput
RUN cp -r /app/frontend/dist/* /static

CMD ./manage.py makemigrations && ./manage.py migrate && /usr/bin/supervisord -n

