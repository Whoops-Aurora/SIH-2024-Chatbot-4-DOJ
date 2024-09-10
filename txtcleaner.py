import re

def clean_text(text):
    # Remove emojis and invalid characters
    emoji_pattern = re.compile("[\U00010000-\U0010ffff]", re.UNICODE)
    cleaned_text = emoji_pattern.sub(r'', text)
    
    # Remove non-printable characters
    cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', cleaned_text)
    
    return cleaned_text

def read_and_clean_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return clean_text(text)
