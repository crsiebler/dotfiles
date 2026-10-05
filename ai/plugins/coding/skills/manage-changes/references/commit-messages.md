# Commit messages

Use Conventional Commits 1.0.0 with these editorial constraints. Honor explicit
user and repository conventions, including mandatory scopes or narrower types.
The length, case and wrapping rules below are house style, not requirements of
the Conventional Commits specification.

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

- Use `feat` for new features, `fix` for bug fixes, `docs` for documentation only,
  `style` for formatting only, `refactor` for code changes without new features or
  fixes, `perf` for performance improvements, `test` for test changes, and `chore`
  for build processes, auxiliary tooling or dependency changes.
- Use an imperative, present-tense description starting with a lowercase letter
  and no trailing period. Limit the entire subject, including scope and `!`, to
  50 characters. Choose a concise scope describing the affected component.
- Wrap body and footer text at 72 characters. Separate subject, optional body
  and optional footer section with exactly one blank line; omit empty sections.
- For breaking changes, place `!` immediately after the type or scope and start
  the footer section with `BREAKING CHANGE:`, explaining the incompatible change
  and required migration. Do not infer breakage merely from a large diff.
- `feat` and `fix` conventionally signal minor and patch releases; breaking
  changes signal major releases. Actual version calculation depends on the
  project's release tooling/configuration. Other types have no inherent bump.

Draft from the intended diff or supplied description, preserving the actual
behavior and purpose. For complex changes, explain motivation and consequences
in the body. Never invent issue numbers, validation or breaking changes.

When asked only to generate a message, return only the final message in a code
block. When validating, confirm a valid message; otherwise identify the specific
violations and provide a corrected code block. Neither mode authorizes committing.
During an authorized shipping workflow, include the message in the commit preview
and retain required validation and delivery reporting.

For squash merges, the final squash commit must follow the same convention if
release tooling reads the target branch's history; check the PR title and final
message policy rather than relying on feature-branch messages alone.

Reference: [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
