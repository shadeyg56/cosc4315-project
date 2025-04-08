from OpenWebUI import OpenWebUI 
import json

MODEL_NAME = "llama3.2"

email = input("Please enter the email you used for Open-WebUI: ")
password = input("Please enter your password: ")

webui = OpenWebUI(email, password)

knowledge = webui.create_or_get_knowledge("SysAdmin Knowledge", "SysAdmin Knowledge scraped from ServerFault")

print("\nDownloading model... might take a while")
model = webui.download_model(MODEL_NAME)
print("Download complete")
 
with open("data.json", "r") as f:
    data = json.load(f)
entries = []
for entry in data:
    string = f"{entry["title"]}\n{entry["top_answer"]}"
    entries.append(string)

print("Adding knowledge.. might take a while.")
ids = webui.add_knowledge(knowledge.get("id"), entries)
knowledge = webui.create_or_get_knowledge("SysAdmin Knowledge", "SysAdmin Knowledge scraped from ServerFault")

print("Configuring model...")
webui.create_model_from(MODEL_NAME, [knowledge])
print("Setup complete!")