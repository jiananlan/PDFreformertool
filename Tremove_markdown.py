import markdown
from bs4 import BeautifulSoup


def md_to_text(md_string):
    # 先将 Markdown 转换为 HTML
    if md_string:
        html = markdown.markdown(md_string)
        # 再用 BeautifulSoup 提取纯文本
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text()
    elif md_string==None:
        return None
    else: return md_string


if __name__ == "__main__":
    md_text = """
        F/CTL 通常指 **飞行控制系统（Flight Control System）**，常见于航空领域，主要涉及飞机姿态、航向和高度的操控。具体可能包括：
        
        * **组成部分:** 操纵杆、方向舵、副翼、升降舵等机械结构，以及电传操纵（Fly-by-Wire）、自动驾驶等电子系统。
        * **功能:** 通过调整飞行控制面（舵面）确保飞机的稳定性、机动性和安全性。
        * **应用:** 民用客机、军用飞机、无人机等各类航空器。
        
        **其他可能的含义（需结合上下文判断）:**
        * **流量控制（Flow Control）:**  工业或计算机系统中对流体或数据流的管控。
        * **燃料控制（Fuel Control）:**  发动机或动力系统中对燃料供给的调节。
        
        建议提供更多背景信息以便更精准地解释该缩写。"""
    plain_text = md_to_text(md_text)
    print(plain_text)  # 输出: Markdown 格式 链接
