import requests
from tokenizer import Tokenizer
import time
import math

api = open('./OPENAI_API_KEY.txt')
API_KEY = api.read().strip('\n')
API_URL = 'https://api.openai.com/v1/chat/completions'

def chat_with_gpt(messages):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-4o-mini',
        'messages': messages
    }
    response = requests.post(API_URL, headers=headers, json=data)
    response_data = response.json()
    try:
        message = response_data['choices'][0]['message']['content']
    except:
        message = ['error',response_data['error']['message']]
    return message

def main():
    messages = [{'role': 'system', 'content': 'I will share with you a string in several parts, after I have provided all the parts I will say "You can analyze them now", and then you have to combine them together and understand it. Now, until I have provided you all the parts and given you that specific prompt marking the end, you will respond with blank messages(.).'}]
    directory = input("Code Directory: ")
    tknizer = Tokenizer()
    combined = tknizer.print_file_contents(directory)
    default_chunk_size = chunk_size = 260000
    print('Size:',len(combined))
    print('Chunks:',math.ceil(len(combined)/chunk_size))
    print('Code tokenized\nSetting up AI...')
    i = 0
    repeat = reduce_chunk = False
    iterations = 1
    while i<len(combined):
        if not repeat:
            if i+chunk_size<=len(combined):
                messages.append({'role': 'user', 'content': combined[i:i+chunk_size]})
            else:
                messages.append({'role': 'user', 'content': combined[i:]})
        
        response = chat_with_gpt(messages)
        print("Response",response)

        if type(response) == str:
            print(response)
            i+=chunk_size
            messages.append({'role': 'assistant', 'content': response})
            print("Chunk no: ",i//chunk_size," out of",math.ceil(len(combined)/chunk_size))
            repeat = False
            reduce_chunk = False
            chunk_size = default_chunk_size
        else:
            sleep_time = 30
            print('\n\nError encountered:',response[1])
            index = response[1].find('Please try again in ')+20
            error = response[1].find('However, your messages resulted in ')+20
            if index!=-1:
                stime = ''
                while response[1][index]!='s':
                    stime+=response[1][index]
                    index+=1
                sleep_time = math.ceil(float(stime))
            elif error!=-1:
                chunk_size = chunk_size//2
                reduce_chunk = True
                sleep_time = 0.1
                
            print('\nRetrying chunk',i//chunk_size,'in',sleep_time,'seconds.\n')
            time.sleep(sleep_time)
            repeat = True

    print('- '*20)
    print('Directory injestion complete')
    print('- '*20)

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
        messages.append({'role': 'user', 'content': user_input})
        response = chat_with_gpt(messages)
        messages.append({'role': 'assistant', 'content': response})
        print(f"\nGPT: {response}")
        print('- '*20)

if __name__ == "__main__":
    main()