import asyncio
import openai
from tqdm.asyncio import tqdm
import T5_a
import rich
import Tconfig

client = openai.AsyncOpenAI(
    api_key=Tconfig.configuration["api_key"], base_url=Tconfig.configuration["api_url"]
)
error_count = 0
error_item = []
same_count = 0
messages = [{"role": "user", "content": f"你好呀"}]


async def call_api(prompt):
    global error_count, same_count, error_item
    result_from_hdf5 = T5_a.query_key(prompt)
    print(prompt)
    if T5_a.key_exs(prompt):
        return result_from_hdf5
    try:
        response = await client.chat.completions.create(
            model=Tconfig.configuration["model"],
            messages=[
                {
                    "role": "user",
                    "content": f"翻译为中文，注意：这是一段涵{Tconfig.configuration['theme']}{Tconfig.configuration['style']}；仅输出译文（说明文字绝对不输出）！（若为代码则保留）纯文本格式：\n"
                    + prompt,
                }
            ],
            temperature=1.3,
            timeout=190000,
        )
        if prompt == response.choices[0].message.content:
            same_count += 1
        T5_a.add_key_value(key=prompt, value=response.choices[0].message.content)
    except Exception as e:
        rich.print(f"🤢🤢🤢[green]发生错误[/green]🤢🤢🤢 {e}")
        error_count += 1
        error_item.append(prompt)
        return prompt
    return response.choices[0].message.content


async def main(prompts):
    global error_item, error_count
    error_item = []
    error_count = 0
    tasks = [call_api(prompt) for prompt in prompts]
    results = []

    for result in tqdm(
        asyncio.as_completed(tasks), desc="并发请求翻译", total=len(tasks)
    ):
        results.append(await result)


async def run(prompts):
    prompts1 = [p for p in prompts if not T5_a.key_exs(p)]
    print(f"共计{len(prompts)}个进行处理,{len(prompts) - len(prompts1)}个输入已经存储")
    result = await main(prompts=prompts1)
    while error_item:
        rich.print(
            "👆🏻" * 50000
            + f"There are {error_count} error in {len(prompts) - len(prompts1)}, Retry now!\n"
            * 500
        )
        prompts1 = error_item
        result = await main(prompts=prompts1)
    if not error_count:
        rich.print(":smile:" * 50000 + "No error over there!\n" * 500)
    if same_count:
        rich.print(
            "💩" * 50000 + f"There are {same_count} Same inputs->outputs\n" * 500
        )
    return result


if __name__ == "__main__":
    raw_prompts = ["嘻嘻", "好好写一首小诗"]
    prompts = [p for p in raw_prompts if not T5_a.key_exs(p)]
    print(
        f"共计{len(raw_prompts)}个进行处理,{len(raw_prompts) - len(prompts)}个输入已经存储"
    )
    asyncio.run(main(prompts=prompts))
