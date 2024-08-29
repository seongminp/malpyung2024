# Models

직접 학습을 할 때 모델이 저장되는 디렉토리입니다.

학습을 하지 않고 추론 검증을 위해서는 [허깅페이스 리포지토리](https://huggingface.co/seongmin/malpyung2024)에 업로드 된 모델을 사용하시면 됩니다.


### 모델 설명
- `sft-lora`: 학습 데이터 (train.jsonl, validation.jsonl, train_augmented.jsonl)로 lora finetuning한 어댑터.
- `sft`: `sfr-lora`를 `gemma-2-9b`에 merge한 모델. (추론 결과는 `sft-lora`와 동일함)
- `kto-lora`: KTO데이터 (kto.jsonl)로 `sft`를 align tuning한 lora 어댑터.
- `kto`: `kto-lora`를 `sft`에 merge한 모델. (추론 결과는 `kto-lora`와 동일함)
- `distill-lora`: `kto` 모델에 self-distillation을 적용한 lora 어댑터.
- `distill`: `distill-lora`를 `kto`에 merge한 모델 (추론 결과는 `distill-lora`와 동일함)
    - 위에 언급된 [허깅페이스](https://huggingface.co/seongmin/malpyung2024)에 올라간 버전입니다.
