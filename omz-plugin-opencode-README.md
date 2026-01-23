# omz-plugin-opencode

oh-my-zsh aliases for common OpenCode CLI commands.

## Installation

### Oh My Zsh

1. Clone the repository:

```bash
git clone --depth=1 https://github.com/crsiebler/omz-plugin-opencode.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/opencode
```

2. Add it to your `~/.zshrc`:

```bash
plugins=(... opencode)
```

## Aliases

| Alias   | Command                    | Description                                 |
|---------|----------------------------|---------------------------------------------|
| op      | `opencode`                | Start OpenCode TUI                          |
| opw     | `opencode web`            | Start OpenCode web interface                  |
| opd     | `opencode --print-logs --log-level DEBUG` | Start OpenCode with debug logging enabled      |
| opc     | `opencode --continue`      | Continue last session                        |
| opcont  | `opencode --continue`      | Continue last session (alternative)           |
| ops     | `opencode session list`     | List all sessions                          |
| opsc    | `opencode --continue`      | Continue last session (short form)         |
| opa     | `opencode agent list`       | List all available agents                  |
| opac    | `opencode agent create`     | Create a new agent                        |
| opdebug | `opencode debug`           | Access debugging utilities                   |
| opdc    | `opencode debug config`    | Show resolved configuration                  |
| opds    | `opencode debug skill`     | List all available skills                  |
| opdp    | `opencode debug paths`     | Show global paths (data, config, cache)    |
| oprun   | `opencode run`            | Run OpenCode with a message                |
| opattach | `opencode attach`          | Attach to running OpenCode server          |
| opserve | `opencode serve`           | Start headless OpenCode server              |
| opacp   | `opencode acp`             | Start ACP (Agent Client Protocol) server  |
| opmcp   | `opencode mcp`             | Manage MCP (Model Context Protocol) servers  |
| opml    | `opencode models`           | List all available models                  |
| opstats | `opencode stats`           | Show token usage and cost statistics       |
| opauth  | `opencode auth`             | Manage credentials                         |
| opexp   | `opencode export`           | Export session data as JSON                |
| opimp   | `opencode import`           | Import session data from JSON file or URL   |
| opgh    | `opencode github`            | Manage GitHub agent                       |
| oppr    | `opencode pr`               | Fetch PR branch and run OpenCode           |
| opupgrade| `opencode upgrade`           | Upgrade OpenCode to latest version           |
| opuninstall| `opencode uninstall`         | Uninstall OpenCode and remove all files    |
| opcompletion| `opencode completion`       | Generate shell completion script             |

## Why `op` prefix?

The `op` prefix was chosen to avoid conflicts with:
- `oc` - OpenShift CLI (widely used container platform)
- `opc` - Oracle Cloud Infrastructure CLI
- `opcd` - Open On-Chip Debugger (embedded development)

The `op` prefix has minimal conflicts while maintaining a direct, intuitive relationship to "OpenCode".

## License

MIT License