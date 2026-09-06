FILES = aliases/.aliases aliases/.docker_aliases aliases/.git_aliases aliases/.node_aliases aliases/.symfony_aliases zsh/.zshenv zsh/.zshrc
PYTHON ?= python3.11
.DEFAULT_GOAL := install

.PHONY: install install-ai install-codex install-opencode validate-ai clean sync-env

install-ai:
	@$(PYTHON) scripts/install-ai.py all

install-codex:
	@$(PYTHON) scripts/install-ai.py codex

install-opencode:
	@$(PYTHON) scripts/install-ai.py opencode

validate-ai:
	@$(PYTHON) scripts/install-ai.py validate

# Full setup includes shell/env/git changes and sudo Ralph.
# AI-only targets above never install binaries or require sudo.
install:
	@if [ -f ~/.zshrc ]; then cp ~/.zshrc ~/.zshrc.backup.$$(date +%Y%m%d_%H%M%S); fi
	for file in $(FILES); do cp -f $$file ~/; done
	@if [ ! -f $$HOME/.env ]; then \
	  cp env/.env.example $$HOME/.env; \
	  echo "Copied env/.env.example to $$HOME/.env. Please edit this file to add your secrets."; \
	else \
	  echo "$$HOME/.env already exists. Synchronizing environment keys..."; \
	  python3 $(CURDIR)/scripts/sync-env.py; \
	fi
	cp git/.gitignore_global $${HOME}/.gitignore_global
	git config --global core.excludesfile $${HOME}/.gitignore_global
	$(MAKE) install-opencode
	sudo cp bin/ralph /usr/local/bin/ralph
	sudo chmod +x /usr/local/bin/ralph
	@echo "Installed shell/env setup."

# Only .zshrc backups; other configuration cleanup remains manual.
clean:
	@case "$$HOME" in ""|/|[!/]*) printf '%s\n' 'HOME must be an absolute directory other than /.' >&2; exit 1 ;; esac
	rm -f -- "$$HOME"/.zshrc.backup.*
	@printf '%s\n' 'Removed .zshrc backups. Other files and backups were not changed.'

sync-env:
	@python3 $(CURDIR)/scripts/sync-env.py
