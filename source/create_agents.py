from edsl import Agent, AgentList
from get_agent_traits import find_agent_traits
import ast

def create_agent_persona(agent_traits):
    agent = Agent(
        name = agent_traits['name'],
        traits = agent_traits['traits']
    )
    return agent


def negotiation_agents(agent_1, agent_2):
    '''
    agent_1 and agent_2 are both dicts like:
    agent_1 = {
        'agent_name': <>,
        'agent_description': <>
    }
    '''

    agent_1_traits = find_agent_traits(agent_1['agent_name'], agent_1['agent_description'])
    agent_2_traits = find_agent_traits(agent_2['agent_name'], agent_2['agent_description'])

    agent_1_traits_json = ast.literal_eval(agent_1_traits)
    agent_2_traits_json = ast.literal_eval(agent_2_traits)
    agent_1 = create_agent_persona(agent_traits=agent_1_traits_json)
    agent_2 = create_agent_persona(agent_traits=agent_2_traits_json)

    return AgentList([agent_1, agent_2])
