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
	# Install global gitignore for git configuration
	cp git/.gitignore_global $${HOME}/.gitignore_global
	git config --global core.excludesfile $${HOME}/.gitignore_global
	cp ai/ralph.md $$HOME/.config/opencode/ralph.md
	@echo "Copied ai/ralph.md to $$HOME/.config/opencode/ralph.md."
	@if [ -f $$HOME/.config/opencode/AGENTS.md ]; then \
	  cp $$HOME/.config/opencode/AGENTS.md $$HOME/.config/opencode/AGENTS.md.backup.$$(date +%Y%m%d_%H%M%S); \
	  echo "Backed up existing AGENTS.md to .config/opencode/AGENTS.md.backup.*"; \
	fi
	cp ai/opencode/AGENTS.md $$HOME/.config/opencode/AGENTS.md
	@echo "Copied ai/opencode/AGENTS.md to $$HOME/.config/opencode/AGENTS.md."
	@if [ -f /usr/local/bin/ralph ]; then \
	  if cp /usr/local/bin/ralph /usr/local/bin/ralph.backup.$$(date +%Y%m%d_%H%M%S); then \
	    echo "Backed up existing ralph to /usr/local/bin/ralph.backup.*"; \
	  else \
	    echo "Error: Failed to back up existing /usr/local/bin/ralph. Aborting installation to avoid data loss."; \
	    exit 1; \
	  fi; \
	fi
	sudo cp bin/ralph /usr/local/bin/ralph
	sudo chmod +x /usr/local/bin/ralph
	@echo "Installed ralph CLI to /usr/local/bin/ralph."
	@if [ -f /usr/local/bin/subagents ]; then \
	  if cp /usr/local/bin/subagents /usr/local/bin/subagents.backup.$$(date +%Y%m%d_%H%M%S); then \
	    echo "Backed up existing subagents to /usr/local/bin/subagents.backup.*"; \
	  else \
	    echo "Error: Failed to back up existing /usr/local/bin/subagents. Aborting installation to avoid data loss."; \
	    exit 1; \
	  fi; \
	fi
	sudo cp bin/subagents /usr/local/bin/subagents
	sudo chmod +x /usr/local/bin/subagents
	@echo "Installed subagents CLI to /usr/local/bin/subagents."
	@echo "Installation complete. Dotfile setup, .env, opencode config, ralph CLI, and subagents CLI are in place. Please run 'source ~/.zshenv' or restart your shell to apply changes."

clean:
	@echo "Removing dotfile backups (.zshrc, .env, ralph, subagents, AGENTS.md)..."
	@rm -f $${HOME}/.zshrc.backup.*
	@rm -f $${HOME}/.env.backup.*
	@rm -f /usr/local/bin/ralph.backup.*
	@rm -f /usr/local/bin/subagents.backup.*
	@rm -f $${HOME}/.config/opencode/AGENTS.md.backup.*
	@echo "Backup removal complete."
