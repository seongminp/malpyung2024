#!/bin/bash

# 추론 2단계 - 요약을 생성합니다.
python inference.py -m seongmin/malpyung2024 -t train_data/test.jsonl -o output.json

# 추론 3단계 - Hard ensemble을 수행합니다.
python hard_enesmble.py -o merged.json -c cache.json

# 추론 4단계 - 요약 후보정을 수행합니다.
python fix_degeneracy -i merged.json -o submission.json
