PACKAGE_NAME={{project_name}}
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXAPIDOC  = sphinx-apidoc
SOURCEDIR     = docs/src
BUILDDIR      = docs/build

PRODIMAGE     = harvardinformatics/{{project_name}}:latest
PRODBUILDARGS = --ssh default

DEVDRFIMAGE   = drf
DEVDRFBUILDARGS = --ssh default
DEVDRFFILE    = Dockerfile-drf
DEVUIIMAGE    = ui
DEVUIFILE     = Dockerfile-ui

DOCKERCOMPOSEFILE = docker-compose.yml
DOCKERCOMPOSEARGS = 

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help docs Makefile prod up down
prod:
	docker build -t $(PRODIMAGE) $(PRODBUILDARGS) .
	docker push $(PRODIMAGE)
up:
	docker build -t $(DEVDRFIMAGE) -f $(DEVDRFFILE) $(DEVDRFBUILDARGS) .
	docker-compose -f $(DOCKERCOMPOSEFILE) $(DOCKERCOMPOSEARGS) up
down:
	docker-compose -f $(DOCKERCOMPOSEFILE) down

up-local:
	docker build -t $(DEVDRFIMAGE) -f $(DEVDRFFILE) $(DEVDRFBUILDARGS) .
	docker-compose -f docker-compose-local.yml $(DOCKERCOMPOSEARGS) up
down-local:
	docker-compose -f docker-compose-local.yml down
test:
	docker-compose run drf ./manage.py test -v 2; docker-compose down

docs:
	docker-compose run drf make html; docker-compose down

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXAPIDOC) -e -M --force -o "$(SOURCEDIR)" nice nice/migrations*
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
