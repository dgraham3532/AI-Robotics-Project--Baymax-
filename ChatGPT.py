import os
from openai import OpenAI


# OpenAIModel = "gpt-3.5-turbo-instruct"
OpenAIModel = "gpt-3.5-turbo"
chat_question = "Hello how are you doing today?"

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OpenAI_API_KEY"),
)
print(client.api_key)
completion = client.chat.completions.create(
          #model="gpt-4",
          model = OpenAIModel,
          messages= chat_question
        )

        # Process the answer
openai_answer = completion.choices[0].message.content
print(f"[green]\n{openai_answer}\n")


