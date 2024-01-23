import json

def read_json(file_name="players.json"):
    try:
        with open(file_name, "r", encoding='utf8') as f:
            return json.load(f)
    except:
        return {}

def write_json(data, file_name="players.json"):
    with open(file_name, "w", encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)
