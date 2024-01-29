# Minimal makefile for Sphinx documentation
#

PACKAGE_NAME  = {{project_name}}
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXAPIDOC  = sphinx-apidoc
SOURCEDIR     = docs/src
BUILDDIR      = docs/build

PRODIMAGE     = registry.gitlab-int.rc.fas.harvard.edu/informatics/{{project_name}}:latest
PRODBUILDARGS = --ssh default

DRFIMAGE      = {{project_name}}-drf
DRFBUILDARGS  = --ssh default
DRFFILE       = Dockerfile-drf

UIIMAGE      = {{project_name}}-ui
UIBUILDARGS  =
UIFILE       = Dockerfile-ui

DOCKERCOMPOSEFILE = docker-compose.yml
DOCKERCOMPOSEARGS =

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: test Makefile docs drf ui build clean test-ui test-drf
clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -f
build: drf ui
ui:
	docker build -t $(UIIMAGE) -f $(UIFILE) $(UIBUILDARGS) .
drf:
	docker build -t $(DRFIMAGE) -f $(DRFFILE) $(DRFBUILDARGS) .

prod:
	./set-version.sh
	docker build --platform linux/amd64 -t $(PRODIMAGE) $(PRODBUILDARGS) . --no-cache
	docker push $(PRODIMAGE)
up: drf
	docker compose -f $(DOCKERCOMPOSEFILE) $(DOCKERCOMPOSEARGS) up
down:
	docker compose -f $(DOCKERCOMPOSEFILE) down
up-local: drf
	docker compose -f docker-compose-local.yml $(DOCKERCOMPOSEARGS) up
down-local:
	docker compose -f docker-compose-local.yml down
run: drf
	docker compose run $(DRFIMAGE) /bin/bash
test-drf: drf
	docker compose run $(DRFIMAGE) ./manage.py test -v 2; docker compose down
test-ui: ui
	docker volume rm {{project_name}}_{{project_name}}-data
	docker compose run $(UIIMAGE) ../wait-for-it.sh -s -t 120 {{project_name}}-drf:80 -- npm run-script test:e2e; docker compose down
test: test-drf
docs:
	docker compose run $(DRFIMAGE) make html; docker compose down

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXAPIDOC) -e -M --force -o "$(SOURCEDIR)" {{project_name}}
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
