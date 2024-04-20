from openai import OpenAI
import json

client = OpenAI()

prompt = "Order 36 Apples from PS 91 Wazidpur, Noida, sector 135"
# prompt = "hello how are you?"

function = [
    {
        'name': 'fruit_list',
        'description': 'Get the fruits information and address',
        'parameters': {
            'type': 'object',
            'properties': {
                'name': {
                    'type': 'string',
                    'description': 'Name of the fruit'
                },
                'count': {
                    'type': 'integer',
                    'description': 'Count of number of fruits'
                },
                'address': {
                    'type': 'string',
                    'description': 'address of the fruit'
                }
            }
        }
    }
]

def fruit_list(name, count, address):
    return f"You ordered {count} {name}s, its being shipped to your address {address}"

response = client.chat.completions.create(
    model= 'gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': prompt}],
    functions=function,
    function_call='auto'
)

response_message = response.choices[0].message

if dict(response_message).get('function_call'):
    # Which funtion was called
    function_called = response_message.function_call.name

    # Extracting the arguments
    function_args = json.loads(response_message.function_call.arguments)

    #Function names
    available_functions = {
        "fruit_list": fruit_list
    }

    function_to_call = available_functions[function_called]
    response_message = function_to_call(*list(function_args.values()))

else:
    response_message = response_message.content

print(response_message)

# Loading the response as a JSON object
'''json_response = json.loads(response.choices[0].message.function_call.arguments)
json_response2 = response

print('#'*500)
print(json_response)
print('#'*500)
print(json_response2)'''
