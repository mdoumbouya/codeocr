import requests
import base64

def clear_response(txt):
    first_tilda = txt.find("```")
    if first_tilda != -1:
        second_tilda = txt.find("```", first_tilda + 1)
        if second_tilda != -1:
            if txt[first_tilda + 3: first_tilda + 9] in ["python", "Python"]:
                return txt[first_tilda + 9:second_tilda].strip()
            else:
                return txt[first_tilda + 3:second_tilda].strip()
    return txt

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Replace with your actual API key
api_key = "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"

image_path = "../images/27.jpg"
base64_image = encode_image(image_path)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "The image contains handwritten python code. Only fix typos in the code. *VERY STRICT RULE* - Do not fix any logical, or numerical error of the original code. KEEP IT EXACTLY AS IT IS, even if it is wrong. - Do not change any indentation from the original image. KEEP IT EXACTLY AS IT IS, even if it is wrong."
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}"
                }
            ]
        }
    ],
    "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

if response.status_code == 200:
    json_response = response.json()
    assistant_message = json_response['choices'][0]['message']['content']
    print(clear_response(assistant_message))
else:
    print(f"Error: {response.status_code} - {response.text}")
