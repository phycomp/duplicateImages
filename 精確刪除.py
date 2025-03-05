要使用 `dhash` 或 `phash` 來更精確地比較圖片並找出重複圖片，可以對之前的腳本進行修改。`dhash` 和 `phash` 是更精確的哈希算法，能夠更好地捕捉圖片的細節差異。

以下是改進後的 Python 腳本，使用 `dhash` 和 `phash` 來比較圖片：

---

### 改進後的腳本

```python
import os
from PIL import Image
import imagehash
from collections import defaultdict

def calculate_hashes(image_path):
    """計算圖片的 dhash 和 phash"""
    with Image.open(image_path) as img:
        dhash = imagehash.dhash(img)  # 計算 dhash
        phash = imagehash.phash(img)  # 計算 phash
        return dhash, phash

def find_duplicate_images(directory):
    # 用來儲存哈希值和對應的圖片路徑
    hash_dict = defaultdict(list)

    # 遍歷目錄中的所有文件
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            filepath = os.path.join(directory, filename)
            try:
                # 計算圖片的 dhash 和 phash
                dhash, phash = calculate_hashes(filepath)
                # 將哈希值組合作為鍵（更精確的比較）
                hash_key = (dhash, phash)
                hash_dict[hash_key].append(filepath)
            except Exception as e:
                print(f"無法處理文件 {filename}: {e}")

    # 找出重複的圖片
    duplicates = [filepaths for filepaths in hash_dict.values() if len(filepaths) > 1]

    return duplicates

def delete_duplicates(duplicates):
    for duplicate_group in duplicates:
        # 保留第一個文件，刪除其他重複文件
        for filepath in duplicate_group[1:]:
            try:
                os.remove(filepath)
                print(f"已刪除重複文件: {filepath}")
            except Exception as e:
                print(f"無法刪除文件 {filepath}: {e}")

if __name__ == "__main__":
    directory = "你的目錄路徑"  # 替換為你的目錄路徑
    duplicates = find_duplicate_images(directory)
    delete_duplicates(duplicates)
```

---

### 改進點說明

1. **使用 `dhash` 和 `phash`**:
   - `dhash` 是基於圖片梯度變化的哈希算法，適合檢測圖片的結構差異。
   - `phash` 是基於圖片頻率的哈希算法，適合檢測圖片的整體相似性。
   - 將兩者結合使用 (`hash_key = (dhash, phash)`) 可以更精確地判斷圖片是否重複。

2. **更精確的比較**:
   - 通過組合 `dhash` 和 `phash`，腳本能夠更好地捕捉圖片的細節差異，減少誤判。

3. **錯誤處理**:
   - 在計算哈希值時，如果圖片無法打開或處理，會捕獲異常並跳過該文件。

---

### 運行腳本

1. 將腳本保存為 `remove_duplicates.py`。
2. 在終端中運行：
   ```bash
   python remove_duplicates.py
   ```

---

### 進一步優化

1. **哈希值相似度閾值**:
   - 如果你希望允許一定程度的差異（例如圖片經過輕微壓縮或調整），可以使用 `hash1 - hash2` 來計算哈希值的差異，並設置一個閾值。
   - 例如：
     ```python
     if (dhash1 - dhash2) < threshold and (phash1 - phash2) < threshold:
         # 認為是重複圖片
     ```

2. **多線程處理**:
   - 如果目錄中的圖片數量很多，可以使用多線程來加速哈希值的計算。

3. **圖像預處理**:
   - 在計算哈希值之前，可以對圖片進行預處理（例如調整大小、轉為灰度圖），以提高比較的準確性。

---

### 示例輸出

運行腳本後，輸出可能如下：

```
已刪除重複文件: /path/to/image1_duplicate.jpg
已刪除重複文件: /path/to/image2_duplicate.png
無法刪除文件 /path/to/image3_duplicate.jpg: 文件不存在
```

---

通過這種方式，你可以更精確地找出並刪除目錄中的重複圖片。
