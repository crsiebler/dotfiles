# Load the Docker aliases
if [ -f ~/.docker_aliases ]; then
	. ~/.docker_aliases
fi

# Load the Git aliases
if [ -f ~/.git_aliases ]; then
	. ~/.git_aliases
fi

# Load the Node aliases
if [ -f ~/.node_aliases ]; then
	. ~/.node_aliases
fi

# Load the Symfony aliases
if [ -f ~/.symfony_aliases ]; then
	. ~/.symfony_aliases
fi

# Load common aliases
if [ -f ~/.aliases ]; then
	. ~/.aliases
fi

export JAVA_HOME=/usr/bin/java
export LC_ALL=C.UTF-8
export PATH="$HOME/.local/bin:$PATH"