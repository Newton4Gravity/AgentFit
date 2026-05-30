from agentfit.schemas import UserProfile


def export_profile_card(profile: UserProfile) -> str:
    """
    Export a sanitized Markdown profile card.

    This is meant to be shared with friends or imported into another agent system.
    It should include useful calibration behavior without exposing private history,
    file paths, project secrets, account details, or sensitive personal information.
    """

    display_name = profile.display_name or "Shared User"

    return f"""# AgentFit Profile Card

## Profile

- Name: {display_name}
- Skill level: {profile.skill_level.value}
- Preferred style: {profile.preferred_style.value}
- Risk tolerance: {profile.risk_tolerance.value}
- Privacy preference: {profile.privacy_preference.value}
- Prefers open source: {str(profile.prefers_open_source).lower()}
- Prefers local-first: {str(profile.prefers_local_first).lower()}
- Likes Markdown: {str(profile.likes_markdown).lower()}
- Wants full code: {str(profile.wants_full_code).lower()}
- Project anchor mode: {str(profile.project_anchor_mode).lower()}

## Agent Behavior Rules

- Match the user's skill level.
- Use the preferred explanation style.
- Ask before destructive or irreversible actions.
- Verify before claiming success.
- Separate verified facts from assumptions.
- Prefer safe, reversible operations.
- Avoid exposing unnecessary private data.
- Use local-first workflows when privacy preference is high.

## Sharing Safety

This profile card is intended to be safe to share.

Review the exported card before sending it to someone else. Remove private paths, private project details, account details, and personal history.

## Suggested Use

Paste this card into an agent setup prompt or import it into an AgentFit-compatible tool.
"""
