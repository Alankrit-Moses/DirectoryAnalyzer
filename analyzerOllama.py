import ollama
from tokenizer import Tokenizer
import os

#Adjust according to the model required
model_name = 'llama3.1:8b'
context_length = 120000     # This is the input context length. Leave enough for output generation


# Set API endpoint and headers
api_endpoint = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}

def chunk_create(string,ctxt_lngth,bffer):
    array = []
    i=0
    while i<len(string):
        if i+ctxt_lngth>=len(string):
            array.append(string[i:])
            break
        else:
            array.append(string[i:i+ctxt_lngth])
        i+=(ctxt_lngth-bffer)
    return array

directories = []
while True:
    directory = input('Enter Directory (Press "q" if no more to provide): ').strip()
    if directory!='q' and directory!='Q':
        directories.append(directory)
    else:
        break

print(directories)
tknizer = Tokenizer()

saveDirectory = input('Directory to save responses (Press "n" if not saving): ').strip()

directoryContents = []
for drctry in directories:
    file_content = tknizer.process_file_contents(drctry)
    directoryContents.append(file_content)

buffer = 10000
context = []

for file_content in directoryContents:
    context+=chunk_create(file_content,context_length,buffer)

while True:
    print('- '*50)
    prompt = input("\nQuestion: ")
    responses = []
    i = 1
    for c in context:
        print('Analyzing chunk '+str(i)+":\n")
        messages = [{'role': 'user', 'content': c+' '+prompt+' '+" Give answer with respect to the messages provided"}]

        # Make the request using the Ollama library
        response = ollama.chat(model=model_name, messages=messages, stream=True,)

        print(". . . . . . . . R E S P O N S E   "+str(i)+" . . . . . . . . \n")
        
        res = ""
        for chunk in response:
            print(chunk['message']['content'], end='', flush=True)
            res += chunk['message']['content']

        #Storing the responses
        responses.append(res)

        # Saving the responses
        if saveDirectory!='N' and saveDirectory!='n':
            path = os.path.join(saveDirectory,("Response "+str(i)+".txt"))
            with open(path,'w') as file:
                file.write(res)
        i+=1

    print('\n\nResponses received...')
    print('\n\n...CONDENSING RESPONSES...')
    while len(responses)>1:
        responses = ' '.join(responses)
        responses = chunk_create(responses,context_length,buffer)
        new_responses = []
        for response in responses:
            message = response+" Analyze the response, summarize and give the answer to the prompt: "+prompt
            responses = ollama.chat(model=model_name, messages=messages,)
            new_responses.append(responses['message']['content'])
        responses = new_responses

    print('\n. . . . . . . . F I N A L   R E S P O N S E . . . . . . . .\n'+responses[0])
    if saveDirectory!='N' and saveDirectory!='n':
            path = os.path.join(saveDirectory,("Final_Response.txt"))
            with open(path,'w') as file:
                file.write(res)