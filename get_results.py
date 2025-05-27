from edsl import Results
# from agent_conversation import max_turns
import pandas as pd
import json
import math
import re
import ast

max_turns = 20
results_per_page = 10
total_pages = math.ceil(max_turns / results_per_page)
results_on_last_page = (max_turns % results_per_page) if (max_turns % results_per_page != 0) else results_per_page

res_arr = []

i = 1
while(i <= total_pages):
    print(f"\npage: {i}")
    if i == total_pages:
        results_per_page = results_on_last_page
    results = Results.list(page=i, page_size = results_per_page, sort_ascending=False).fetch()
    
    for j, item in enumerate(results):
        item_dict = {}

        item_dict['iteration'] = item[0]['scenario']['index']
        item_dict['agent'] = item[0]['agent']['name']
        print(f"Agent Name: {item_dict['agent']}")

        try:
            # resp = item[0]['answer']['dialogue'][10:-3]
            # print(f"\nagent_resp: {resp}")
            # json_answer = json.loads(resp)

            resp = item[0]['answer']['dialogue']
            cleaned_resp = re.sub(r"^```python|```$", "", resp.strip()).strip()
            json_answer = ast.literal_eval(cleaned_resp)

            item_dict['answer'] = json_answer["Statement"]
            item_dict['sources'] = json_answer['grounding_sources']

            res_arr.append(item_dict)
        except Exception as e:
            # print(f"Error in page- {i}, result- {j+1}: {e}")
            print(f"Parsing Response Failed: {e}")
            continue

    i += 1



df = pd.DataFrame(res_arr)
df.sort_values(by="iteration", inplace=True)
# print(df.head())
df.to_csv('output-rice-xi_1.csv', index=False)