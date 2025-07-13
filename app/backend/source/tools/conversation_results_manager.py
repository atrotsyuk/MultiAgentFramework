import math
import re
import ast
import os
import pandas as pd
from edsl import Results
from app.backend.source.tools.conversation_manager import ConversationManager
from app.backend.source.tools.agent_manager import agent_manager

class ConversationResultExtractor:
    def __init__(self, agent_uuids, topic, max_turns=3, results_per_page=10):
        self.agent_uuids = agent_uuids
        self.topic = topic
        self.max_turns = max_turns
        self.results_per_page = results_per_page
        self.res_arr = []
        self.conversation = None
        self.df = None

    def run_conversation(self):
        self.conversation_manager = ConversationManager(
            max_turns=self.max_turns,
            agent_uuids=self.agent_uuids,
            topic=self.topic
        )
        self.conversation = self.conversation_manager.start_conversation()

    def fetch_and_parse_results(self):
        total_pages = math.ceil(self.max_turns / self.results_per_page)
        results_on_last_page = (
            self.max_turns % self.results_per_page
            if self.max_turns % self.results_per_page != 0
            else self.results_per_page
        )

        for i in range(1, total_pages + 1):
            print(f"\nFetching page: {i}")
            page_size = results_on_last_page if i == total_pages else self.results_per_page
            results = Results.list(page=i, page_size=page_size, sort_ascending=False).fetch()

            for item in results:
                try:
                    iteration = item[0]['scenario']['index']
                    agent_name = item[0]['agent']['name']
                    response_raw = item[0]['answer']['dialogue']
                    cleaned_resp = re.sub(r"^```python|```$", "", response_raw.strip()).strip()
                    parsed_resp = ast.literal_eval(cleaned_resp)

                    self.res_arr.append({
                        'iteration': iteration,
                        'agent': agent_name,
                        'answer': parsed_resp['Statement'],
                        'sources': parsed_resp['grounding_sources']
                    })
                except Exception as e:
                    print(f"Failed to parse response: {e}")
                    iteration = item[0]['scenario']['index']
                    agent_name = item[0]['agent']['name']
                    response_raw = item[0]['answer']['dialogue']
                    parsed_resp = response_raw[10:-3]
                    self.res_arr.append({
                        'iteration': iteration,
                        'agent': agent_name,
                        'answer': parsed_resp,
                        'sources': ""
                    })
                    # continue

        self.df = pd.DataFrame(self.res_arr)
        self.df.sort_values(by="iteration", inplace=True)

    def save_to_csv(self, output_path=None):
        if self.df is None:
            raise ValueError("No results found. Run fetch_and_parse_results() first.")
        
        agent_list = agent_manager.get_agents_list()

        # agent_1_name = self.agent_params[0]['agent_name']
        # agent_2_name = self.agent_params[1]['agent_name']
        turns = self.max_turns

        base_directory_path = os.path.join("static")

        if not os.path.exists(base_directory_path):
            os.makedirs(base_directory_path, exist_ok = True)
        # save_to_folder = os.path.join("app", "backend", "static")

        if output_path is None:
            # output_path = f"output-{agent_1_name}_{agent_2_name}_{turns}.csv"
            output_path = f"output-{self.topic}_{turns}.csv"
        filename = os.path.join(base_directory_path, output_path)

        # filename = output_path or f'{save_to_folder}/output-{agent_1_name}_{agent_2_name}_{turns}.csv'
        self.df.to_csv(filename, index=False)
        print(f"\n✅ Results saved to {filename}")

    def get_results_df(self):
        return self.df.to_dict(orient="records")
