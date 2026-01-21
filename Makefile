FILES = aliases/.aliases aliases/.docker_aliases aliases/.git_aliases aliases/.node_aliases aliases/.symfony_aliases zsh/.zshenv zsh/.zshrc

install:
	@if [ -f ~/.zshrc ]; then cp ~/.zshrc ~/.zshrc.backup.$$(date +%Y%m%d_%H%M%S); fi
	for file in $(FILES); do cp -f $$file ~/; done
	@if [ -f $$HOME/.env ]; then \
	  cp -f $$HOME/.env $$HOME/.env.backup.$$(date +%Y%m%d_%H%M%S); \
	  echo "Backed up existing .env to .env.backup.*"; \
	fi
	@if [ ! -f $$HOME/.env ]; then \
	  cp env/.env.example $$HOME/.env; \
	  echo "Copied env/.env.example to $$HOME/.env. Please edit this file to add your secrets."; \
	else \
	  echo "$$HOME/.env already exists."; \
	fi
	@mkdir -p $$HOME/.config/opencode
	cp -r ai/opencode/* $$HOME/.config/opencode/
	@echo "Copied ai/opencode/ directory contents to $$HOME/.config/opencode/."
	cp ai/ralph.md $$HOME/.config/opencode/ralph.md
	@echo "Copied ai/ralph.md to $$HOME/.config/opencode/ralph.md."
	@if [ -f /usr/bin/ralph ]; then \
	  if sudo cp /usr/bin/ralph /usr/bin/ralph.backup.$$(date +%Y%m%d_%H%M%S); then \
	    echo "Backed up existing ralph to /usr/bin/ralph.backup.*"; \
	  else \
	    echo "Error: Failed to back up existing /usr/bin/ralph. Aborting installation to avoid data loss."; \
	    exit 1; \
	  fi; \
	fi
	sudo cp bin/ralph /usr/bin/ralph
	sudo chmod +x /usr/bin/ralph
	@echo "Installed ralph CLI to /usr/bin/ralph."
	@echo "Installation complete. Dotfile setup, .env, opencode config, and ralph CLI are in place. Please run 'source ~/.zshenv' or restart your shell to apply changes."

clean:
	@echo "Removing dotfile backups (.zshrc, .env, ralph)..."
	@rm -f $${HOME}/.zshrc.backup.*
	@rm -f $${HOME}/.env.backup.*
	@sudo rm -f /usr/bin/ralph.backup.*
	@echo "Backup removal complete."
