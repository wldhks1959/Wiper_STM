###
#      옵션	        설명
# --weights	사용할 모델 가중치
# --data	평가용 데이터셋 YAML
# --img	입력 이미지 크기
# --task val	검증(validation)만 수행
# --half	FP16으로 빠르게 (TensorRT처럼 mixed precision)
# --device 0	GPU 사용 (CUDA 장치)
# --save-json	COCO 평가용 JSON 저장
# --verbose	클래스별 정밀도/재현율 출력
###

python val.py \
  --weights yolov5s.pt \
  --data data/coco128.yaml \
  --img 640 \
  --task val \
  --half \
  --device 0 \
  --verbose

# python val.py \
#   --weights yolov5s.pt \
#   --data /home/wiper/jiwan/yolov5/data/kitti.yaml \
#   --img 640 \
#   --task val \
#   --half \
#   --device 0 \
#   --save-json \
#   --verbose
