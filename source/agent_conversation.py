import textwrap
from edsl import Model, QuestionFreeText
from conversation import Conversation

from create_agents import negotiation_agents

edsl_model = Model(model_name="google/gemma-2-9b-it", service_name='deep_infra')

max_turns = int(input("Enter Max conversation turns:\t"))
agent_1_name = input("Name of first agent:\t")
agent_1_desription = input("Description of first agent:\t")
agent_2_name = input("Name of second agent:\t")
agent_2_desription = input("Description of second agent:\t")
topic = input("Topic on which agents should converse:\t")
print("\n")

agent_1 = {"agent_name": agent_1_name, "agent_description": agent_1_desription}
agent_2 = {"agent_name": agent_2_name, "agent_description": agent_2_desription}

print("-----Creating Agent Personas------\n")
agents = negotiation_agents(agent_1, agent_2)
print("-----Agent Personas Created")

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