if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

export ZSH="${ZSH:-$HOME/.oh-my-zsh}"

ZSH_THEME="powerlevel10k/powerlevel10k"

plugins=(
    alias-finder
    autopep8
    aws
    brew
    bun
    conda
    docker
    docker-compose
    git
    gh
    opencode
    kubectl
    nvm
    python
    urltools
    wd
    yarn
    you-should-use
    zsh-autosuggestions
    zsh-syntax-highlighting
)

[[ -d "$HOME/.docker/completions" ]] && \
  fpath=("$HOME/.docker/completions" $fpath)

if [[ -r "$ZSH/oh-my-zsh.sh" ]]; then
  source "$ZSH/oh-my-zsh.sh"
else
  print -u2 "Warning: Oh My Zsh is not installed at $ZSH"
  autoload -Uz compinit
  compinit
fi

if [[ -z ${SSH_CONNECTION:-} ]] && (( $+commands[code] )); then
  export EDITOR="code --wait"
elif (( $+commands[nvim] )); then
  export EDITOR="nvim"
else
  export EDITOR="vim"
fi
export VISUAL="$EDITOR"

for alias_file in \
  "$HOME/.docker_aliases" \
  "$HOME/.git_aliases" \
  "$HOME/.node_aliases" \
  "$HOME/.symfony_aliases" \
  "$HOME/.aliases"; do
  [[ -r $alias_file ]] && source "$alias_file"
done
unset alias_file

[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

export NVM_DIR="$HOME/.nvm"

export BUN_INSTALL="$HOME/.bun"
typeset -U path PATH
[[ -d "$BUN_INSTALL/bin" ]] && path=("$BUN_INSTALL/bin" $path)

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
if [[ -x /opt/anaconda3/bin/conda ]]; then
  __conda_setup="$(/opt/anaconda3/bin/conda shell.zsh hook 2>/dev/null)"
  if [[ $? -eq 0 ]]; then
    eval "$__conda_setup"
  elif [[ -r /opt/anaconda3/etc/profile.d/conda.sh ]]; then
    source /opt/anaconda3/etc/profile.d/conda.sh
  fi
  unset __conda_setup
fi
# <<< conda initialize <<<

# opencode
[[ -d "$HOME/.opencode/bin" ]] && path=("$HOME/.opencode/bin" $path)

[[ -d /Library/TeX/texbin ]] && path=(/Library/TeX/texbin $path)

# >>> railway initialize >>>
source "$HOME/.railway/env"
# <<< railway initialize <<<

if [[ -r "$HOME/.env" ]]; then
  source "$HOME/.env"
fi
