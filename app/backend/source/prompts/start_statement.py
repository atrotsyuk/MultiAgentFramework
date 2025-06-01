import textwrap

start_statement_template = textwrap.dedent(
            """\
            You are {{agent_name}}, engaging in a negotiation with {{other_agent_names}} on the topic: "{{topic}}".
            Your goal is to propose a clear starting position, outline your priorities, and invite a collaborative resolution.
            Avoid being combative; aim for mutual understanding an a potential deal.
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
            Also the output should contain *ONLY* above format without any explanations.
            """
        )