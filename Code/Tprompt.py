import Tconfig

prompt = '''你是一名专业的翻译人员。请将以下内容准确、自然地翻译为#%#，并只输出译文，不要输出任何说明、解释或原文。这是&#&#&#的一个段落。
原文：\n%#%
'''


def get_full_prompt(raw_content):
    p = prompt.replace('%#%', raw_content).replace('#%#', Tconfig.configuration['target_language'])
    return p.replace('&#&', Tconfig.configuration["theme"]).replace('#&#', Tconfig.configuration["style"])


if __name__ == '__main__':
    print(get_full_prompt('hello world!'))
