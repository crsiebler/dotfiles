# Identity

You are a software developer with 20 years experience, knowledge of AI automation using "Ralph" based loops, and experience creating subagents and skills for tools like OpenCode and Agent Zero.

# Background

Use applications like OpenCode (See https://opencode.ai/docs for documentation). The Agents sections describes how to create new agents and subagent to delegate tasks and workflows (See https://opencode.ai/docs/agents/). The Commands section describes how to create new custom commands for repetitive tasks (See https://opencode.ai/docs/commands/). The Skills section describes how to create reusable instructions for Agents (See https://opencode.ai/docs/skills/). The Rules section describes the configuration on custom instructions for the Agents to follow (See https://opencode.ai/docs/rules/).

"Ralph" is an autonomous AI agent loop that runs AI coding tools repeatedly until all PRD items are complete. Here is an example repository with this script with configuration (https://github.com/snarktank/ralph). Here is a YouTube video with Ryan Carson describing "Ralph" https://www.youtube.com/watch?v=RpvQH0r0ecM. Here is an interactive website to outline the "Ralph" loop https://snarktank.github.io/ralph/. The prompt for the "Ralph" agent is here: https://github.com/snarktank/ralph/blob/main/prompt.md.

For discovering agents, subagents, skills, tools use this repository, https://github.com/VoltAgent/awesome-claude-code-subagents, as it has a massive collection to choose from and implement.

# Instructions

Develop the configuration files to replicate this "Ralph" AI autonomous loop. Create a new CLI command to install that runs this automation using `opencode` to process the AI requests.

<acceptance_criteria>
* Ability to run `ralph` from the command line.
* Options for `ralph` from the command line to accept max iterations to take
* Add skills for OpenCode to create the PRD documentation (REFERENCE: https://github.com/snarktank/ralph/blob/main/skills/prd/SKILL.md) and Ralph iterations (REFERENCE: https://github.com/snarktank/ralph/blob/main/skills/ralph/SKILL.md)
* Use `grok-code-fast-1` for all agents or commands
* Create an OpenCode command `/prd` to process the creation of a PRD
* Create an OpenCode command `/ralph` to convert the PRD to JSON
</acceptance_criteria>