from transformers import LlamaForCausalLM, LlamaTokenizer # Import LlamaForCausalLM and LlamaTokenizer explicitly
import torch
import time
import os # Import os for cache clearing suggestion

# --- Model Setup ---
# Define the model name - Using 3B model for lower RAM usage
model_name = "openlm-research/open_llama_3b"

# Load the tokenizer and model
# We'll load the model in 8-bit precision to reduce memory usage if a GPU is available
# If you don't have a GPU or enough VRAM, you might need to load in 4-bit or on CPU,
# which will be significantly slower.
# For 8-bit loading, you might need to install 'accelerate' and 'bitsandbytes':
# pip install accelerate bitsandbytes
try:
    print(f"Loading model '{model_name}'...")
    # Load the tokenizer explicitly using LlamaTokenizer, as shown in documentation
    tokenizer = LlamaTokenizer.from_pretrained(model_name)
    print("Tokenizer loaded successfully.")

    # Check if CUDA is available and load in 8-bit if possible
    if torch.cuda.is_available():
        print("CUDA available, loading model in 8-bit.")
        # Import accelerate and bitsandbytes here, although they should be installed
        import accelerate
        import bitsandbytes
        # Load the model explicitly using LlamaForCausalLM, as shown in documentation
        model = LlamaForCausalLM.from_pretrained(
            model_name,
            load_in_8bit=True,
            torch_dtype=torch.float16, # Use float16 for potentially lower memory usage
            device_map="auto" # Automatically distribute model layers across available devices
        )
    else:
        print("CUDA not available, loading model on CPU (will be slow).")
        # Load the model explicitly using LlamaForCausalLM
        model = LlamaForCausalLM.from_pretrained(model_name)

    print("Model loaded successfully.")

except Exception as e:
    print(f"Error loading model: {e}")
    print("Please ensure you have sufficient resources and necessary libraries (transformers, torch, accelerate, bitsandbytes if using 8-bit) installed.")
    print("If the error persists, try clearing your Hugging Face cache as suggested below.")
    model = None # Set model to None if loading fails
    tokenizer = None

# --- Helper function for inference ---
def generate_text(prompt, max_new_tokens=50):
    """
    Generates text from the loaded LLM.
    Returns the generated text and the time taken.
    """
    if model is None or tokenizer is None:
        print("Model not loaded. Cannot generate text.")
        return None, None

    try:
        # Encode the prompt
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids

        # Move input_ids to the same device as the model
        if torch.cuda.is_available():
            input_ids = input_ids.to(model.device)

        # Generate text
        start_time = time.time()
        # Use model.generate for text generation
        # Add pad_token_id and eos_token_id for better generation behavior
        generated_ids = model.generate(
            input_ids=input_ids,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id, # Use eos_token_id for padding
            eos_token_id=tokenizer.eos_token_id # Explicitly set eos_token_id
        )
        end_time = time.time()

        # Decode the generated text
        # Decode only the newly generated tokens (excluding the input prompt)
        # Ensure we are decoding the correct part of the tensor
        generated_text = tokenizer.decode(generated_ids[0][len(input_ids[0]):], skip_special_tokens=True)

        return generated_text, (end_time - start_time)

    except Exception as e:
        print(f"Error during text generation: {e}")
        return None, None

# Example usage (optional, you can comment this out)
# if model is not None and tokenizer is not None:
#     print("\n--- Example Generation ---")
#     example_prompt = "Tell me a short story about a brave knight."
#     generated_text, duration = generate_text(example_prompt, max_new_tokens=100)
#     if generated_text:
#         print(f"Prompt: {example_prompt}")
#         print(f"Generated: {generated_text}")
#         print(f"Time taken: {duration:.4f} seconds")

# --- Troubleshooting Tip ---
# If you continue to have loading issues, you might need to clear your Hugging Face cache.
# The cache location is usually in your home directory under .cache/huggingface/
# You can try deleting the 'hub' folder within the huggingface cache directory.
# Example command (use with caution, this deletes all cached models and tokenizers):
# import shutil
# cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "huggingface", "hub")
# if os.path.exists(cache_dir):
#     print(f"\nTo clear Hugging Face cache, you can uncomment and run the following lines:")
#     print(f"# import shutil")
#     print(f"# shutil.rmtree('{cache_dir}')")
#     print("Warning: This will require redownloading all models.")