#!/bin/bash

# 학습 1단계 - Supervied finetuning을 수행합니다.
llamafactory-cli train ../train_configs/sft.yaml --dataset-dir=../data
llamafactory-cli export ../train_configs/export-sft.yaml --dataset-dir=../data

# 학습 2단계 - KTO를 수행합니다.
llamafactory-cli train ../train_configs/kto.yaml --dataset-dir=../data
llamafactory-cli export ../train_configs/export-kto.yaml --dataset-dir=../data

# 추론 1단계 - Self-distillation을 수행합니다.
llamafactory-cli train ../train_configs/distill.yaml --dataset-dir=../data
llamafactory-cli export ../train_configs/export-distill.yaml --dataset-dir=../data

# 추론 2단계 - 요약을 생성합니다.
cd ..
python inference.py -m models/distill -t data/test.jsonl -o output.json

# 추론 3단계 - Hard ensemble을 수행합니다.
python hard_ensemble.py -o merged.json

# 추론 4단계 - 요약 후보정을 수행합니다.
python fix_degeneracy.py -i merged.json -o submission.json
