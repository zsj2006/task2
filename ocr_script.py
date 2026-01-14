from paddleocr import PaddleOCR
import pandas as pd
import os

# 1. 初始化 OCR（中英文）
ocr = PaddleOCR(lang='ch')

image_dir = "images"
results = []

# 2. 遍历图片
for img_name in sorted(os.listdir(image_dir)):
    if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(image_dir, img_name)
        print(f"正在处理: {img_name}")
        ocr_result = ocr.predict(img_path)

        # 3. 提取识别文本
        if ocr_result and len(ocr_result) > 0:
            result = ocr_result[0]
            texts = result.get('rec_texts', [])
            scores = result.get('rec_scores', [])

            for text, confidence in zip(texts, scores):
                if text:  # 跳过空字符串
                    results.append({
                        "图片名": img_name,
                        "识别文字": text,
                        "置信度": confidence
                    })
                    print(f"  识别: {text} (置信度: {confidence:.3f})")

# 4. 生成 Excel
output_file = "识别结果.xlsx"
if results:
    df = pd.DataFrame(results)
    df.to_excel(output_file, index=False)
    print(f"\n[OK] 已成功生成 Excel：{output_file}，共 {len(results)} 条记录")

    # 自动打开 Excel 文件
    os.startfile(output_file)
else:
    print("\n[WARNING] 未识别到任何文本")
