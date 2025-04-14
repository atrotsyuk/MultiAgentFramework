from edsl import Results
from edsl import QuestionFreeText, QuestionYesNo

res_arr = ["9be1c970-349d-45cd-9ef0-2d1e91e3ae46",
           "28f286db-f922-467c-882d-01078e56eb62",
           "fb57ac14-d287-4573-89f2-df9bee94797b",
           "3af35edc-42de-4e75-83d9-5124aefa4c2f",
           "8b514837-c211-4d70-89b2-6a3c12a0616b",
           "2cddb6c9-fbad-4688-8fd5-27cb91fdbe6b",
           "620cdd16-a5ff-4d81-bbc7-f52432790ad0",
           "ad3c032c-9012-470c-8a53-3337abbd569b",
           "7d9e50c3-7d70-411a-9d0f-c67789f7ab1d",
           "30ff1d04-1e6e-47a4-a65c-4352d6b8dc7b",
           "a72344c7-5c7c-4c55-98d2-5d8b83709331",
           "3707881f-7fd0-4c79-9b1f-37cef9ee244e",
           "e2c02c61-deb1-432c-bcdb-535de6d2fd2b",
           "a9f8a05c-4358-445a-8269-f19de0776f16",
           "d3bbbee5-ed30-44f1-b946-a47df8658072"]

dialogue_list = []
for item in res_arr:
  res = Results.pull(item)
  dial = res.select("index", "agent_name", "dialogue")
  # dial.print(format="rich")
  dialogue_list.append(dial)


dl_2 = []
for item in dialogue_list:
  dl_2.append(
      {
          "index": item.data[0]["scenario.index"][0],
          "agent_name": item.data[1]["agent.agent_name"][0],
          "dialogue": item.data[2]["answer.dialogue"][0]
      }
  )

print(dl_2)

import pandas as pd
df = pd.DataFrame.from_records(dl_2, columns=['index', 'agent_name', 'dialogue'])
df.head()
df.to_csv('dialogue_gemma.csv', index=False)

q_deal = QuestionYesNo(
    question_text="""This was a negotiation: {{ transcript }}. 
                     Was a deal reached?
                    """,
    question_name="deal",
)

q_res_steps = QuestionFreeText(
    question_text="""This was a negotiation: {{ transcript }}. 
                     A deal was reached. what was agreed deal from the conversation.
                    """,
    question_name="resolution_reached",
)

survey = (
    q_deal.add_question(q_res_steps)
)

from edsl import Scenario
s = Scenario(
    {
        "num_agents": 2,
        "max_turns": 15,
        # "conversation_index": self.conversation_index,
        "transcript": str(dl_2),
        "number_of_agent_statements": 15,
    }
)
transcript_analysis = survey.by(s).run()
transcript_analysis.select("deal","resolution_reached").print(format="rich")

resolution_id = "ae7d038e-8864-4b61-aacd-5fa140eeb441"
resolution_res = Results.pull(resolution_id)
data_ = resolution_res.select("resolution_reached")
print(data_[0]['answer.resolution_reached'][0])
with open("resolution_reached.txt", "w") as f:
    f.write(data_[0]['answer.resolution_reached'][0])