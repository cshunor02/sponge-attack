#!/usr/bin/env python3

import os, time, csv, argparse, torch, matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def _benchmark(prompts, model, tok,
               max_new=2048,
               csv_path="docs/recursive_bomb.csv",
               pdf_path="docs/recursive_bomb.pdf"):

    rows = []
    for idx, prompt in enumerate(prompts, 1):
        t0 = time.perf_counter()
        ids_in = tok(prompt, return_tensors="pt").input_ids.to(model.device)
        ids    = model.generate(ids_in, max_new_tokens=max_new, do_sample=False)
        t1 = time.perf_counter()

        in_tok  = ids_in.shape[1]
        out_tok = ids.shape[1] - in_tok
        lat     = t1 - t0
        tps     = out_tok / lat if lat else 0
        vram    = (torch.cuda.max_memory_allocated() / 2**20
                   if torch.cuda.is_available() else 0)

        rows.append([idx, in_tok, out_tok, lat, tps, vram])
        print(f"[{idx:>3}/{len(prompts)}]  out={out_tok:>6}  "
              f"{lat:>6.2f}s  {tps:>6.1f} tok/s  {vram:>7.0f} MB")

    # CSV
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="") as f:
        csv.writer(f).writerows(
            [["idx","in_tok","out_tok","lat","tps","vram_mb"]] + rows
        )
    print("CSV: ", csv_path)

    # PDF
    outs, lats, vrams = zip(*[(r[2], r[3], r[5]) for r in rows])
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    with PdfPages(pdf_path) as pdf:
        outs, lats, vrams = zip(*[(r[2], r[3], r[5]) for r in rows])

        fig, ax = plt.subplots(figsize=(7,4))
        ax.scatter(outs, lats, s=20, alpha=.6)
        ax.set_xlabel("output tokens")
        ax.set_ylabel("latency (s)")
        ax.set_ylim(min(lats)*0.9, max(lats)*1.1)
        ax.set_title("Latency vs length")
        ax.grid(True, ls="--", lw=.3)
        pdf.savefig(fig); plt.close(fig)

        vram0 = min(vrams)
        vram_rel = [v-vram0 for v in vrams]

        fig, ax = plt.subplots(figsize=(7,4))
        ax.scatter(outs, vram_rel, s=20, alpha=.6, color="tab:red")
        ax.set_xlabel("output tokens")
        ax.set_ylabel("Δ VRAM (MB)")
        ax.set_title(f"VRAM over baseline ({vram0:.0f} MB)")
        ax.grid(True, ls="--", lw=.3)
        pdf.savefig(fig); plt.close(fig)

    print("PDF: ", pdf_path)

def run_recursive_bomb(model, tokenizer):
    run(model, tokenizer)

def run(model, tokenizer,
        *,
        input_path="inputs/recursive_bomb.txt",
        max_new=2048,
        csv_path="docs/recursive_bomb.csv",
        pdf_path="docs/recursive_bomb.pdf"):

    with open(input_path, encoding="utf-8") as f:
        prompts = [p.strip() for p in f.read().split("\n\n") if p.strip()]

    _benchmark(prompts, model, tokenizer,
               max_new=max_new, csv_path=csv_path, pdf_path=pdf_path)

# standalone CLI mode
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="inputs/recursive_bomb.txt")
    ap.add_argument("--csv",   default="docs/recursive_bomb.csv")
    ap.add_argument("--pdf",   default="docs/recursive_bomb.pdf")
    ap.add_argument("--max",   type=int, default=2048,
                    help="max_new_tokens")
    ap.add_argument("--model", default=os.getenv("LLAMA_MODEL",
                        "openlm-research/open_llama_3b"))
    args = ap.parse_args()

    # lazy-load the model only in CLI mode
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    bnb = BitsAndBytesConfig(load_in_8bit=True)
    tok = AutoTokenizer.from_pretrained(args.model)
    mod = AutoModelForCausalLM.from_pretrained(
            args.model, quantization_config=bnb, device_map="auto")

    with open(args.input, encoding="utf-8") as f:
        prompts = [p.strip() for p in f.read().split("\n\n") if p.strip()]

    _benchmark(prompts, mod, tok,
               max_new=args.max, csv_path=args.csv, pdf_path=args.pdf)

if __name__ == "__main__":
    main()
