# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXAPIDOC  = sphinx-apidoc
SOURCEDIR     = docs/src
BUILDDIR      = docs/build

PRODIMAGE     = harvardinformatics/{{project_name}}:latest
PRODBUILDARGS =

DEVDRFIMAGE   = {{project_name}}-drf
DEVDRFBUILDARGS =
DEVDRFFILE    = Dockerfile
DEVUIIMAGE    = {{project_name}}-ui
DEVUIFILE     = Dockerfile

DOCKERCOMPOSEFILE = docker-compose.yml
DOCKERCOMPOSEARGS =

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help docs Makefile prod up down build

build: drf ui
ui:
	docker build -t $(DEVUIIMAGE) -f $(DEVUIFILE) . --target ui
drf:
	docker build -t $(DEVDRFIMAGE) -f $(DEVDRFFILE) $(DEVDRFBUILDARGS) . --target drf
prod:
	./set-version.sh
	docker build --platform linux/amd64 -t $(PRODIMAGE) $(PRODBUILDARGS) . --target prod
	docker push $(PRODIMAGE)
up: drf
	docker compose -f $(DOCKERCOMPOSEFILE) $(DOCKERCOMPOSEARGS) up
down:
	docker compose -f $(DOCKERCOMPOSEFILE) down
up-local:
	docker compose -f docker-compose-local.yml $(DOCKERCOMPOSEARGS) up
down-local:
	docker compose -f docker-compose-local.yml down

test: drf
	docker compose run {{project_name}}-drf ./wait-for-it.sh -t 60 {{project_name}}-db:3306 -- ./manage.py test -v 2; docker compose down

docs:
	docker compose run {{project_name}}-drf make html; docker compose down

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXAPIDOC) -e -M --force -o "$(SOURCEDIR)" {{project_name}} {{project_name}}/migrations*
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
