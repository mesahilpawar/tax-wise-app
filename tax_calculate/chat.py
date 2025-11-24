import google.generativeai as genai
API_KEY = "AIzaSyB0uh02cPfU5XurKHiQmxmgz80qAB2Awok"

genai.configure(api_key=API_KEY)


model = genai.GenerativeModel('gemini-2.0-flash')
chat = model.start_chat()

# msg = f"""
#     below that indian income tax query write possible answer in just short create proffessinal chatbot answer in  40-50 words and dont ask for extra questions 
#     query : retirement benefits tax,
    
#     """


# response = chat.send_message(msg)
# print("Gemini : ",response.text)


def gen_chat(msg,res):
    try:
        msg = f"""
        Note : if anyone ask about your identity tell you are assistent of TaxBuddy App also dont mentione name query and response in ans just talk casual
        below that indian income tax query write possible answer in just short create proffessinal chatbot answer in  40-50 words and dont ask for extra questions 
        query : {msg}"""
        chat = model.start_chat()
        response = chat.send_message(msg)
        return response.text
    except Exception as e:
        print(e)
        return res