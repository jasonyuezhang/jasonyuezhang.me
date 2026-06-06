.PHONY: serve build post resume publish-resume setup-resume

CATEGORY ?= notes

serve:
	bundle exec jekyll serve

build:
	bundle exec jekyll build

post:
	@test -n "$(TITLE)" || (echo 'Usage: make post TITLE="Post Title" [CATEGORY=notes]' >&2; exit 1)
	./scripts/new_post.sh "$(TITLE)" "$(CATEGORY)"

setup-resume:
	./scripts/setup_resume.sh

resume:
	./resume/build.sh

publish-resume:
	./scripts/publish_resume.sh
