import textwrap

create_agent_text = textwrap.dedent(
        """\
Create an agent persona for {{agent_name}} given agent description as {{agent_description}}.\
The output must be in a form of python dict:
{
    "name": agent_name,
    "traits": {
        "persona": "...",
        "leadership": "...",
        "negotiation": "...",
        "military_policy": "...",
        "economic_strategy": "...",
        "communication_style": "...",
        "goal": Optional,
        "past_achievements": "..."
    }
}

Examples:
{{example_traits}}
"""
)