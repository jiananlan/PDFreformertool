from openai import OpenAI

client = OpenAI(
    api_key="Change as your api key", base_url="https://api.deepseek.com"
)

# 初始化对话历史（包含系统消息）
messages = []
while True:
    # 获取用户输入
    user_input = """github 新建一个和自己昵称相同的仓库有什么用
"""
    # 退出条件
    if user_input.lower() in ["exit", "quit"]:
        print("对话结束")
        break

    # 添加用户消息到历史
    messages.append({"role": "user", "content": user_input})

    try:
        # 发起流式请求
        response = client.chat.completions.create(
            model="deepseek-reasoner",  # 可替换为deepseek-chat，v3模型，当前r1
            messages=messages,  # temperature=1.3,
            stream=True,
            timeout=500000,  # 启用流式输出,t
        )

        # 初始化回复收集
        full_response = []
        print("\nAssistant: ", end="", flush=True)  # 先打印前缀

        # 实时处理流式响应
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:  # 过滤空内容
                print(content, end="", flush=True)  # 逐字打印
                full_response.append(content)

        # 添加完整回复到历史
        ai_response = "".join(full_response)
        messages.append({"role": "assistant", "content": ai_response})
        print()
        print(messages)  # 换行
        print(ai_response)
        break

    except Exception as e:
        print(f"\n发生错误: {str(e)}")
        break
