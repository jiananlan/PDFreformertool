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
same_count = 0
messages = [{"role": "user", "content": f"你好呀"}]
error_item = []


async def call_api(prompt, type=1):
    """

    :param prompt:
    :param type: 1 正常翻译
                2 简单翻译
    :return:
    """
    global error_item
    if len(prompt.replace(" ", "")) < 6:
        return prompt
    global error_count, same_count
    result_from_hdf5 = T5_a.query_key(prompt)
    print(prompt)
    if T5_a.key_exs(prompt):
        return result_from_hdf5
    try:
        if type == 1:
            response = await client.chat.completions.create(
                model=Tconfig.configuration["model"],
                messages=[
                    {
                        "role": "user",
                        "content": f"翻译为中文，注意：这是一段涵{Tconfig.configuration['theme']}{Tconfig.configuration['style']}；仅输出译文！禁止输出解释、描述或者附加内容：\n"
                        + prompt,
                    }
                ],
                temperature=1.3,
                timeout=90000,
            )
        else:
            response = await client.chat.completions.create(
                model=Tconfig.configuration["model"],
                messages=[
                    {
                        "role": "user",
                        "content": f"将下面内容翻译为中文，{Tconfig.configuration['theme']}，仅输出译文。禁止输出解释、描述或者附加内容：\n"
                        + prompt,
                    }
                ],
                temperature=1.3,
                timeout=90000,
            )
        if prompt == response.choices[0].message.content:
            same_count += 1
        print(
            f"👉🏻👉🏻👉🏻[green]翻译结果[/green]👈🏻👈🏻👈🏻{response.choices[0].message.content}"
        )
        T5_a.add_key_value(key=prompt, value=response.choices[0].message.content)
    except Exception as e:
        rich.print(f"🤢🤢🤢[green]发生错误[/green]🤢🤢🤢 {e}")
        error_item.append((prompt, type))
        error_count += 1
        return prompt
    return response.choices[0].message.content


async def main(prompts_s, prompts_f):
    global error_count, error_item, same_count
    error_item = []
    error_count = 0
    tasks = [call_api(prompt, type=2) for prompt in prompts_s]
    tasks += [call_api(prompt, type=1) for prompt in prompts_f]
    results = []

    for result in tqdm(
        asyncio.as_completed(tasks), desc="并发请求翻译（表格部分）", total=len(tasks)
    ):
        results.append(await result)


async def run(prompts):
    """

    :param prompts: (prompts_simple,prompts_full)
    :return:
    """
    simple = prompts[0]
    full = prompts[1]
    prompts1 = [p for p in simple if not T5_a.key_exs(p)]
    prompts2 = [p for p in full if not T5_a.key_exs(p)]
    print(
        f"共计{len(simple + full)}个进行处理,{len(simple + full) - len(prompts1 + prompts2)}个输入已经存储"
    )
    result = await main(prompts_s=prompts1, prompts_f=prompts2)
    while error_count:
        prompts1, prompts2 = [], []
        for prompt, type in error_item:
            prompts1.append(prompt) if type == 1 else prompts2.append(prompt)
        result = await main(prompts_s=prompts1, prompts_f=prompts2)
        rich.print(
            "👆🏻" * 50000
            + f"There are {error_count} error in {len(prompts) - len(prompts1)}, Retry now!\n"
            * 500
        )

    if not error_count:
        rich.print(":smile:" * 50000 + "No error over there!\n" * 500)
    if same_count:
        rich.print(
            "💩" * 50000 + f"There are {same_count} Same inputs->outputs\n" * 500
        )
    return result


if __name__ == "__main__":
    raw_prompts = ["ILS approach", "V1"]
    prompts = [p for p in raw_prompts if not T5_a.key_exs(p)]
    print(
        f"共计{len(raw_prompts)}个进行处理,{len(raw_prompts) - len(prompts)}个输入已经存储"
    )
    asyncio.run(main(prompts_s=prompts, prompts_f=[]))
