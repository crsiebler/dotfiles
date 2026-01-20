FILES = .aliases .docker_aliases .git_aliases .node_aliases .symfony_aliases .zshenv .zshrc

install:
	@if [ -f ~/.zshrc ]; then cp ~/.zshrc ~/.zshrc.backup.$$(date +%Y%m%d_%H%M%S); fi
	for file in $(FILES); do cp -f $$file ~/; done
	@if [ -f $$HOME/.env ]; then \
	  cp -f $$HOME/.env $$HOME/.env.backup.$$(date +%Y%m%d_%H%M%S); \
	  echo "Backed up existing .env to .env.backup.*"; \
	fi
	@if [ ! -f $$HOME/.env ]; then \
	  cp .env.example $$HOME/.env; \
	  echo "Copied .env.example to $$HOME/.env. Please edit this file to add your secrets."; \
	else \
	  echo "$$HOME/.env already exists."; \
	fi
	@mkdir -p $$HOME/.config/opencode
	@if [ -f $$HOME/.config/opencode/opencode.json ]; then \
	  cp $$HOME/.config/opencode/opencode.json $$HOME/.config/opencode/opencode.json.backup.$$(date +%Y%m%d_%H%M%S); \
	  echo "Backed up existing opencode.json to opencode.json.backup.*"; \
	fi
	cp opencode.json $$HOME/.config/opencode/opencode.json
	@echo "Copied opencode.json to $$HOME/.config/opencode/opencode.json."
	@echo "Installation complete. Dotfile setup, .env, and opencode config are in place. Please run 'source ~/.zshenv' or restart your shell to apply changes."
