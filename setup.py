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

addKnowledge = input("Would you like to upload documents to the database (Y/N): ")
if addKnowledge.lower() == "y":
    print("Adding knowledge.. might take a while.")
    ids = webui.add_knowledge(knowledge.get("id"), entries)
    knowledge = webui.create_or_get_knowledge("SysAdmin Knowledge", "SysAdmin Knowledge scraped from ServerFault")

print("Importing settings...")
with open("ui-settings.json") as f:
    settings = json.load(f)
webui.set_config(settings)

print("Configuring model...")
webui.create_model_from(MODEL_NAME, [knowledge])
print("Setup complete!")