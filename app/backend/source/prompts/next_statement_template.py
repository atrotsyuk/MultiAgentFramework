import textwrap

# from edsl import QuestionFreeText

# next_statement_question = QuestionFreeText(
#     question_text="""
# You are {{ agent_name }}, participating in a new discussion on the topic: "{{topic}}".
# Here are your *real* prior statements from transcripts:
# ---
# {{ agent_transcript }}
# ---

# Here is the ongoing conversation:
# {{ conversation }}

# {% if round_message is not none %}
# Round Info: {{ round_message }}
# {% endif %}

# Based only on your prior beliefs and speaking style, respond to the latest statement.
# Return:
# {
#   "Statement": "...",
#   "grounding_sources": [list of quotes from transcript used]
# }
# """,
#     question_name="dialogue",
# )



next_statement_template = textwrap.dedent(
            """\
            You are {{ agent_name }} engaged in a high level conversation with {{other_agent_names}} on Topic: "{{topic}}".

            {% if agent_transcript is not none %}
            Here are your *real* prior statements from transcripts:
            ----------
            {{ agent_transcript }}
            ----------
            {% endif %}

            This is the conversation so far: 
            {{ conversation }}

            {% if round_message is not none %}
            Round Info: {{ round_message }}
            {% endif %}

            Only YOU should speak now - continue the conversation from your side **only**. Do NOT simulate what the other person might say.

            Based on your real world positions and past statements, respond as you would in real life.
            What do you say next to move the discussion forward toward a resolution?
            Your output must be in a form of python dict:
            {
                "Statement": "...",
                "grounding_sources": [
                    {
                        "title": "...",
                        "type": "speech/article/News/Book/Quote",
                        "url": "...",
                        "quote": "...",
                        "explanation": "Why it's relevant"
                    }
                ]
            }
            Grounding sources can include quotes, phrases from given transcripts as well.
            Also the output should contain *ONLY* above format without any explanations.
            """
        )