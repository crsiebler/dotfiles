# dotfiles

A collection of configuration files for storing user preferences and preserving the state of a utility. Support for Zsh only.

## Setting Up

1. Copy the provided `.env.example` from this repository to your `$HOME` directory as `.env`, and fill in your own values:

   cp .env.example $HOME/.env
   # then edit $HOME/.env to add your secrets

2. The global opencode configuration, `opencode.json`, should be copied to `$HOME/.config/opencode/opencode.json`:

   mkdir -p $HOME/.config/opencode/
   cp opencode.json $HOME/.config/opencode/opencode.json

3. Run `make install` to copy all supported dotfiles to your home directory as usual.

4. **After installation:**
   - Open a new terminal, or manually run `source ~/.zshrc` to apply all settings and load environment variables from `$HOME/.env`.
   - Any changes to `$HOME/.env` require you to re-source it (`source ~/.env`) or start a new shell.

`make setup` will automate all these steps, backing up any existing files before overwriting them. Your secrets in `.env` will never be committed, and your configuration is backed up just like `.zshrc`.