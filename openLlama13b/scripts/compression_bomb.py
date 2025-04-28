#!/usr/bin/env python3
"""
Benchmark prompts from inputs/compression_bomb.txt
and show which ones achieve over a given token minimum.
"""

import os, csv, time, argparse, torch, matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def load(model_name: str):
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    print(f"Loading {model_name}")
    bnb = BitsAndBytesConfig(load_in_8bit=True)
    tok = AutoTokenizer.from_pretrained(model_name)
    mod = AutoModelForCausalLM.from_pretrained(
        model_name, quantization_config=bnb, device_map="auto"
    )
    return mod, tok

def _bench(prompts, model, tok, max_new, tok_min,
           csv_path, pdf_path):

    rows = []          # idx, prompt, out_tok, lat, vram, worked?

    for idx, prompt in enumerate(prompts, 1):
        t0 = time.perf_counter()
        inp = tok(prompt, return_tensors="pt").input_ids.to(model.device)
        gen = model.generate(inp, max_new_tokens=max_new, do_sample=False)
        t1 = time.perf_counter()

        out_tok = gen.shape[1] - inp.shape[1]
        lat     = t1 - t0
        vram    = torch.cuda.max_memory_allocated() / 2**20 if torch.cuda.is_available() else 0
        worked  = out_tok >= tok_min
        rows.append([idx, prompt, out_tok, lat, vram, worked])

        flag = "Y " if worked else "N "
        print(f"{flag} [{idx:>3}] out={out_tok:>6}  "
              f"{lat:>6.2f}s  vram={vram:>7.0f} MB")

    # CSV
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="") as f:
        csv.writer(f).writerows(
            [["idx","prompt","out_tok","lat_s","vram_mb","worked"]] + rows
        )
    print("CSV to", csv_path)

    # PDF plot (color coded)
    outs, lats, worked_flags = zip(*[(r[2], r[3], r[5]) for r in rows])
    colours = ["tab:green" if ok else "tab:red" for ok in worked_flags]

    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    with PdfPages(pdf_path) as pdf:
        fig, ax = plt.subplots(figsize=(7,4))
        ax.scatter(outs, lats, c=colours, s=22, alpha=.7)
        ax.set_xlabel("output tokens")
        ax.set_ylabel("latency (s)")
        ax.set_title(f"Compression-bomb results  (green = ≥{tok_min} tok)")
        ax.grid(True, ls="--", lw=.3)
        pdf.savefig(fig); plt.close(fig)
    print("PDF  →", pdf_path)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input",  default="inputs/compression_bomb.txt")
    ap.add_argument("--csv",    default="docs/compression_bomb.csv")
    ap.add_argument("--pdf",    default="docs/compression_bomb.pdf")
    ap.add_argument("--max",    type=int, default=4096, help="max_new_tokens")
    ap.add_argument("--tok-min",type=int, default=1000,
                    help="threshold that marks a prompt as 'worked'")
    ap.add_argument("--model",  default=os.getenv("LLAMA_MODEL",
                        "openlm-research/open_llama_3b"))
    args = ap.parse_args()

    with open(args.input, encoding="utf-8") as f:
        prompts = [p.strip() for p in f if p.strip()]

    model, tok = load(args.model)
    _bench(prompts, model, tok,
           max_new=args.max,
           tok_min=args.tok_min,
           csv_path=args.csv,
           pdf_path=args.pdf)

def run_compression_bomb(model, tokenizer):
    run(model, tokenizer, tok_min=1000)

def run(model, tokenizer,
        *, input_path="inputs/compression_bomb.txt",
           max_new=4096, tok_min=1000,
           csv_path="docs/compression_bomb.csv",
           pdf_path="docs/compression_bomb.pdf"):

    with open(input_path, encoding="utf-8") as f:
        prompts = [p.strip() for p in f if p.strip()]

    _bench(prompts, model, tokenizer,
           max_new=max_new, tok_min=tok_min,
           csv_path=csv_path, pdf_path=pdf_path)

if __name__ == "__main__":
    main()
