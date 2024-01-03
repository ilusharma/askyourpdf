import requests
import json

def create_user():
    url = "https://auth-service.askyourpdf.com/create-anon-user"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = json.loads(response.text)
    user_id = data['userId']

    return user_id

def create_chat_id(user_id):
    url = "https://chat-api.askyourpdf.com/chat"

    payload = {}
    headers = {
        'Authorization': f'Bearer {user_id}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    chat_id = data['chat_id']

    return chat_id

def check_usage(user_id):
    url = "https://doc-api.askyourpdf.com/api/usage"

    payload = {}
    headers = {
        'Authorization': f'bearer {user_id}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    return data

def create_conversation(user_id):

    url = "https://chat-api.askyourpdf.com/conversations?page=1&page_size=20&order=desc&"

    payload = {}
    headers = {
        'Authorization': f'bearer {user_id}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text


def init_chat(user_id, chat_id):

    url = f"https://chat-api.askyourpdf.com/chat/{chat_id}"

    payload = {}
    headers = {
        'Authorization': f'bearer {user_id}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)


    return response.text


def file_upload(user_id,file,chat_id):
    url = "https://doc-api.askyourpdf.com/api/upload"

    payload = {}

    files = [
        ('file', file)
    ]
    headers = {
        'Authorization': f'bearer {user_id}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    if response.status_code == 200:
        data = json.loads(response.text)
        fileId = data['docId']
        init_chat(user_id, chat_id)
        create_conversation(user_id)
        return fileId
    else:
        return response.text


def chatBot(user_id,file_id, chat_id, message):
    url = f"https://chat-api.askyourpdf.com/chat/{file_id}?chat_id={chat_id}&model_name=GPT3&language=DEFAULT"

    payload = json.dumps({
        "message": message
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'bearer {user_id}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text



