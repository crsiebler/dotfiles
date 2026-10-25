FILES = aliases/.aliases aliases/.docker_aliases aliases/.git_aliases aliases/.node_aliases aliases/.symfony_aliases zsh/.zshenv zsh/.zshrc
PYTHON ?= python3.11
.DEFAULT_GOAL := install

.PHONY: install check-install-prerequisites install-zsh-extensions install-ai install-codex install-opencode preview-ai-cleanup validate-ai clean sync-env

# AI installation reconciles verified retired skills after installing replacements.
# Override AI_TARGET=opencode or codex to preview one harness.
AI_TARGET ?= all
preview-ai-cleanup:
	@$(PYTHON) scripts/install-ai.py $(AI_TARGET) --preview

install-ai:
	@$(PYTHON) scripts/install-ai.py all

install-codex:
	@$(PYTHON) scripts/install-ai.py codex

install-opencode:
	@$(PYTHON) scripts/install-ai.py opencode

validate-ai:
	@$(PYTHON) scripts/install-ai.py validate

# Full setup includes shell/env/git changes.
# AI-only targets above never install binaries or require sudo.
install-zsh-extensions:
	@$(PYTHON) scripts/install-zsh-extensions.py

check-install-prerequisites:
	@$(PYTHON) scripts/install-ai.py opencode --check-prerequisites

# Keep mutations in the recipe so even make -j waits for the CLI check.
install: check-install-prerequisites
	$(MAKE) install-zsh-extensions
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
	@echo "Installed shell/env setup."

# Remove recognized shell and AI installer backups, preserving active files.
clean:
	@$(PYTHON) scripts/clean-install-backups.py

sync-env:
	@python3 $(CURDIR)/scripts/sync-env.py
