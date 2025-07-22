import ast
from edsl import Agent, AgentList
from app.backend.source.edsl_client.edsl_find_agent_traits import edsl_find_agent
from typing import List, Dict
import uuid
import os
import json
from pathlib import Path

class AgentManager:
    def __init__(self):
        self.agents_list = {}

    def _create_agent_persona(self, agent_traits: dict) -> Agent:
        return Agent(
            name=agent_traits['name'],
            traits=agent_traits['traits']
        )

    def build_agents(self, agent_dict: List[Dict[str, str]]) -> AgentList:
        """
        Accepts two agent descriptors as dicts:
        {
            'agent_name': <str>,
            'agent_description': <str>
        }
        Returns an AgentList of EDSL Agent objects with extracted traits.
        """

        resp = []
        for agent in agent_dict:
            print(f"Creating agent persona for {agent['agent_name']}")
            agent_1_traits_str = edsl_find_agent.find(agent['agent_name'], agent['agent_description'])
            print(f"found traits for agent {agent['agent_name']}")

            agent_1_traits = ast.literal_eval(agent_1_traits_str)

            agent_obj_1 = self._create_agent_persona(agent_1_traits)
            print(f"Created agent persona")
            agent_uuid = uuid.uuid4()

            self.agents_list[agent_uuid] = agent_obj_1

            # save agent to a json file
            try:
                agent_json_path = os.path.join("app", "backend", "source", "agents", f"{str(agent_uuid)}.json")
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(agent_json_path), exist_ok=True)
                
                agent_json = {str(agent_uuid): agent_1_traits}
                
                with open(agent_json_path, 'w') as f:
                    json.dump(agent_json, f, indent=2)  # Use indent for readability
                
            except Exception as e:
                print(f"Error creating json: {e}")

            resp.append(agent_obj_1)
            print(f"Agent persona created for agent {agent['agent_name']}")

        return AgentList(resp)
    


    def get_agents_list(self):
        agents_data = []
        directory = os.path.join("app", "backend", "source", "agents")
        # List all JSON files
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                filepath = os.path.join(directory, filename)
                try:
                    with open(filepath, 'r') as f:
                        agent_json = json.load(f)

                        # Each file is assumed to contain {uuid: {name, traits}}
                        for uuid, agent_info in agent_json.items():
                            agent_entry = {
                                "uuid": uuid,
                                "name": agent_info.get("name"),
                                "traits": agent_info.get("traits")
                            }
                            agents_data.append(agent_entry)

                except Exception as e:
                    print(f"Error reading {filename}: {e}")

        agents_data.extend(self.import_agents_from_genagents())
        return agents_data

    def import_agents_from_genagents(self):
        agents_data = []

        base_path = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
        print(base_path)
        target_path = base_path / "genagents" / "agent_bank" / "populations" / "gss_agents"
        print(target_path)

        # Make sure the path exists
        if not target_path.exists():
            print(f"❌ Path does not exist: {target_path}")
        else:
            print(f"✅ Searching in: {target_path}")

            # Loop through subdirectories (assuming UUID-named folders)
            for subdir in target_path.iterdir():
                if subdir.is_dir():
                    agent_id = str(subdir.absolute()).split('/')[-1]
                    # print("agent_id", agent_id)
                    scratch_file = subdir / "scratch.json"
                    if scratch_file.exists():
                        try:
                            with open(scratch_file, 'r') as f:
                                data = json.load(f)
                                # print(f"📄 Read from {scratch_file}:")
                                # print(json.dumps(data, indent=2))

                                agent_entry = {
                                    "uuid": agent_id,
                                    "name": data['first_name'] + ' ' + data['last_name'],
                                    "traits": data
                                }
                                agents_data.append(agent_entry)
                        except Exception as e:
                            print(f"⚠️ Failed to read {scratch_file}: {e}")
                    else:
                        print(f"❌ scratch.json not found in {subdir}")
        return agents_data

agent_manager = AgentManager()
