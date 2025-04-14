# import sqlite3
from edsl import Agent, AgentList, Model, QuestionFreeText, QuestionYesNo
from conversation import Conversation

# Load Expected Parrot Model
# edsl_model = Model(model_name="meta-llama/Llama-3.2-1B-Instruct", service_name='deep_infra')
edsl_model = Model(model_name="google/gemma-2-9b-it", service_name='deep_infra')

def negotiation_agents():
    putin = Agent(
        name="Vladimir Putin",
        traits={
            "persona": "President of Russia, former intelligence officer",
            "leadership": "Authoritarian, strategic, and pragmatic",
            "negotiation": "Hardline, calculated, and tactical",
            "military_policy": "Strong focus on military dominance and security",
            "economic_strategy": "Energy leverage, sanctions resilience, and state-controlled economy",
            "communication_style": "Cold, calculated, and propagandist",
            # "goal": "Minimize impacts of western sanctions and improve diplomatic and economic ties with China to herald a new world order",
        },
    )
    xi = Agent(
        name="Xi Jinping",
        traits={
            "persona": "President of China, Chairman of the Communist Party",
            "leadership": "Authoritarian, long-term strategist, nationalist",
            "economic_strategy": "State-controlled economy, tech-driven growth, BRI expansion",
            "global_diplomacy": "Soft power strategist, U.S. rival, Russia-China alliance builder",
            "military_policy": "Modernizes PLA, cyber warfare focus, South China Sea expansion",
            "communication_style": "Diplomatic, calculated, and propagandist",
            # "goal": "Minimize impacts of US Tariff war with China by seeking new economic and diplomatic avenues in Russia",
        },
    )
    return AgentList([putin, xi])

agents = negotiation_agents()
topic = "Will global tariffs make America's economy stronger?"

per_round_message_template = """
Round {{ current_turn }} of {{ max_turns }}.

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


# Define the conversation
conversation = Conversation(
    agent_list=agents,
    max_turns=15,
    verbose=True,
    default_model=edsl_model,
    topic = topic,
    per_round_message_template=per_round_message_template
)

# Run the conversation and store results in SQLite
conversation.converse()
results = conversation.to_results()

# Print conversation results
results.select("index", "agent_name", "dialogue").print(format="rich")
