import json

def load_config(category):
    try:
        with open("config.json","r") as file:
            config = json.load(file)
            return config[category]
    except FileNotFoundError:
        raise("JSON 파일을 찾을 수 없습니다.")
    
def save_config(category, key, value):
    try:
        with open("config.json", "r") as file:
            config = json.load(file)
    except FileNotFoundError:
        config = {}
    try:
        config[category][key] = value
    except:
        raise("잘못된 카테고리입니다.")    
    with open("config.json", "w") as file:
        json.dump(config, file, indent=4)

if __name__ == "__main__":
    save_config("email", "sender", "your@gmail.com")
    save_config("email", "receiver", "your@gmail.com")
    save_config("email", "username", "your@gmail.com")
    save_config("email", "password", "your_gmail_second_password")