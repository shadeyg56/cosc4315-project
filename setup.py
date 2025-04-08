from OpenWebUI import OpenWebUI 
import json

MODEL_NAME = "llama3.2"

email = input("Please enter the email you used for Open-WebUI: ")
password = input("Please enter your password")

webui = OpenWebUI(email, password)

knowledge = webui.create_or_get_knowledge("SysAdmin Knowledge", "SysAdmin Knowledge scraped from ServerFault")

model = webui.download_model(MODEL_NAME)
 
with open("data.json", "r") as f:
    data = json.load(f)
entries = []
for entry in data:
    string = f"{entry["title"]}\n{entry["top_answer"]}"
    entries.append(entry["top_answer"])

ids = webui.add_knowledge(knowledge.get("id"), entries[0:100])
knowledge = webui.create_or_get_knowledge("SysAdmin Knowledge", "SysAdmin Knowledge scraped from ServerFault")


webui.create_model_from(MODEL_NAME, [knowledge])