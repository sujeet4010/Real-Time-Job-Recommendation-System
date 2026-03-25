import fitz # PyMuPDF
import os 
from dotenv import load_dotenv
import requests


load_dotenv()

CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")

API_URL = "https://api.cerebras.ai/v1/chat/completions"

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file.
    
    Args:
        uploaded_file (str): The path to the PDF file.
        
    Returns:
        str: The extracted text.
    """
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text



# def ask_openai(prompt, max_tokens=500):
#     """
#     Sends a prompt to the OpenAI API and returns the response.
    
#     Args:
#         prompt (str): The prompt to send to the OpenAI API.
#         model (str): The model to use for the request.
#         temperature (float): The temperature for the response.
        
#     Returns:
#         str: The response from the OpenAI API.
#     """
    

#     response = client.chat.completions.create(
#         model= "gpt-4o",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#         temperature=0.5,
#         max_tokens=max_tokens
#     )

#     return response.choices[0].message.content
def ask_cerebras(prompt, max_tokens=500):
    """
    Ask question to ChatCerebras
    """

    headers = {
        "Authorization": f"Bearer {CEREBRAS_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3.1-8b",
        "messages": [
            {"role": "system", "content": "You are a helpful PDF Q&A assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": max_tokens
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(response.text)
        return "Error occurred"


