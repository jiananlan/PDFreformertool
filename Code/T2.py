from openai import OpenAI
import rich


def run_ds_translate(
    raw_paragraph, model_of_translate="reasoner", topic="计算机技术和科学技术"
):
    def process_result(p_result):
        p_result = p_result.split("#$@#")
        trans = [_content for _content in p_result[0].split("\n") if _content != ""]
        key = p_result[1].split("\n")
        key_list = {}
        for i in key:
            try:
                if "%^&#" in i:
                    t = i.split("%^&#")
                else:
                    t = i.split("-")
                key_list[t[0]] = t[1]
            except IndexError:
                pass
        return trans, key_list

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
            "role": "system",
            "content": f"翻译为中文，注意：这是一段涵盖{topic}的文章；翻译准确，不要凭空增加含义；最后展示出你的文中各科学名词的译得名称和原英文名称的对照（仅限重要名词需对照），必须前后一致 "
            f"输出为两部分 用字符#$@#隔开，对照表原名和译名由字符%^&#隔开,一对键-值间占一行",
        }
    ]
    if model_of_translate == "reasoner":
        messages = [
            {
                "role": "user",
                "content": f"翻译为中文，注意：这是一段涵盖{topic}的文章；翻译准确，不要凭空增加含义；最后展示出你的文中各科学名词的译得名称和原英文名称的对照（仅限重要名词需对照），必须前后一致 "
                f"输出为两部分 用字符#$@#隔开，对照表原名和译名由字符%^&#隔开,一对键-值间占一行",
            },
            {"role": "assistant", "content": "好的"},
        ]

    while True:
        user_input = raw_paragraph
        if model_of_translate == "chat" and messages[-1]["role"] != "user":
            messages.append({"role": "user", "content": user_input})
        elif model_of_translate == "reasoner" and messages[-1]["role"] != "user":
            messages.append(
                {
                    "role": "user",
                    "content": f"翻译为中文，注意：这是一段涵盖{topic}的文章；翻译准确，不要凭空增加含义；最后展示出你的文中各科学名词的译得名称和原英文名称的对照（仅限重要名词"
                    f"需对照），必须前后一致输出为两部分 用字符#$@#隔开，对照表原名和译名由字符%^&#隔开,一对键-值间占一行"
                    + user_input,
                }
            )
        try:
            response = client.chat.completions.create(
                model=f"deepseek-{model_of_translate}",
                messages=messages,
                temperature=1.3,
                stream=True,
                timeout=None,
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
                return tuple([raw_sentence] + list(process_result(ai_response)))
            else:
                rich.print("[red]翻译失败，正在重试[/red]")
        except Exception as e:
            rich.print(f"[red]\n发生错误: {str(e)}[/red]")
            break


class TranslateResult:
    raw_content: list
    trans_content: list
    key_list: dict

    def __init__(self, *args):
        if len(args) == 1:
            self.trans_content = args[0]
        elif len(args) == 2:
            self.raw_content = args[0]
            self.trans_content = args[1]
        elif len(args) == 3:
            self.raw_content = args[0]
            self.trans_content = args[1]
            self.key_list = args[2]

    def __str__(self):
        return (
            f"Translate_result(\n    Raw content {self.raw_content};\n    Trans content {self.trans_content};\n    "
            f"Key list {self.key_list})"
        )

    def load_from_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            read_result = [line.replace("\n", "") for line in file.readlines()]
        if len(read_result) == 1:
            self.trans_content = eval(read_result[0])
        elif len(read_result) == 2:
            self.raw_content = eval(read_result[0])
            self.trans_content = eval(read_result[1])
        elif len(read_result) == 3:
            self.raw_content = eval(read_result[0])
            self.trans_content = eval(read_result[1])
            self.key_list = eval(read_result[2])


if __name__ == "__main__":
    with open("Input", "r", encoding="utf-8") as f:
        p = [x.replace("\n", "") for x in f.readlines() if x != "\n"]
    input_content = "\n".join([t for t in p if t != ""])
    result = run_ds_translate(input_content, model_of_translate="chat")
    print()
    if result:
        r = TranslateResult(*result)
        print(r)
