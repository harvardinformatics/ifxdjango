# ifxdjango
Django project template for ifx Django REST / VueJS / Vuetify applications

Use this project as a template for creating new Django projects using the FAS Informatics Django / REST / Vue JS / Vuetify
stack.  Sufficient boilerplate code is established to allow the project to get up and running.

First, to create the project use django-admin startproject; make sure all of the files that must be
processed (project_name substituted) are listed by name and extension:

    > mkdir ifxtest
    > cd ifxtest
    > django-admin startproject --template=https://github.com/harvardinformatics/ifxdjango/archive/v3.0.zip -e py,html,js,conf,sh,json,cfg,txt,vue -n .env.development,.env.production,Dockerfile-drf,Dockerfile-ui,Dockerfile,docker-compose.yml,Makefile ifxtest .

Add a 40 character REST application token to the docker-compose file at the *IFX_APP_TOKEN environment variable of the drf
section.  This will allow the application to interact with other systems.  Make sure this is different from other applications in the development environment (nanites/initDev.py has a pretty good list).  You may want to add this to the set of application
users setup in the nanites/initDev.py file.

It goes without saying that you do not want to use the production token here.

Library submodules should then be added to the application

   > for m in ifxauth ifxurls djvocab nanites.client ifxuser ifxmail.client ifxrequest ifxreport ifxec fiine.client ifxbilling; do git submodule add git@github.com:harvardinformatics/${m}.git; done

Your application may require a different list.  If so, make sure that PYTHONPATH is properly set.

Once the project has been created, build the necessary containers and install the Javascript libraries

    > make build
    > docker compose run ifxtest-ui yarn

After several minutes of this, you should be able to start up the application

    > docker compose up

Before logging in or attempting to access the authenticated "Demo" page (which automatically attemps to log you in), run the applyDevData management command to ensure that the test user is properly set up.

    > docker compose run ifxtest-drf ./manage.py applyDevData

UserSerializer and UserViewSet classes will need to be created in serializers.py.  They are not created beforehand
so that the proper local IfxUser subclass can be specified

