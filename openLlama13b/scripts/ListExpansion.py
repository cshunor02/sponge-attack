import torch
import time
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Define model source
model_name = "openlm-research/open_llama_3b"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto")

# Set up text generation pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device_map="auto")

# Prompt to generate structured cyber attack information
prompt = (
    "List 1,000 types of cyber attacks grouped into at least 20 categories. "
    "For each item, include:\\n"
    "- A name\\n"
    "- A one-sentence description\\n"
    "- A hypothetical impact score (1–100)"
)

# Track time for inference
start = time.time()
results = generator(prompt, max_new_tokens=1024, do_sample=False, truncation=True)
end = time.time()

# Display inference time and results
print(f"\\n--- Inference Time: {round(end - start, 2)} seconds ---\\n")
print(results[0]["generated_text"])