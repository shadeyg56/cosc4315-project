from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling

# Load your sys admin dataset
dataset = load_dataset("json", data_files={"train": "data.json"})
dataset = dataset["train"].train_test_split(test_size=0.2, seed=35)

# Load GPT-2 model and tokenizer
model_name = "openai-community/gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(model_name)

# Preprocess the dataset
def tokenize(example):
    prompt = f"Question: {example['question']}\nAnswer: {example['top_answer']}"
    return tokenizer(prompt, padding="max_length", truncation=True)

tokenized_dataset = dataset.map(tokenize, batched=False)

data_collator = DataCollatorForLanguageModeling(tokenizer, mlm=False)

# Fine-tuning parameters
training_args = TrainingArguments(
    evaluation_strategy="epoch",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    save_total_limit=2
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    data_collator=data_collator
)

# Fine-tuning
trainer.train()

# Save the fine-tuned model
# model.save_pretrained("./fine_tuned_sys_admin_model")
# tokenizer.save_pretrained("./fine_tuned_sys_admin_model")
trainer.save_model("sys-admin-gpt2")