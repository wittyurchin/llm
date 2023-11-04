import openai
import os

openai.api_key = "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"

def llm_response(prompt):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role':'user','content':prompt}],
        temperature=0
    )
    return response.choices[0].message['content']


prompt = '''
    Classify the following review 
    as having either a positive or
    negative sentiment:

    The banana pudding was relly tasty!
'''

response = llm_response(prompt)
print(response)
