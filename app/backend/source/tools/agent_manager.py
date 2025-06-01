import ast
from edsl import Agent, AgentList
from backend.source.edsl_client.edsl_find_agent_traits import edsl_find_agent

class AgentManager:
    def __init__(self):
        pass

    def _create_agent_persona(self, agent_traits: dict) -> Agent:
        return Agent(
            name=agent_traits['name'],
            traits=agent_traits['traits']
        )

    def build_agents(self, agent_1: dict, agent_2: dict) -> AgentList:
        """
        Accepts two agent descriptors as dicts:
        {
            'agent_name': <str>,
            'agent_description': <str>
        }
        Returns an AgentList of EDSL Agent objects with extracted traits.
        """
        agent_1_traits_str = edsl_find_agent.find(agent_1['agent_name'], agent_1['agent_description'])
        agent_2_traits_str = edsl_find_agent.find(agent_2['agent_name'], agent_2['agent_description'])

        agent_1_traits = ast.literal_eval(agent_1_traits_str)
        agent_2_traits = ast.literal_eval(agent_2_traits_str)

        agent_obj_1 = self._create_agent_persona(agent_1_traits)
        agent_obj_2 = self._create_agent_persona(agent_2_traits)

        return AgentList([agent_obj_1, agent_obj_2])

agent_manager = AgentManager()







# from edsl import Agent, AgentList
# from get_agent_traits import find_agent_traits
# import ast

# def create_agent_persona(agent_traits):
#     agent = Agent(
#         name = agent_traits['name'],
#         traits = agent_traits['traits']
#     )
#     return agent


# def negotiation_agents(agent_1, agent_2):
#     '''
#     agent_1 and agent_2 are both dicts like:
#     agent_1 = {
#         'agent_name': <>,
#         'agent_description': <>
#     }
#     '''

#     agent_1_traits = find_agent_traits(agent_1['agent_name'], agent_1['agent_description'])
#     agent_2_traits = find_agent_traits(agent_2['agent_name'], agent_2['agent_description'])

#     agent_1_traits_json = ast.literal_eval(agent_1_traits)
#     agent_2_traits_json = ast.literal_eval(agent_2_traits)
#     agent_1 = create_agent_persona(agent_traits=agent_1_traits_json)
#     agent_2 = create_agent_persona(agent_traits=agent_2_traits_json)

#     return AgentList([agent_1, agent_2])
