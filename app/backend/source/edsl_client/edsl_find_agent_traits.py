import re
from edsl import Model, QuestionFreeText, Scenario
from backend.source.prompts.find_agent_traits import create_agent_text
from backend.source.examples.traits import example_traits

class EdslAgent:
    def __init__(self, model_name="google/gemma-2-9b-it", service_name=None, examples=None):
        self.model = Model(model_name=model_name, service_name=service_name) if service_name else Model(model_name=model_name)
        self.create_agent_text = create_agent_text
        self.examples = examples or example_traits

    def find(self, agent_name: str, agent_description: str) -> str:
        question = QuestionFreeText(
            question_text=self.create_agent_text,
            question_name="create_agent_q"
        )

        scenario = Scenario({
            "agent_name": agent_name,
            "agent_description": agent_description,
            "example_trais": self.examples
        })

        response = question.by(scenario).by(self.model).run()
        traits_code = response[0]["answer"]["create_agent_q"]
        cleaned = re.sub(r"^```python|```$", "", traits_code.strip()).strip()

        return cleaned

edsl_find_agent = EdslAgent()






# import textwrap
# from edsl import Model, QuestionFreeText, Scenario
# import re

# from examples.traits import example_traits

# from prompts.find_agent_traits import create_agent_text

# # edsl_model = Model(model_name="google/gemma-2-9b-it", service_name='deep_infra')
# edsl_model = Model(model_name="google/gemma-2-9b-it")


# def find_agent_traits(agent_name, agent_description, examples= example_traits):
#     create_agent_text = create_agent_text
#     find_agent = QuestionFreeText(
#         question_text = create_agent_text,
#         question_name = "create_agent_q"
#     )

#     find_agent_sc = Scenario(
#         {
#             "agent_name": agent_name,
#             "agent_description": agent_description,
#             "example_trais": example_traits
#         }
#     )

#     resp = find_agent.by(find_agent_sc).by(edsl_model).run()
#     traits = resp[0]["answer"]["create_agent_q"]
#     cleaned_resp = re.sub(r"^```python|```$", "", traits.strip()).strip()
#     # print(f"--------agent {agent_name} traits------:\n {cleaned_resp}\n")
#     return cleaned_resp

# # find_agent_traits("Narendra Modi", "Prime Minister of India")
# # find_agent_traits("Sashi Tharoor", "MP from Kerala, Senior member of Congress")