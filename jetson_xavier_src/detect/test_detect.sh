#!/bin/bash

VIDEO_PATH="/home/wiper/jiwan/videos/test_drive_30.mp4"
IMG_SIZE=640
CONF=0.25

# 실험 조합 정의 
# baseline : 기본 YOLOv5
# half : F16 모드로 실행 (메모리 적고 빠름)
# augment: --augment -> 추론 시 테스트 -time augmentation 적용(정확도 증가, 속도 감소)
# half_augment : F16 모드 + --augment
declare -A experiments
experiments["baseline"]="--half"
experiments["half_augment"]="--half --augment"

for name in "${!experiments[@]}"; do
    python detect.py \
        --weights yolov5s.pt \
        --source "$VIDEO_PATH" \
        --conf $CONF \
        --img $IMG_SIZE \
        --save-txt \
        --save-conf \
        --device 0 \
        --project runs/test_detect \
        --name "$name" \
        ${experiments[$name]}
done

# 결과 요약 실행
python test_detect_summary.py
