import textwrap
from edsl import Model, QuestionFreeText, Scenario
import re

edsl_model = Model(model_name="google/gemma-2-9b-it", service_name='deep_infra')

def find_agent_traits(agent_name, agent_description):
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
{
    "name" = "Vladimir Putin",
    "traits"={
        "persona": "President of Russia, former intelligence officer",
        "leadership": "Authoritarian, strategic, and pragmatic",
        "negotiation": "Hardline, calculated and tactical",
        "military_policy": "Strong focus on military dominance and security",
        "economic_strategy": "Energy leverage, sanction resilience, and state-controlled economy",
        "communication_style": "Cold, calculated and propagandist",
        "goal": "Minimise impact of western sanctions and improve diplomatic and economic ties with China to heral a new world order"
    }
},
{
    "name"="Condoleezza Rice",
    "traits" = {
        "persona": "Former U.S. Secretary of State and National Security Advisor; Stanford professor and political scientist",
        "leadership": "Principled, composed under pressure, institutionally grounded",
        "economic_strategy": "Market-oriented with support for global liberal trade frameworks",
        "global_diplomacy": "Proponent of rules-based order, U.S. global leadership, multilateral engagement",
        "military_policy": "Believes in strong defense posture backed by diplomatic strategy; post-9/11 security coordination",
        "communication_style": "Disciplined, analytical, persuasive without inflammatory rhetoric",
        "goal": "Promote U.S. leadership through diplomacy, democratic values, and strategic alliances"
    }
},
{
    "name" = "Xi Jinping",
    "traits"={
        "persona": "President of China, chairman of communist party",
        "leadership": "Authoritarian, long-term strategist, nationalist",
        "economic_strategy": "State-controlled economy, tech-driven growth, BRI expansion",
        "global_diplomacy": "Soft power strategist, U.S. rival, Russia-China alliance builder",
        "military_policy": "Modernizes PLA, cyber warfare focus, South China sea expansion",
        "communication_style": "Diplomatic, calculated and propagandist",
        # "goal": "Minimize impacts of US tariff war with China by seeking new economic and diplomatic avenues in Russia"
    }
}
"""
    )
    find_agent = QuestionFreeText(
        question_text = create_agent_text,
        question_name = "create_agent_q"
    )

    find_agent_sc = Scenario(
        {
            "agent_name": agent_name,
            "agent_description": agent_description
        }
    )

    resp = find_agent.by(find_agent_sc).by(edsl_model).run()
    traits = resp[0]["answer"]["create_agent_q"]
    cleaned_resp = re.sub(r"^```python|```$", "", traits.strip()).strip()
    # print(f"--------agent {agent_name} traits------:\n {cleaned_resp}\n")
    return cleaned_resp

# find_agent_traits("Narendra Modi", "Prime Minister of India")
# find_agent_traits("Sashi Tharoor", "MP from Kerala, Senior member of Congress")