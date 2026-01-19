FILES = .aliases .docker_aliases .git_aliases .node_aliases .symfony_aliases .zshenv .zshrc

install:
	@if [ -f ~/.zshrc ]; then cp ~/.zshrc ~/.zshrc.backup.$$(date +%Y%m%d_%H%M%S); fi
	for file in $(FILES); do cp -f $$file ~/; done
	@echo "Installation complete. Please run 'source ~/.zshenv' or restart your shell to apply changes."

dry-run:
	@echo "Would backup ~/.zshrc if it exists with timestamp"
	@echo "Would copy the following files to ~/ : $(FILES)"
	@echo "Would then print: 'Please run \"source ~/.zshenv\" or restart your shell to apply changes.'"