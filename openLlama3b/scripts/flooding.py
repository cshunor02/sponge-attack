import time
import threading
import queue
import torch

# --- Flooding Attack Logic (Encapsulated in a function) ---
def worker(prompt_queue, results_queue, model, tokenizer, max_new_tokens=50):
    """Thread worker function to process prompts from the queue."""
    if model is None or tokenizer is None:
         # Put an error message for all prompts if model/tokenizer not loaded
         while not prompt_queue.empty():
             try:
                 prompt = prompt_queue.get_nowait()
                 results_queue.put((prompt, "Error: Model or tokenizer not loaded in the environment.", None))
                 prompt_queue.task_done()
             except queue.Empty:
                 break
         return # Exit the thread

    while True:
        try:
            prompt = prompt_queue.get_nowait()
        except queue.Empty:
            break

        try:
            # Encode the prompt
            input_ids = tokenizer(prompt, return_tensors="pt").input_ids
            if torch.cuda.is_available():
                # Ensure input_ids are on the same device as the model
                input_ids = input_ids.to(model.device)

            # Generate text
            start_time = time.time()
            generated_ids = model.generate(
                input_ids=input_ids,
                max_new_tokens=max_new_tokens,
                pad_token_id=tokenizer.eos_token_id, # Use eos_token_id for padding
                eos_token_id=tokenizer.eos_token_id # Explicitly set eos_token_id
            )
            end_time = time.time()

            # Decode the generated text
            generated_text = tokenizer.decode(generated_ids[0][len(input_ids[0]):], skip_special_tokens=True)

            results_queue.put((prompt, generated_text, end_time - start_time))

        except Exception as e:
            results_queue.put((prompt, f"Error during generation: {e}", None))

        prompt_queue.task_done() # Mark task as done

def run_flooding_attack(model, tokenizer):
    # Check if model and tokenizer are available before starting
    if model is None or tokenizer is None:
        print("Model or tokenizer not provided to run_flooding_attack.")
        return

    num_requests = 100 # Number of requests to send
    num_threads = 10 # Number of concurrent threads (simulating multiple users)
    prompts = [f"Write a short sentence about topic {i}." for i in range(num_requests)]

    prompt_queue = queue.Queue()
    results_queue = queue.Queue()

    # Populate the queue with prompts
    for prompt in prompts:
        prompt_queue.put(prompt)

    threads = []
    print(f"\n--- Starting Flooding Attack with {num_requests} requests and {num_threads} threads ---")
    start_attack_time = time.time()

    # Start worker threads
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(prompt_queue, results_queue, model, tokenizer))
        thread.start()
        threads.append(thread)

    # Wait for all prompts to be processed
    prompt_queue.join()

    end_attack_time = time.time()
    total_attack_duration = end_attack_time - start_attack_time

    print("\n--- Flooding Attack Results ---")
    processed_count = 0
    total_latency = 0
    while not results_queue.empty():
        prompt, result, duration = results_queue.get()
        # print(f"Prompt: {prompt[:50]}...") # Print truncated prompt
        # print(f"Result: {result[:50]}...") # Print truncated result
        if duration is not None:
            processed_count += 1
            total_latency += duration
            # print(f"Latency: {duration:.4f} seconds")
        # else:
            # print("Request failed.")
        # print("-" * 20)

    print(f"Total requests sent: {num_requests}")
    print(f"Requests processed successfully: {processed_count}")
    print(f"Total attack duration: {total_attack_duration:.4f} seconds")
    if processed_count > 0:
        average_latency = total_latency / processed_count
        print(f"Average request latency: {average_latency:.4f} seconds")
        throughput = processed_count / total_attack_duration
        print(f"Throughput: {throughput:.2f} requests/second")
    else:
        print("No requests were processed successfully.")

    print("--- Flooding Attack Simulation Finished ---")

# Example of how to run this script directly for testing (optional)
# if __name__ == "__main__":
#     # This part is for direct testing and would require loading the model here
#     # For normal use with the menu script, this block is not executed
#     print("Running Flooding Attack script directly (requires model loading here).")
#     # Add model loading code here if you want to run this script standalone for testing
#     # from transformers import LlamaForCausalLM, LlamaTokenizer
#     # model_name = "openlm-research/open_llama_3b"
#     # tokenizer = LlamaTokenizer.from_pretrained(model_name)
#     # model = LlamaForCausalLM.from_pretrained(model_name, device_map='auto')
#     # run_flooding_attack(model, tokenizer)
#     print("Direct execution finished.")