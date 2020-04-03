FROM python:3.6

EXPOSE 80
RUN apt-get update -y && apt-get install -y \
    nginx \
    supervisor \
    curl

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY etc/nginx.conf /etc/nginx/sites-available/default
COPY etc/supervisor.conf /etc/supervisor/conf.d/app.conf
COPY etc/logging.ini /etc/logging.ini

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash - && apt-get install -y nodejs
RUN apt-get install npm -y
RUN npm install npm@latest -g

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install gunicorn && \
    pip install Django>2.2,<3 && \
    pip install git+https://github.com/harvardinformatics/djvocab.git@a0cfeba93ea805d3861e97e9c38fd27447e5b58a && \
    pip install git+https://github.com/harvardinformatics/ifxurls.git@72f75b3fcc9446fc5095ad747b3ed53d05bc4799 && \
    pip install git+https://github.com/harvardinformatics/ifxuser.git@701eec94d06e83fcb42416b9fb07255569c4c2c4 && \
    pip install git+https://github.com/harvardinformatics/ifxauth.git@3c81a098f5a099e2d0d4baea00d80cc0ed0e834a && \
    pip install git+https://github.com/harvardinformatics/ifxmail.client.git@b649c6ed9edfa7cae5a402485e689fcaf1e3dc86 && \
    pip install -r requirements.txt

ADD . /app

ENV PYTHONPATH /app

RUN rm -rf /app/frontend/dist/* && rm -rf /static/* && rm -rf /app/frontend/node_modules/* && (cd frontend && npm install . && npm run-script build)
RUN mkdir -p /app/frontend/dist/static && ./manage.py collectstatic --noinput
RUN cp -r /app/frontend/dist/* /static

CMD ./manage.py makemigrations && ./manage.py migrate && /usr/bin/supervisord -n

