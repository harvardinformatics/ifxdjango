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
RUN npm install -g @vue/cli@4.5.9 @vue/cli-service@4.5.9 eslint@7.9.0 n@7.0.0 node-gyp@7.1.2 npm@6.14.10 yarn@1.22.10

WORKDIR /app

ARG DJVOCAB_COMMIT=a0cfeba93ea805d3861e97e9c38fd27447e5b58a
ARG IFXURLS_COMMIT=b9109ab326393be2b216600ff114e98b2a826422
ARG NANITES_CLIENT_COMMIT=a11ff96ccb2c888d0d07ac97f27de1153463bf59
ARG IFXUSER_COMMIT=909b88fbf35f7d3000398ff211a5361921df32d7
ARG IFXAUTH_COMMIT=afcaad2b05f5dd90e86e53b2de864bef04c91898
ARG IFXMAIL_CLIENT_COMMIT=5fc6d834c76c0f66d823ff0b5d384ab7b30009b0
ARG IFXSEMANTICDATA_COMMIT=4c5271fac3ec43b694c04e01e865ad636f81d494
ARG IFXREQUEST_COMMIT=9aa45ce73b8fe98905dcadc57856b7c1e93fa6e1
ARG IFXBILLING_COMMIT=0a0d74edc1c7998585efd91f4152377478323f4f

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

