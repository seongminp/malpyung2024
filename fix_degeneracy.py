import json
import argparse


def valid(text):
    if len(text) > 500:
        return False
    if len(text) < 150:
        return False
    if "~" in text:
        return False
    return True


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", help="File to fix")
    parser.add_argument("-o", "--output-file", help="Final output")
    args = parser.parse_args()

    with open(args.input_file) as rf:
        data = json.load(rf)

    with open("submissions/best1.json") as rf:
        candidate1 = json.load(rf)

    with open("submissions/best2.json") as rf:
        candidate2 = json.load(rf)

    with open("submissions/best3.json") as rf:
        candidate3 = json.load(rf)

    with open("submissions/best4.json") as rf:
        candidate4 = json.load(rf)

    with open("submissions/best5.json") as rf:
        candidate5 = json.load(rf)

    with open("submissions/best6.json") as rf:
        candidate6 = json.load(rf)

    for i, sample in enumerate(data):
        summary = sample["output"]
        alternative1 = candidate1[i]["output"]
        alternative2 = candidate2[i]["output"]
        alternative3 = candidate3[i]["output"]
        alternative4 = candidate1[i]["output"]
        alternative5 = candidate2[i]["output"]
        alternative6 = candidate3[i]["output"]
        if valid(summary):
            alternative = summary
        elif valid(alternative):
            alternative = alternative1
        elif valid(alternative2):
            alternative = alternative2
        elif valid(alternative3):
            alternative = alternative3
        elif valid(alternative4):
            alternative = alternative4
        elif valid(alternative5):
            alternative = alternative5
        else:
            alternative = alternative6

        sample["output"] = alternative

    with open(args.output_file, "w") as wf:
        json.dump(data, wf, indent=4, ensure_ascii=False)
