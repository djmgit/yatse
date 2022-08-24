import os

def save_raw_data(document_id: str, data_path: str, text: str):
    with open(os.path.join(data_path, document_id), 'w') as f:
        f.write(text)
