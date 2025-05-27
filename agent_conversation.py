import textwrap
from edsl import Agent, AgentList, Model, QuestionFreeText, QuestionYesNo
from conversation import Conversation

edsl_model = Model(model_name="google/gemma-2-9b-it", service_name='deep_infra')
max_turns = 20

def negotiation_agents():
    # putin = Agent(
    #     name = "Vladimir Putin",
    #     traits={
    #         "persona": "President of Russia, former intelligence officer",
    #         "leadership": "Authoritarian, strategic, and pragmatic",
    #         "negotiation": "Hardline, calculated and tactical",
    #         "military_policy": "Strong focus on military dominance and security",
    #         "economic_strategy": "Energy leverage, sanction resilience, and state-controlled economy",
    #         "communication_style": "Cold, calculated and propagandist",
    #         # "goal": "Minimise impact of western sanctions and improve diplomatic and economic ties with China to heral a new world order"
    #     }
    # )
    rice = Agent(
        name="Condoleezza Rice",
        traits = {
            "persona": "Former U.S. Secretary of State and National Security Advisor; Stanford professor and political scientist",
            "leadership": "Principled, composed under pressure, institutionally grounded",
            "economic_strategy": "Market-oriented with support for global liberal trade frameworks",
            "global_diplomacy": "Proponent of rules-based order, U.S. global leadership, multilateral engagement",
            "military_policy": "Believes in strong defense posture backed by diplomatic strategy; post-9/11 security coordination",
            "communication_style": "Disciplined, analytical, persuasive without inflammatory rhetoric",
            "goal": "Promote U.S. leadership through diplomacy, democratic values, and strategic alliances"
        }
    )


    xi = Agent(
        name = "Xi Jinping",
        traits={
            "persona": "President of China, chairman of communist party",
            "leadership": "Authoritarian, long-term strategist, nationalist",
            "economic_strategy": "State-controlled economy, tech-driven growth, BRI expansion",
            "global_diplomacy": "Soft power strategist, U.S. rival, Russia-China alliance builder",
            "military_policy": "Modernizes PLA, cyber warfare focus, South China sea expansion",
            "communication_style": "Diplomatic, calculated and propagandist",
            # "goal": "Minimize impacts of US tariff war with China by seeking new economic and diplomatic avenues in Russia"
        }
    )

    return AgentList([rice, xi])

agents = negotiation_agents()

# topic = "How Russia-China relationship need to grow to downplay all American Sanctions?"
topic = "How can China and US shape the world trade?"

    # "grounding_sources": [list of sources] (for example: URLs, title, quotes, news URLs, books etc)
start_statement = textwrap.dedent(
    """\
You are {{agent_name}}, engaging in a negotiation with {{other_agent_names}} on the topic: "{{topic}}".
Your goal is to propose a clear starting position, outline your priorities, and invite a collaborative resolution.
Avoid being combative; aim for mutual understanding an a potential deal.
Your output must be in a form of python dict:
{
    "Statement": "...",
    "grounding_sources": [
        {
            "title": "...",
            "type": "speech/article/News/Book/Quote",
            "url": "...",
            "quote": "...",
            "explanation": "Why it's relevant"
        }
    ]
}
Also the output should contain *ONLY* above format without any explanations.
    """
)
start_statement_question = QuestionFreeText(
    question_text=start_statement,
    question_name="dialogue",
)

next_statement = textwrap.dedent(
    """\
You are {{ agent_name }} engaged in a high level conversation with {{other_agent_names}} on Topic: "{{topic}}".
This is the conversation so far: 
{{ conversation }}

{% if round_message is not none %}
Round Info: {{ round_message }}
{% endif %}

Only YOU should speak now - continue the conversation from your side **only**. Do NOT simulate what the other person might say.

Based on your real world positions and past statements, respond as you would in real life.
What do you say next to move the discussion forward toward a resolution?
Your output must be in a form of python dict:
{
    "Statement": "..."
    "grounding_sources": [
        {
            "title": "...",
            "type": "speech/article/News/Book/Quote",
            "url": "...",
            "quote": "...",
            "explanation": "Why it's relevant"
        }
    ]
}
Also the output should contain *ONLY* above format without any explanations.
    """
)
next_statement_question = QuestionFreeText(
    question_text=next_statement,
    question_name="dialogue",
)

per_round_message_template = """
Round {{current_turn}} of {{max_turns}}.
{% if current_turn == 1 %}
Lay out your key concerns and priorities. Set the tone for negotiation.
{% elif current_turn == max_turns %}
This is the final round. Make or accept a concrete proposal to finalize the agreement.
{% elif current_turn >= max_turns - 2 %}
Time is short. Converge toward actionable solutions or compromises.
{% else %}
Build on what has been said. Move the negotiation forward constructively.
{% endif %}
"""

conversation = Conversation(
    agent_list=agents,
    start_statement_question=start_statement_question,
    next_statement_question=next_statement_question,
    max_turns=max_turns,
    verbose=True,
    default_model=edsl_model,
    topic=topic,
    per_round_message_template=per_round_message_template
)


conversation.converse()

# results = conversation.to_results()
# results.to_pandas().to_csv("grounded_output.csv", index=False)
