import asyncio
from openai import AsyncAzureOpenAI
from tqdm.asyncio import tqdm
import Tprompt
import T5_a

endpoint = "Change to yours"
deployment = "gpt-4.1"
api_key = "change as your key"
api_version = "2024-12-01-preview"

messages_list = [
    '''114, vacate right.''',
]
error_list = list


async def ask(client, user_content):
    global error_list
    try:
        response = await client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": Tprompt.get_full_prompt(user_content)}]
        )
        result = response.choices[0].message.content
        T5_a.add_key_value(key=user_content, value=result)
        return result
    except Exception as e:
        error_list.append(user_content)
        return f'error occurs: {e}'


async def main(raw_content_list):
    global error_list
    r = []
    for c in raw_content_list:
        if not T5_a.key_exs(c):
            r.append(c)
    error_list = r
    print(r)
    while error_list:
        error_list_backup = error_list.copy()
        error_list = []
        client = AsyncAzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version
        )

        tasks = [ask(client, content) for content in error_list_backup]

        results = []
        for coro in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc="Processing(ChatGPT4.1 specialized)"):
            res = await coro
            results.append(res)

        for question, answer in zip(error_list_backup, results):
            print(f"Translate raw: {question}\nTranslater: {answer}\n{'=' * 40}")
        if error_list:
            print(f'There are {len(error_list)} error, i will retry now if error.')
        else:
            print('There are no error.')


if __name__ == '__main__':
    asyncio.run(main(messages_list))
