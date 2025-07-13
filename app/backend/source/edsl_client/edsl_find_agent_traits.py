import re
# import ast
from edsl import Model, QuestionFreeText, Scenario
from app.backend.source.prompts.find_agent_traits import create_agent_text
from app.backend.source.examples.traits import example_traits

class EdslAgent:
    def __init__(self, model_name="google/gemma-2-9b-it", service_name=None, examples=None):
        self.model = Model(model_name=model_name, service_name=service_name) if service_name else Model(model_name=model_name)
        self.create_agent_text = create_agent_text
        self.examples = examples or example_traits

    def extract_dict_from_code_block(self, code_str: str) -> dict:
        # Step 1: Remove ```python ... ``` code block
        code_cleaned = re.sub(r"^```(?:python)?\s*|\s*```$", "", code_str.strip())
        # print(code_cleaned)

        # Step 2: Extract dict portion from 'var = {...}' format
        match = re.search(r"=\s*(\{.*\})\s*$", code_cleaned, re.DOTALL)
        if match:
            dict_str = match.group(1)
        else:
            dict_str = code_cleaned  # fallback if it's already just a dict

        # print(dict_str)
        return dict_str

    def find(self, agent_name: str, agent_description: str) -> str:
        print(f"Finding traits for agent: {agent_name}")
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
        try:
            cleaned = self.extract_dict_from_code_block(traits_code)
        except Exception as e:
          print(f"Fetching agent {agent_name} failed")
          cleaned = str({"name": agent_name, "traits": {"persona": agent_description}})
        finally:
          return cleaned

edsl_find_agent = EdslAgent()
