from OpenWebUI import OpenWebUI 
import json

webui = OpenWebUI("", "")

knowledge = webui.create_or_get_knowledge("Testing", "hello world")

model = webui.download_model("llama3.2")
 
with open("data.json", "r") as f:
    data = json.load(f)
stuff = []
for entry in data:
    stuff.append(entry["top_answer"])

ids = webui.add_knowledge(knowledge.get("id"), stuff[0:100])
knowledge = webui.create_or_get_knowledge("Testing", "hello world")


webui.create_model_from("llama3.2", [knowledge])