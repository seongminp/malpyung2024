# malpyung2024
2024 인공지능 말평 &lt;일상 대화 요약 (나 유형)> 엘리팀

## 개요

1. 대회 재현성 검증을 위해선 환경설정 후 `run_inference.sh`만 수행하시면 됩니다 (inference, 앙상블, 후처리 포함).

2. 앙상블 파이프라인 없이 업로드 된 모델로 대화를 요약하려면 `inference.py`만 보시면 됩니다.

3. 직접 훈련을 하시려면 `run_everything.sh`을 참고해주세요.


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
python inference.py -m seongmin/malpyung2024 -t data/test.jsonl -o output.json

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

- `data` - 훈련, 추론에 필요한 데이터 디렉토리.
  
| dataset_info.json      	| LLaMA-Factory로 훈련을 위해 필요한 meatadata 	|
|------------------------	|----------------------------------------------	|
| distill1.jsonl         	| self-distillation 훈련용 데이터 1            	|
| distill2.jsonl         	| self-distillation 훈련용 데이터 2            	|
| kto.jsonl              	| KTO 훈련용 데이터                            	|
| test.jsonl             	| Prompt 형식 적용된 테스트 데이터             	|
| train.jsonl            	| Prompt 형식 적용된 훈련 데이터               	|
| train_augmented.jsonl  	| 국립국어원 일상대화요약 2023 데이터          	|
| validation.jsonl       	| Prompt 형식 적용된 dev 데이터                	|
| 일상대화요약_test.json 	| 원본 대회 테스트 데이터                      	|


- `llamafactory` - LLaMA-Factory 라이브러리 (훈련을 위한 dependency입니다).
- `models` - 학습 완료된 모델이 저장되는 디렉토리입니다 (sft, kto, distilled 등).
- `submissions` - 리더보드에 제출할 최종 JSON이 저장되는 디렉토리입니다.
- `train_configs` - LLaMA-Factory에 필요한 훈련 configuration이 모여있습니다.
- `fix_degeneracy.py` - 모델 최종 후처리를 수행하는 모듈입니다.
- `hard_ensemble.py` - 여러 요약 결과를 앙상블하는 모듈입니다.
- `inference.py` - 사전학습된 모델을 이용해서 요약을 생성합니다. 
- `requirements.txt` - PIP dependency 목록입니다.
- `run_everything.sh` - 훈련+추론 파이프라인을 전부 수행합니다.
- `run_inference.sh` - 재현성 검증을 위해 추론 파이프라인을 전부 수행합니다. Self-distillation 다음 단계부터 수행합니다.
