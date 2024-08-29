import argparse
from pathlib import Path

import evaluate

from tqdm import tqdm
import copy
import json


bert_scorer = evaluate.load("bertscore")
bert_model_type = "bert-base-multilingual-cased"


def calc_bertscore(true_data, pred_data):
    if type(true_data[0]) is list:
        true_data = list(map(lambda x: x[0], true_data))

    scores = bert_scorer.compute(
        predictions=pred_data, references=true_data, model_type=bert_model_type
    )

    return sum(scores["f1"]) / len(scores["f1"])


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-c", "--cache", help="Precomputed values")
    args = parser.parse_args()

    candidates = [
    ]

    refs = [
    ]
   
    with open(args.cache) as rf:
        cache = json.load(rf)

    ref_datas = []
    for ref in refs:
        with open(ref) as rf:
            ref_data = [json.loads(line) for line in rf]
        ref_datas.append((Path(ref).stem, ref_data))


    candidate_submissions = [] 
    for c in candidates:
        with open(c) as rf:
            d = json.load(rf)
        candidate_submissions.append((Path(c).stem, d))

    output = []

    for i in tqdm(range(len(ref_datas[0][1]))):

        collected = []
        for name, d in candidate_submissions:

            entry = {}
            for ri, (ref_name, ref_data) in enumerate(ref_datas):
                ref = ref_data[i]['conversation'][-1]['content']
                id = f"{ref_name}_{name}_{i}"
                summary = d[i]['output']
                if id in cache:
                    bertscore = cache[id]['bertscore']
                else:
                    bertscore = calc_bertscore([ref], [summary])

                cache[id] = {f"rouge": None, "bertscore": bertscore, "bleurt": None}
                entry[f'r_{ref_name}'] = rouge
                entry[f'bs_{ref_name}'] = bertscore
                entry[f'bl_{ref_name}'] = bleurt
            entry['summary'] = summary
            entry['source'] = name

            collected.append(entry)

        # Rank with bertscore.
        ranked = sorted(collected, key=lambda x: sum(x[f'bs_{rn}'] for rn, _ in ref_datas), reverse=True)

        entry = copy.deepcopy(d[i])
        entry['output'] = ranked[0]['summary']
        output.append(entry)

    with open(args.cache, 'w') as wf:
        json.dump(cache, wf, ensure_ascii=False, indent=4)
    with open(args.output, 'w') as wf:
        json.dump(output, wf, indent=4, ensure_ascii=False)
