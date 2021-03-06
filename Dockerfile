# syntax=docker/dockerfile:experimental
FROM python:3.6

EXPOSE 80
RUN apt-get update -y && apt-get install -y \
    nginx \
    supervisor \
    curl
RUN mkdir ~/.ssh && echo "Host github.com\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY etc/nginx.conf /etc/nginx/sites-available/default
COPY etc/supervisor.conf /etc/supervisor/conf.d/app.conf
COPY etc/logging.ini /etc/logging.ini

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && apt-get install -y nodejs
RUN apt-get install npm -y
RUN npm install npm@latest -g

WORKDIR /app

ARG DJVOCAB_COMMIT=ad47dcbe7a75e9c3b70c4dec4c56399fd55de514
ARG IFXURLS_COMMIT=6ce5e88f22dddd66d4468205777f28a7b31dd5ed
ARG NANITES_CLIENT_COMMIT=6162573c8dbd2ca6604163ae0b1e8d41c5b143da
ARG IFXUSER_COMMIT=056d06c5592ca72c911fffdc9c7436441f78ce31
ARG IFXAUTH_COMMIT=9bffad89afa07395e237567fd61e9919b0cc905c
ARG IFXMAIL_CLIENT_COMMIT=ac1e4dadfa12509a97c3a4bb9c76f1d93350ed02

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
    pip install -r requirements.txt

ADD . /app

ENV PYTHONPATH /app

RUN rm -rf /app/frontend/dist/* && rm -rf /static/* && rm -rf /app/frontend/node_modules/* && (cd frontend && npm install . && npm run-script build)
RUN mkdir -p /app/frontend/dist/static && ./manage.py collectstatic --noinput
RUN cp -r /app/frontend/dist/* /static

CMD ./manage.py makemigrations && ./manage.py migrate && /usr/bin/supervisord -n

