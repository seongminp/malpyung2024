import argparse
import json

import torch
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="Model path")
    parser.add_argument("-t", "--test-file", help="Test file")
    parser.add_argument("-o", "--output", help="Output file")
    args = parser.parse_args()

    with open("data/일상대화요약_test.json") as rf:
        result = json.load(rf)

    tokenizer = AutoTokenizer.from_pretrained(args.model)
    generator = pipeline(
        model=args.model,
        task="text-generation",
        device_map="auto",
        model_kwargs={"attn_implementation": "sdpa"},
        torch_dtype=torch.bfloat16,
    )

    with open(args.test_file) as rf:
        dataset = [json.loads(line)["conversation"][:-1] for line in rf]

    batch_size = 1
    for i in tqdm(range(0, len(dataset), batch_size)):
        conversation = dataset[i : i + batch_size]
        output = generator(
            conversation, max_new_tokens=700, temperature=0.6, top_p=0.9, do_sample=True
        )
        summaries = [out[0]["generated_text"][-1]["content"] for out in output]

        for j, summary in enumerate(summaries):
            result[i + j]["output"] = summary

    with open(args.output, "w") as wf:
        json.dump(result, wf, ensure_ascii=False, indent=4)
