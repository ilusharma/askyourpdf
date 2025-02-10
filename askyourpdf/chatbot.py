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



def main():
    # Step 1: Create an anonymous user
    user_id = create_user()
    print(f"User ID: {user_id}")
    
    # Step 2: Create a new chat ID
    chat_id = create_chat_id(user_id)
    print(f"Chat ID: {chat_id}")
    
    # Step 3: Upload a PDF file
    pdf_path = "test.pdf"  # Replace with the actual path to your PDF
    with open(pdf_path, 'rb') as pdf_file:
        file_id = file_upload(user_id, pdf_file, chat_id)
    
    if not isinstance(file_id, str):
        print("Error in file upload:", file_id)
        return

    print(f"Uploaded File ID: {file_id}")
    while True:

    # Step 4: Interact with the chatbot
        message = input('que') # Replace with your desired input
        response = chatBot(user_id, file_id, chat_id, message)
        print("Chatbot Response:", response)

if __name__ == "__main__":
    main()
