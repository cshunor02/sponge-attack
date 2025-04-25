This set of Python scripts demonstrates various attack types, including Denial of Service (DoS) variations (Flooding, Resource Exhaustion/Sponge, Energy-Latency) and input manipulation attacks (Adversarial Examples, Deceptive Inputs), targeting the **open_llama_13b** model.

These scripts use the Hugging Face **transformers** library to load and interact with the model. They provide basic examples of how to craft inputs and measure some of the observable effects of the attacks.

# Prerequisites:

Before running these scripts, you'll need to have Python installed, along with the transformers and torch libraries. You can install them using pip:
```
pip install transformers
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install accelerate bitsandbytes
pip install protobuf
pip install sentencepiece
```
You will also need sufficient hardware resources (CPU, RAM, and potentially GPU) to run the open_llama_3b model, as it is a large model.

# Disclaimer:

These scripts are for educational and research purposes only. Attacking systems or services without explicit permission is illegal and unethical. Use these scripts responsibly and only in controlled environments with models you own or have permission to test.

# How to?

Run the loadModel.py file

# Resources
[open llama 3b](https://huggingface.co/openlm-research/open_llama_3b)
[pytorch](https://pytorch.org/)
[open llama git](https://github.com/openlm-research/open_llama)