import json
from sklearn.model_selection import train_test_split

def read_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = [json.loads(line.strip()) for line in f if line.strip()]
    return data

def write_jsonl(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            json_line = json.dumps(item, ensure_ascii=False)
            f.write(json_line + '\n')

def split_jsonl_dataset(input_path, train_path, test_path, test_size=0.2, seed=42):
    data = read_jsonl(input_path)
    train_data, test_data = train_test_split(data, test_size=test_size, random_state=seed)
    write_jsonl(train_data, train_path)
    write_jsonl(test_data, test_path)
    print(f"训练集 {len(train_data)} 条, 测试集 {len(test_data)} 条")

# 4. 示例调用
split_jsonl_dataset(
    input_path='3.jsonl',
    train_path='train3.jsonl',
    test_path='test3.jsonl',
    test_size=0.2
)

