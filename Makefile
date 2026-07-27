lint:
	shellcheck skills/mediacrawler/scripts/*.sh
	npx -y skills-ref validate skills/mediacrawler

.PHONY: lint
