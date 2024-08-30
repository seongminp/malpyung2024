# malpyung2024
2024 인공지능 말평 &lt;일상 대화 요약 (나 유형)> 엘리팀


## 환경 설정
1. Git 레포지토리를 clone 합니다.
```
git clone https://github.com/seongminp/malpyung2024.git
cd malpyung2024
```
2. 가상환경을 초기화하고 필요 라이브러리를 설치합니다.
```
python3 -m venv ./env
source ./env/bin/activate
pip install -r requirements.txt
```

## 모델 추론하기 (모델 재현성 검증)
```
./run_inference.sh
```
스크립트 실행 후 *submission.json* 파일에 최종 요약이 출력됩니다.

#### `run_inference.sh` 코드 설명
```
#!/bin/bash

# 추론 2단계 - 요약을 생성합니다.
python inference.py \
    -m seongmin/malpyung2024 \
    -t data/test.jsonl \
    -o output.json

# 추론 3단계 - Hard ensemble을 수행합니다.
python hard_ensemble.py -o merged.json

# 추론 4단계 - 요약 후보정을 수행합니다.
python fix_degeneracy.py -i merged.json -o submission.json
```
- `inference.py`: Self-distillation까지 완료된 모델을 Huggingface에서 다운  받고 요약을 생성합니다.
- `hard_ensemble.py`: 여러 요약을 합쳐서 앙상블합니다. 
  - 본 예시에는 inference.py를 한 번 호출하지만, 실제로는 여러 번 부를수록 성능이 올라갑니다. 
  - 여러 번 inference를 하실 경우, hard_ensemble.py 33번째 줄의 candidates 리스트에 앙상블할 json 파일 경로를 추가해주세요.
- `fix_degeneracy.py`: 길이 기반 요약 후처리 보정을 합니다.

## 레포지토리 각 파일 설명
