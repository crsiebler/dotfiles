# Environment shared by interactive and non-interactive Zsh processes.
if [[ -z ${JAVA_HOME:-} && -x /usr/libexec/java_home ]]; then
  java_home="$(/usr/libexec/java_home 2>/dev/null)"
  [[ -n $java_home ]] && export JAVA_HOME="$java_home"
  unset java_home
fi

export LANG="${LANG:-en_US.UTF-8}"

typeset -U path PATH
[[ -d "$HOME/.local/bin" ]] && path=("$HOME/.local/bin" $path)
