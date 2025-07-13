from typing import List
from edsl import Model, QuestionFreeText, Agent, AgentList

from source.edsl_client.edsl_conversation import Conversation
from source.tools.agent_manager import agent_manager
from source.prompts import start_statement, next_statement_template, per_round_message_template
from source.utils import load_all_transcripts

class ConversationManager:
    def __init__(self, max_turns: int, agent_uuids: List[str], topic: str, model_name="google/gemma-2-9b-it", service_name="deep_infra"):
        self.model = Model(model_name=model_name, service_name=service_name)

        self.turns = max_turns
        self.agent_uuids = agent_uuids
        self.topic = topic

        self.start_statement_template = start_statement.start_statement_template

        self.next_statement_template = next_statement_template.next_statement_template

        self.per_round_message_template = per_round_message_template.per_round_message_template

        self.agent_transcript = load_all_transcripts()


    def start_conversation(
        self,
        verbose: bool = True
    ):
        
        # print("-----Creating Agent Personas------\n")
        # agents = agent_manager.build_agents(
        #     agent_1=self.agent_params[0],
        #     agent_2=self.agent_params[1]
        # )
        # print("-----Agent Personas Created\n")
        agents_l = []
        for item in agent_manager.get_agents_list():
            # print(item)
            if item['uuid'] in self.agent_uuids:
                # agents_l.append({'name': item['name'], 'traits': item['traits']})
                edsl_agent = Agent(name=item['name'], traits=item['traits'])
                print(edsl_agent)
                agents_l.append(edsl_agent)
        agents = AgentList(agents_l)
        # print(agents)

        start_question = QuestionFreeText(
            question_text=self.start_statement_template,
            question_name="dialogue",
        )

        next_question = QuestionFreeText(
            question_text=self.next_statement_template,
            question_name="dialogue",
        )

        conversation = Conversation(
            agent_list=agents,
            start_statement_question=start_question,
            next_statement_question=next_question,
            max_turns=self.turns,
            verbose=verbose,
            default_model=self.model,
            topic=self.topic,
            per_round_message_template=self.per_round_message_template,
            transcript=self.agent_transcript
        )

        print("starting Conversation-------------")
        conversation.converse()
        return conversation  # Optional: return to access results after
