import os
import random
import shutil

# 너가 정의한 클래스 매핑
CATEGORY_MAP = {
    'Car': 0,
    'Van': 0,
    'Truck': 0,
    'Pedestrian': 1,
    'Person_sitting': 1,
    'Cyclist': 1,
    'Tram': 2,
    'Misc': 3
}

IGNORE_CLASSES = ['DontCare']

IMG_WIDTH = 1242
IMG_HEIGHT = 375

kitti_img_dir = "datasets/KITTI/training/image_2"
kitti_label_dir = "datasets/KITTI/training/label_2"
yolo_img_dir = "datasets/KITTI/kitti_yolo/images"
yolo_label_dir = "datasets/KITTI/kitti_yolo/labels"

# 디렉토리 생성
for split in ['train', 'val']:
    os.makedirs(os.path.join(yolo_img_dir, split), exist_ok=True)
    os.makedirs(os.path.join(yolo_label_dir, split), exist_ok=True)

# 파일 셔플 및 분할
file_names = sorted(os.listdir(kitti_img_dir))
random.seed(42)
random.shuffle(file_names)
split_idx = int(len(file_names) * 0.8)
train_files = file_names[:split_idx]
val_files = file_names[split_idx:]

def convert_and_copy(files, split):
    for file in files:
        file_id = file.split('.')[0]

        # 이미지 복사
        shutil.copy(
            os.path.join(kitti_img_dir, file),
            os.path.join(yolo_img_dir, split, file)
        )

        # 라벨 처리
        label_path = os.path.join(kitti_label_dir, file_id + '.txt')
        if not os.path.exists(label_path):
            continue

        with open(label_path, 'r') as f:
            lines = f.readlines()

        yolo_lines = []
        for line in lines:
            parts = line.strip().split()
            label = parts[0]
            if label in IGNORE_CLASSES:
                continue
            if label not in CATEGORY_MAP:
                continue  # 정의되지 않은 클래스 무시

            cls_id = CATEGORY_MAP[label]
            xmin, ymin, xmax, ymax = map(float, parts[4:8])
            x_center = ((xmin + xmax) / 2) / IMG_WIDTH
            y_center = ((ymin + ymax) / 2) / IMG_HEIGHT
            w = (xmax - xmin) / IMG_WIDTH
            h = (ymax - ymin) / IMG_HEIGHT
            yolo_lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}")

        with open(os.path.join(yolo_label_dir, split, file_id + '.txt'), 'w') as f:
            f.write('\n'.join(yolo_lines))

# 실행
convert_and_copy(train_files, 'train')
convert_and_copy(val_files, 'val')
print(f"✅ 총 {len(train_files)} train, {len(val_files)} val 변환 완료")
