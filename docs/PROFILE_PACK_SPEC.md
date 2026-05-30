# AgentFit Profile Pack Spec

## Purpose

A Profile Pack is a portable configuration that tells an AI agent how to adapt to a user, device, or task.

Profile Packs are meant to be shared like `SKILLS.md`, `AGENTS.md`, or project handoff files.

## Design principles

1. Human-readable first.
2. Machine-readable second.
3. Safe to share by default.
4. Private data must be redacted.
5. User must preview before import.
6. Imported packs should be customizable.

## Recommended formats

AgentFit should support:

- `.md` profile cards
- `.json` profile packs

## Markdown profile card

A Markdown card is best for humans and agent prompts.

Example:

```markdown
# AgentFit Profile Card

## User Style
- Skill level: beginner
- Preferred guidance: step_by_step
- Risk tolerance: low
- Privacy preference: high

## Agent Rules
- Ask before destructive actions.
- Verify before claiming success.
- Prefer reversible operations.
```

## JSON profile pack

A JSON pack is best for import/export.

Example:

```json
{
  "pack_name": "beginner-raspberry-pi-builder",
  "version": "0.1.0",
  "safe_to_share": true,
  "profile": {
    "skill_level": "beginner",
    "preferred_style": "step_by_step",
    "risk_tolerance": "low",
    "privacy_preference": "high"
  }
}
```

## Do not include

Shared packs should not include private credentials, private project history, personal documents, tokens, home network details, or private device identifiers.

## Good pack categories

- Beginner Coding Pack
- Raspberry Pi Homelab Pack
- Obsidian Knowledge Base Pack
- Local AI Privacy Pack
- Agent Debugging Pack
- Writer Pack
- Hardware Project Pack
