# ifxdjango
Django project template for ifx Django REST / VueJS / Vuetify applications

Use this project as a template for creating new Django projects using the FAS Informatics Django / REST / Vue JS / Vuetify
stack.  Sufficient boilerplate code is established to allow the project to get up and running.

First, to create the project use django-admin startproject; make sure all of the files that must be
processed (project_name substituted) are listed by name and extension:

    > mkdir ifxtest
    > cd ifxtest
    > django-admin startproject --template=https://github.com/harvardinformatics/ifxdjango/archive/v1.0.zip -e py,html,vue,js,conf -n .env.development,.env.production,Dockerfile-drf,docker-compose.yml ifxtest .

Once the project has been created, build the necessary containers and install the Javascript libraries

    > docker-compose build
    > docker-compose run ui npm install .

After several minutes of this, you should be able to start up the application

    > docker-compose up
