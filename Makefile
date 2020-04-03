#
# Make file for docs and test.  Docs aren't setup yet
# Most of it gets generated in nanites/client/swagger, but for some reason, a nanites.client.swagger directory
# is also created.  Contents are copied to the correct location and the dir is removed.
#
PACKAGE_NAME={{project_name}}
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXAPIDOC  = sphinx-apidoc
SOURCEDIR     = docs/src
BUILDDIR      = docs/build


help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: test Makefile docs

test:
	docker-compose run drf ./manage.py test -v 2; docker-compose down

docs:
	docker-compose run drf make html; docker-compose down

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXAPIDOC) -e -M --force -o "$(SOURCEDIR)" {{project_name}}
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
