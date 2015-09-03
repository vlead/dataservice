BUILD_DEST=build

CODE_DEST="${BUILD_DEST}/code"
VER_BRANCH=build-release
VER_FILE=VERSION

LITERATE_TOOLS="https://github.com/vlead/literate-tools.git"
LITERATE_DIR=literate-tools
ELISP_DIR=elisp
ORG_DIR=org-templates
STYLE_DIR=style
PWD=$(shell pwd)

all:  clean build

clean-literate:
	rm -rf ${ELISP_DIR}
	rm -rf ${ORG_DIR}
	rm -rf ${STYLE_DIR}
	rm -rf src/${ORG_DIR}
	rm -rf src/${STYLE_DIR}

pull-literate-tools:
	@echo "pulling literate support code"
	echo ${PWD}
ifeq ($(wildcard elisp),)
	git clone ${LITERATE_TOOLS}
	mv ${LITERATE_DIR}/${ELISP_DIR} .
	mv ${LITERATE_DIR}/${ORG_DIR} .
	mv ${LITERATE_DIR}/${STYLE_DIR} .
	rm -rf ${LITERATE_DIR}
	ln -s ${PWD}/${ORG_DIR}/ ${PWD}/src/${ORG_DIR}
	ln -s ${PWD}/${STYLE_DIR}/ ${PWD}/src/${STYLE_DIR}
else
	@echo "Literate support code already present"
endif

init: pull-literate-tools
	mkdir -p ${BUILD_DEST} ${CODE_DEST}

build: init write-version
	emacs  --script elisp/publish.el
	rm -f ${BUILD_DEST}/docs/*.html~

# get the latest commit hash and its subject line
# and write that to the VERSION file
write-version:
	echo -n "Built from commit: " > ${CODE_DEST}/${VER_FILE}
	echo `git rev-parse HEAD` >> ${CODE_DEST}/${VER_FILE}
	echo `git log --pretty=format:'%s' -n 1` >> ${CODE_DEST}/${VER_FILE}

lint: build only-lint

release: checkout-release build write-release-version rm-ver-branch only-lint

release-and-export: release export

# get the latest tagged release and write that to the VERSION file
write-release-version:
	git checkout release
	echo -n "VERSION: " > ${CODE_DEST}/${VER_FILE}
	echo `git describe` >> ${CODE_DEST}/${VER_FILE}
	#echo "--"
	#echo `git cat-file -p $(shell git describe)` >> ${CODE_DEST}/${VER_FILE}

# lint the ansible code for syntax errors; and also list tasks
only-lint:
	ansible-playbook -i ${CODE_DEST}/hosts --syntax-check --list-tasks ${CODE_DEST}/site.yml; \
	if [ $$? -eq 0 ] ; then echo "No syntax errors in ansible scripts." ; fi

# checkout the release branch, find the latest tag and put it that snapshot in
# a temporary branch
checkout-release:
	git checkout release
	if [ -z $(shell git describe --abbrev=0) ]; then echo "No tagged release found!"; exit 1; fi
	git checkout -b ${VER_BRANCH} $(shell git describe --abbrev=0)

# remove the temporarily created branch
rm-ver-branch:
	git checkout release
	git branch -d ${VER_BRANCH}

# copy the code dir to our configuration-server
export:
	rsync -auvz ${CODE_DEST} ${CONFIG_SERVER_USER}@${CONFIG_SERVER}:${CONFIG_SERVER_HOME_DIR}

clean:
	rm -rf ${BUILD_DEST}

