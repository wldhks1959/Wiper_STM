import os, glob, re, statistics, pandas as pd

# 🔍 inference time이 기록된 로그 파일에서 시간을 추출
def extract_inference_times(log_file):
    times = []
    with open(log_file, 'r') as f:
        for line in f:
            match = re.search(r"inference: (\d+\.\d+)s", line)  # 'inference: 0.085s' 형식 추출
            if match:
                times.append(float(match.group(1)))  # 소수점 형태로 저장
    return times

# 📦 각 라벨(txt 파일)에서 객체 탐지 수를 누적 계산
def count_detections(label_dir):
    total = 0
    for file in glob.glob(os.path.join(label_dir, "*.txt")):
        with open(file, 'r') as f:
            total += len(f.readlines())  # 각 줄이 1개 객체 탐지를 의미함
    return total

# 🗂 실험 결과가 저장된 디렉토리 경로 (detect.py의 --project에 해당)
base_dir = "runs/test_detect"
results = []

# 🔄 각 실험 디렉토리에 대해 평균 시간, FPS, 객체 수를 계산
for name in os.listdir(base_dir):
    exp_dir = os.path.join(base_dir, name)
    label_dir = os.path.join(exp_dir, "labels")               # 라벨 텍스트 파일 위치
    log_file = os.path.join(exp_dir, "results.txt")           # 추론 시간 로그

    # 추론 시간 로그가 있다면 평균과 FPS 계산
    if os.path.exists(log_file):
        inf_times = extract_inference_times(log_file)
        avg_time = statistics.mean(inf_times) if inf_times else 0
        fps = 1 / avg_time if avg_time else 0
    else:
        avg_time = 0
        fps = 0

    # 📊 객체 수 계산
    total_objs = count_detections(label_dir)

    # 📋 결과 누적
    results.append({
        "Option Combination": name,
        "FPS": round(fps, 2),
        "Inference Time (ms)": f"{avg_time * 1000:.2f}",
        # "Amount of the total objs": f"{total_objs}"
    })

# 💡 DataFrame으로 변환 후 시각화
df = pd.DataFrame(results)
print(df)
df.to_csv("summary_results.csv", index=False)  # CSV로 저장