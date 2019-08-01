FROM python:3

EXPOSE 80
RUN apt-get update -y && apt-get install -y \
    nginx \
    supervisor \
    curl

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY etc/nginx.conf /etc/nginx/sites-available/default
COPY etc/supervisor.conf /etc/supervisor/conf.d/app.conf

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash - && apt-get install -y nodejs
RUN npm install npm@latest -g

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip && \
    pip install gunicorn && \
    pip install git+https://github.com/harvardinformatics/djvocab.git@a0cfeba93ea805d3861e97e9c38fd27447e5b58a && \
    pip install git+https://github.com/harvardinformatics/ifxurls.git@72f75b3fcc9446fc5095ad747b3ed53d05bc4799 && \
    pip install git+https://github.com/harvardinformatics/ifxuser.git@6e54fdc6bba0d76c717d79484209872e7db2b059 && \
    pip install git+https://github.com/harvardinformatics/ifxauth.git@3c81a098f5a099e2d0d4baea00d80cc0ed0e834a && \
    pip install git+https://github.com/harvardinformatics/ifxmail.client.git@b649c6ed9edfa7cae5a402485e689fcaf1e3dc86 && \
    pip install -r requirements.txt

ADD . /app

ENV PYTHONPATH /app

RUN rm -rf /app/frontend/dist/* && rm -rf /app/static/* && rm -rf /app/frontend/node_modules/* && (cd frontend && npm install . && npm run-script build)
RUN mkdir -p /app/frontend/dist/static && ./manage.py collectstatic --noinput
RUN cp -r /app/frontend/dist/* /app/static

CMD ./manage.py makemigrations && ./manage.py migrate && /usr/bin/supervisord -n

