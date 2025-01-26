import torch
import google
from trl import SFTTrainer, SFTConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, DataCollatorForSeq2Seq
from datasets import load_dataset

dataset = load_dataset("json", data_files="training_data/rmf_training.json")

train_dataset = dataset["train"]

print(train_dataset)

pretrained_model_name = "Mistral-7B-Instruct-v0.3"
model = AutoModelForCausalLM.from_pretrained(pretrained_model_name, torch_dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name, trust_remote_code=True)

model_training_args = TrainingArguments(
    output_dir="Mistral-7B-Instruct-v0.3",
    per_device_train_batch_size=4,
    optim="adamw_torch",
    logging_steps=80,
    learning_rate=2e-4,
    warmup_ratio=0.1,
    lr_scheduler_type="linear",
    num_train_epochs=1,
    save_strategy="epoch"
)

SFT_trainer = SFTTrainer(
    model=model,
    train_dataset=train_dataset,
    dataset_text_field="text",
    max_seq_length=1024,
    tokenizer=tokenizer,
    args=model_training_args,
    packing=True,
    peft_config=lora_peft_config,
)

tokenizer.pad_token = tokenizer.eos_token
model.resize_token_embeddings(len(tokenizer))
model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_peft_config)
training_args = model_training_args
trainer = SFT_trainer
trainer.train()
