#!/bin/bash

# 환경설정 - 가상환경을 초기화하고 라이브러리를 설치합니다.
export HF_TOKEN=""
python3 -m venv ./env
source ./env/bin/activte
pip install -r requirements.txt
cd llamafactory
pip install .

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
python inference.py -m models/distill -t train_data/test.jsonl -o submission.json

# 추론 3단계 - Hard emsemble을 수행합니다.
python hard_enesmble.py -o merged.json -c cache.json

# 추론 4단계 - 요약 후보정을 수행합니다.
python fix_degeneracy -i merged.json -o fixed.json
