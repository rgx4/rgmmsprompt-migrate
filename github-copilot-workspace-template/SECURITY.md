# Security

This template contains no credentials, MCP servers, deployment automation, or application-specific secrets.

## Reporting a vulnerability

Use the security-reporting mechanism configured by the repository that publishes this template. Do not disclose exploitable vulnerabilities in public issues when a private reporting channel is available.

## Adopting this template

- Never place credentials, tokens, private keys, customer data, or secret values in Copilot instructions, skills, agents, `WORKSPACE.md`, or prompts.
- Treat `/add-dir` as a trust decision because added roots can contribute trusted agents and skills.
- Review child-repository agents and skills before loading repositories you do not trust.
- Keep destructive commands subject to normal Copilot permission prompts and repository-specific policy.
- Configure MCP only after reviewing the external system, exposed tools, authentication, and data boundary.
- Keep repository/organization branch protection, CI, code review, and secret-scanning controls in place; natural-language agent guidance is not a substitute for them.
