per_round_message_template = """
        Round {{current_turn}} of {{max_turns}}.
        {% if current_turn == 1 %}
        Lay out your key concerns and priorities. Set the tone for negotiation.
        {% elif current_turn == max_turns %}
        This is the final round. Make or accept a concrete proposal to finalize the agreement.
        {% elif current_turn >= max_turns - 2 %}
        Time is short. Converge toward actionable solutions or compromises.
        {% else %}
        Build on what has been said. Move the negotiation forward constructively.
        {% endif %}
        """