import math
import re
import ast
import os
import pandas as pd
from edsl import Results
from backend.source.tools.conversation_manager import ConversationManager

class ConversationResultExtractor:
    def __init__(self, agent_params, topic, max_turns=3, results_per_page=10):
        self.agent_params = agent_params
        self.topic = topic
        self.max_turns = max_turns
        self.results_per_page = results_per_page
        self.res_arr = []
        self.conversation = None
        self.df = None

    def run_conversation(self):
        self.conversation_manager = ConversationManager(
            max_turns=self.max_turns,
            agent_params=self.agent_params,
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
                    continue

        self.df = pd.DataFrame(self.res_arr)
        self.df.sort_values(by="iteration", inplace=True)

    def save_to_csv(self, output_path=None):
        if self.df is None:
            raise ValueError("No results found. Run fetch_and_parse_results() first.")

        agent_1_name = self.agent_params[0]['agent_name']
        agent_2_name = self.agent_params[1]['agent_name']
        turns = self.max_turns

        base_directory_path = os.path.join("backend", "static")

        if not os.path.exists(base_directory_path):
            os.makedirs(base_directory_path, exist_ok = True)
        # save_to_folder = os.path.join("app", "backend", "static")

        if output_path is None:
            output_path = f"output-{agent_1_name}_{agent_2_name}_{turns}.csv"
        filename = os.path.join(base_directory_path, output_path)

        # filename = output_path or f'{save_to_folder}/output-{agent_1_name}_{agent_2_name}_{turns}.csv'
        self.df.to_csv(filename, index=False)
        print(f"\n✅ Results saved to {filename}")

    def get_results_df(self):
        return self.df.to_dict(orient="records")




# from edsl import Results
# # from agent_conversation import max_turns, agent_1_name, agent_2_name
# from app.backend.source.tools.conversation_manager import ConversationManager
# import pandas as pd
# import math
# import re
# import ast

# max_turns = 3
# agent_traits = [
#     {
#         "agent_name": "Narendra Modi",
#         "agent_description": "Prime Minister Of India"
#     },
#     {
#         "agent_name": "Donald Trump",
#         "agent_description": "President of USA"
#     }
# ]
# topic = "Should India lower its Tarriffs over USA?"

# conversation_manager = ConversationManager(max_turns=max_turns, agent_params=agent_traits, topic=topic)

# conversation = conversation_manager.start_conversation()

# results_per_page = 10
# total_pages = math.ceil(conversation.max_turns / results_per_page)
# results_on_last_page = (conversation.max_turns % results_per_page) if (conversation.max_turns % results_per_page != 0) else results_per_page

# res_arr = []

# i = 1
# while(i <= total_pages):
#     print(f"\npage: {i}")
#     if i == total_pages:
#         results_per_page = results_on_last_page
#     results = Results.list(page=i, page_size = results_per_page, sort_ascending=False).fetch()
    
#     for j, item in enumerate(results):
#         item_dict = {}

#         item_dict['iteration'] = item[0]['scenario']['index']
#         item_dict['agent'] = item[0]['agent']['name']
#         print(f"Agent Name: {item_dict['agent']}")

#         try:
#             resp = item[0]['answer']['dialogue']
#             cleaned_resp = re.sub(r"^```python|```$", "", resp.strip()).strip()
#             json_answer = ast.literal_eval(cleaned_resp)

#             item_dict['answer'] = json_answer["Statement"]
#             item_dict['sources'] = json_answer['grounding_sources']

#             res_arr.append(item_dict)
#         except Exception as e:
#             print(f"Parsing Response Failed: {e}")
#             continue

#     i += 1



# df = pd.DataFrame(res_arr)
# df.sort_values(by="iteration", inplace=True)
# # print(df.head())

# agent_1_name = conversation_manager.agent_params[0]['agent_name']
# agent_2_name = conversation_manager.agent_params[1]['agent_name']
# turns = conversation_manager.turns

# df.to_csv(f'output-{agent_1_name}_{agent_2_name}_{turns}.csv', index=False)