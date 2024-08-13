# import ollama

# messages = []
# messages.append({'role': 'system', 'content': "Keep generating a garbage message until you can't anymore."})

# params = {
#     "model": "llama3.1",
#     'messages': messages
# }
# import ollama

# # Initialize messages
# messages = []
# messages.append({'role': 'system', 'content': "How to make a milkshake?"})

# # Define the parameters for the streaming request
# params = {
#     'model': 'llama3.1',
#     'messages': messages,
#     'stream': True  # Enable streaming
# }

# # Make the request using the Ollama library with streaming
# response_stream = ollama.chat(**params)

# # Process the streamed response
# for chunk in response_stream:
#     print(chunk['message']['content'], end='', flush=True)


# # curl http://localhost:11434/api/generate -d '{"model": "llama3.1:8b", "prompt": "Why is the sky blue?" }'


import ollama

stream = ollama.chat(
    model='llama3.1:8b',
    messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)

# Use this file to see if ollama library and llama extensions are installed properly