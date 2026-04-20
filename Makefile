FILES = aliases/.aliases aliases/.docker_aliases aliases/.git_aliases aliases/.node_aliases aliases/.symfony_aliases zsh/.zshenv zsh/.zshrc

install:
	@if [ -f ~/.zshrc ]; then cp ~/.zshrc ~/.zshrc.backup.$$(date +%Y%m%d_%H%M%S); fi
	for file in $(FILES); do cp -f $$file ~/; done
	@mkdir -p $$HOME/.config/opencode/skills $$HOME/.config/opencode/agents $$HOME/.config/opencode/commands
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
	@if [ -f $$HOME/.config/opencode/opencode.json ]; then \
	  cp $$HOME/.config/opencode/opencode.json $$HOME/.config/opencode/opencode.json.backup.$$(date +%Y%m%d_%H%M%S); \
	  echo "Backed up existing opencode.json to .config/opencode/opencode.json.backup.*"; \
	fi
	cp ai/opencode/opencode.json $$HOME/.config/opencode/opencode.json
	@echo "Copied ai/opencode/opencode.json to $$HOME/.config/opencode/opencode.json."
	cp ai/ralph.md $$HOME/.config/opencode/ralph.md
	@echo "Copied ai/ralph.md to $$HOME/.config/opencode/ralph.md."
	@if [ -f $$HOME/.config/opencode/AGENTS.md ]; then \
	  cp $$HOME/.config/opencode/AGENTS.md $$HOME/.config/opencode/AGENTS.md.backup.$$(date +%Y%m%d_%H%M%S); \
	  echo "Backed up existing AGENTS.md to .config/opencode/AGENTS.md.backup.*"; \
	fi
	cp ai/opencode/AGENTS.md $$HOME/.config/opencode/AGENTS.md
	@echo "Copied ai/opencode/AGENTS.md to $$HOME/.config/opencode/AGENTS.md."
	@if [ -d $$HOME/.config/opencode/skills ] && [ "$$(ls -A $$HOME/.config/opencode/skills 2>/dev/null)" ]; then \
	  cp -R $$HOME/.config/opencode/skills $$HOME/.config/opencode/skills.backup.$$(date +%Y%m%d_%H%M%S); \
	  echo "Backed up existing skills to .config/opencode/skills.backup.*"; \
	fi
	cp -R ai/opencode/skills/. $$HOME/.config/opencode/skills/
	@echo "Copied ai/opencode/skills to $$HOME/.config/opencode/skills/."
	@if [ -d $$HOME/.config/opencode/agents ] && [ "$$(ls -A $$HOME/.config/opencode/agents 2>/dev/null)" ]; then \
	  cp -R $$HOME/.config/opencode/agents $$HOME/.config/opencode/agents.backup.$$(date +%Y%m%d_%H%M%S); \
	  echo "Backed up existing agents to .config/opencode/agents.backup.*"; \
	fi
	cp -R ai/opencode/agents/. $$HOME/.config/opencode/agents/
	@echo "Copied ai/opencode/agents to $$HOME/.config/opencode/agents/."
	@if [ -d $$HOME/.config/opencode/commands ] && [ "$$(ls -A $$HOME/.config/opencode/commands 2>/dev/null)" ]; then \
	  cp -R $$HOME/.config/opencode/commands $$HOME/.config/opencode/commands.backup.$$(date +%Y%m%d_%H%M%S); \
	  echo "Backed up existing commands to .config/opencode/commands.backup.*"; \
	fi
	cp -R ai/opencode/commands/. $$HOME/.config/opencode/commands/
	@echo "Copied ai/opencode/commands to $$HOME/.config/opencode/commands/."
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
	@echo "Installation complete. Dotfile setup, .env, opencode config, agents, commands, ralph CLI, and subagents CLI are in place. Please run 'source ~/.zshenv' or restart your shell to apply changes."

clean:
	@echo "Removing dotfile backups (.zshrc, .env, opencode.json, ralph, subagents, AGENTS.md, skills, agents, commands)..."
	@rm -f $${HOME}/.zshrc.backup.*
	@rm -f $${HOME}/.env.backup.*
	@rm -f $${HOME}/.config/opencode/opencode.json.backup.*
	@rm -f /usr/local/bin/ralph.backup.*
	@rm -f /usr/local/bin/subagents.backup.*
	@rm -f $${HOME}/.config/opencode/AGENTS.md.backup.*
	@rm -rf $${HOME}/.config/opencode/skills.backup.*
	@rm -rf $${HOME}/.config/opencode/agents.backup.*
	@rm -rf $${HOME}/.config/opencode/commands.backup.*
	@echo "Backup removal complete."
