import torch
from transformers import LlamaForCausalLM, LlamaTokenizer

# Define the model name - Using 3B model for lower RAM usage
model_name = "openlm-research/open_llama_3b"

model = None
tokenizer = None

def load_model_and_tokenizer():
    """Loads the LLM model and tokenizer."""
    global model, tokenizer # Declare global to modify the global variables
    try:
        print(f"Loading model '{model_name}'...")
        tokenizer = LlamaTokenizer.from_pretrained(model_name)
        print("Tokenizer loaded successfully.")

        # Check if CUDA is available and load in 8-bit if possible
        if torch.cuda.is_available():
            print("CUDA available, loading model in 8-bit.")
            try:
                import accelerate
                import bitsandbytes
            except ImportError:
                print("Error: accelerate or bitsandbytes not installed. Cannot load in 8-bit.")
                print("Please install them: pip install accelerate bitsandbytes")
                return False # Loading failed

            model = LlamaForCausalLM.from_pretrained(
                model_name,
                load_in_8bit=True,
                torch_dtype=torch.float16,
                device_map="auto"
            )
        else:
            print("CUDA not available, loading model on CPU (will be slow).")
            model = LlamaForCausalLM.from_pretrained(model_name)

        print("Model loaded successfully.")
        return True # Successfully loaded

    except Exception as e:
        print(f"Error loading model: {e}")
        print("Please ensure you have sufficient resources and necessary libraries (transformers, torch, accelerate, bitsandbytes if using 8-bit, sentencepiece) installed.")
        print("If the error persists, try clearing your Hugging Face cache.")
        model = None # Ensure model is None if loading fails
        tokenizer = None # Ensure tokenizer is None if loading fails
        return False # Failed to load

def run_attack_menu():
    """Presents an attack menu and runs the selected attack."""
    if model is None or tokenizer is None:
        print("Model and tokenizer are not loaded. Cannot run attacks.")
        return

    attack_options = {
        "1": {"name": "Flooding Attack", "module": "flooding", "function": "run_flooding_attack"},
        "2": {"name": "DoS (Sponge/Resource Exhaustion) Attack", "module": "dos", "function": "run_dos_sponge_attack"},
        "3": {"name": "Energy-Latency Attack", "module": "energyLatency", "function": "run_energy_latency_attack"},
        "4": {"name": "Adversarial Examples", "module": "adversial", "function": "run_adversarial_attack"},
        "5": {"name": "Deceptive Inputs", "module": "deceptiveInputs", "function": "run_deceptive_attack"},
        "6": {"name": "Recursive-bomb Attack", "module": "recursive_bomb", "function": "run_recursive_bomb"},
        "q": {"name": "Quit"}
    }

    while True:
        print("\n--- Select an Attack to Run ---")
        for key, attack_info in attack_options.items():
            print(f"{key}: {attack_info['name']}")

        choice = input("Enter your choice: ").strip().lower()

        if choice == 'q':
            print("Exiting attack menu.")
            break
        elif choice in attack_options and choice != 'q':
            attack_info = attack_options[choice]
            module_name = attack_info["module"]
            function_name = attack_info["function"]

            try:
                attack_module = __import__(module_name)
                attack_function = getattr(attack_module, function_name)

                print(f"\n--- Running {attack_info['name']} ---")
                # the calling function for the attack
                attack_function(model, tokenizer)
                print(f"--- Finished {attack_info['name']} ---")

            except ImportError:
                print(f"Error: Could not import the module '{module_name}'.")
                print("Please ensure the attack script file exists in the same directory.")
            except AttributeError:
                 print(f"Error: Could not find the function '{function_name}' in '{module_name}'.")
                 print("Please ensure the attack script has a function named correctly.")
            except Exception as e:
                print(f"An error occurred while running the attack: {e}")

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Load the model and tokenizer first
    if load_model_and_tokenizer():
        # If loading was successful, run the attack menu
        run_attack_menu()

