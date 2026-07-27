lint:
	shellcheck skills/*/scripts/*.sh
	uvx ruff check skills/*/scripts/*.py
	npx -y skills-ref validate skills/mediacrawler
	npx -y skills-ref validate skills/seedance

.PHONY: lint
