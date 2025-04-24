from openai import OpenAI
import rich
import T5


def run_ds_translate(
    raw_paragraph, model_of_translate="reasoner", topic="计算机技术和科学技术"
):
    if T5.query_key(raw_paragraph):
        raw_sentence = [lines for lines in raw_paragraph.split("\n") if lines != ""]
        rich.print(
            f'[cyan]{raw_paragraph[:50].replace('\n', '  ')}... [bold]已经存在于数据库中[/bold][/cyan]'
        )
        return [raw_sentence], T5.query_key(raw_paragraph).split("\n")

    def process_result(p_result):
        return [line for line in p_result.split("\n") if line != ""]

    rich.print(
        f'[green][bold]模型 {model_of_translate} 正在翻译[/bold] {raw_paragraph[:50].replace('\n', '  ')}...[/green]'
    )
    rich.print(f"[yellow]{'─' * 20}开始生成翻译内容{'─' * 20}[/yellow]")
    client = OpenAI(
        api_key="Change as your api key",
        base_url="https://api.deepseek.com",
    )

    messages = [
        {
            "role": "user",
            "content": f"翻译为中文，注意：这是一段涵盖{topic}的文章；仅输出译文（说明文字绝对不输出）！（若为代码则保留）纯文本格式：\n"
            + raw_paragraph,
        }
    ]
    while True:
        try:
            response = client.chat.completions.create(
                model=f"deepseek-{model_of_translate}",
                messages=messages,
                temperature=1.3,
                stream=True,
                timeout=50000,
            )

            full_response = []

            for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    print(content, end="", flush=True)
                    full_response.append(content)

            ai_response = "".join(full_response)
            print()
            rich.print(f"[yellow]{'─' * 20}生成翻译内容完毕{'─' * 20}[/yellow]")
            if ai_response != "":
                raw_sentence = [
                    lines for lines in raw_paragraph.split("\n") if lines != ""
                ]
                rich.print(f"[cyan]{'─' * 20}正在写入数据库中{'─' * 20}[cyan]")
                T5.add_key_value(
                    key=raw_paragraph, value="\n".join(process_result(ai_response))
                )
                return [raw_sentence], list(process_result(ai_response))
            else:
                rich.print("[red]翻译失败，正在重试 (Timeout)[/red]")
        except Exception as e:
            rich.print(f"[red]\n发生错误: {str(e)}[/red]")
            break


class TranslateResult:
    raw_content: list
    trans_content: list

    def __init__(self, *args):
        if len(args) == 1:
            self.trans_content = args[0]
        elif len(args) == 2:
            self.raw_content = args[0]
            self.trans_content = args[1]

    def __str__(self):
        return f"Translate_result(\n    Raw content {self.raw_content};\n    Trans content {self.trans_content};\n    "

    def load_from_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            read_result = [line.replace("\n", "") for line in file.readlines()]
        if len(read_result) == 1:
            self.trans_content = eval(read_result[0])
        elif len(read_result) == 2:
            self.raw_content = eval(read_result[0])
            self.trans_content = eval(read_result[1])


if __name__ == "__main__":
    with open("input.txt", "r", encoding="utf-8") as f:
        p = [x.replace("\n", "") for x in f.readlines() if x != "\n"]
    input_content = "\n".join([t for t in p if t != ""])
    result = run_ds_translate(input_content, model_of_translate="reasoner")
    print()
    if result:
        r = TranslateResult(*result)
        print(r)
