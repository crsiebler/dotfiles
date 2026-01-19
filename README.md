# dotfiles

A collection of configuration files for storing user preferences and preserving the state of a utility. Support for Zsh only.

## Setting Up

Run `make install` to copy the configuration files (including .zshrc with aliases sourcing) to your user profile.

After installation, you must restart your shell or manually run `source ~/.zshrc` for the new aliases and configuration changes to take effect. The Makefile's source command runs in a separate process and won't update your current shell session automatically.
