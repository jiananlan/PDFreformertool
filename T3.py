import fitz
from copy import deepcopy
import time


class Block:
    text: str
    font: str
    size: float
    pos: tuple
    page_num: int
    center_pos: tuple

    def __init__(self, **kwargs):
        self.text = kwargs["text"]
        self.font = kwargs["font"]
        self.size = kwargs["size"]
        self.pos = kwargs["pos"]
        self.page_num = kwargs["page_num"]
        self.center_pos = (
            (kwargs["pos"][0] + kwargs["pos"][2]) / 2,
            (kwargs["pos"][1] + kwargs["pos"][3]) / 2,
        )

    def __str__(self):
        return f"[Block]│{self.page_num} -> {self.text[:70]} ...{self.center_pos}"

    def __eq__(self, other):
        if self.page_num == other.page_num:
            if (
                self.center_pos[0] == other.center_pos[0]
                and self.center_pos[1] == other.center_pos[1]
            ):
                if self.text == other.text:
                    return True
        return False


class paragraph:
    text: str
    first_block: Block
    type: int = 1
    page_num: int
    allow_multi_line: bool = False

    def __init__(self, Block: Block, page_num: int):
        self.text = Block.text
        self.first_block = Block
        self.page_num = page_num

    def __str__(self):
        return f"段落[{self.page_num + 1}]{self.allow_multi_line}│ {self.text}"

    def __eq__(self, other):
        if self.page_num == other.page_num:
            if self.first_block == other.first_block:
                if self.text == other.text:
                    return True
        return False

    def add_Line(self, other_block: Block):
        if abs(self.first_block.pos[1] - other_block.pos[1]) > 1.5:
            self.allow_multi_line = True
            self.text += " " + other_block.text


def compare_2_blocks(block1, block2):
    """
    Compare two blocks
    :param block1: Block 1
    :param block2: Block 2
    :return: True - similar
             False - not similar
    """
    if block1.page_num != block2.page_num:
        return False
    if block1.pos[2] == block2.pos[2]:
        return True
    if (
        abs(block1.center_pos[1] - block2.center_pos[1]) <= 0.7
        or block1.pos[1] == block2.pos[1]
    ):
        return True
    if block1.font == block2.font:
        return True
    if block1.text == block2.text:
        return True
    return False


def mode(data):
    """计算列表data中的众数，并返回包含所有众数的列表"""
    if not data:
        return []  # 列表为空时返回空列表

    counts = {}
    for num in data:
        counts[num] = counts.get(num, 0) + 1  # 统计每个数字出现的次数

    max_count = max(counts.values())  # 找出最大的出现次数

    modes = [k for k, v in counts.items() if v == max_count]  # 收集所有众数

    return modes


def two_similar_height(block, block_list):
    for b in block_list:
        if (
            abs(block.pos[1] - b.pos[1]) <= 0.6
            and abs(block.page_num - b.page_num) <= 1
        ):
            return True
    return False


yemei_list = []


def detect_yemei(block, page_block_list):
    global yemei_list
    temp_pl = deepcopy(page_block_list)
    if two_similar_height(block, yemei_list):
        yemei_list.append(block)
        return True
    if block in temp_pl:
        temp_pl.remove(block)
    for b in temp_pl:
        if b.pos[3] < block.pos[3] or b.pos[1] < block.pos[1]:
            return False
        if block.pos[1] > 50:
            return False
    yemei_list.append(block)
    return True


def sort_pdf_blocks(blocks):
    """
    按照 PDF 文章顺序（从上到下，左到右）排序块
    :param blocks: List[Dict]，每个块是 {'text': str, 'x': float, 'y': float, 'width': float, 'height': float}
    :return: 排序后的 blocks 列表
    """
    # 1. 按 y 轴排序，确保整体从上到下
    blocks.sort(key=lambda b: b.center_pos[1])

    # 2. 逐行排序
    sorted_blocks = []
    current_line = []

    def flush_line():
        """按 x 轴排序当前行的块，并加入到最终结果中"""
        if current_line:
            current_line.sort(key=lambda b: b.center_pos[0])  # 按 x 排序
            sorted_blocks.extend(current_line)
            current_line.clear()

    line_threshold = 3  # 允许的 y 轴误差，避免相邻行被误判为同一行
    prev_y = None

    for block in blocks:
        if prev_y is None or abs(block.center_pos[1] - prev_y) > line_threshold:
            flush_line()
            prev_y = block.center_pos[1]
        current_line.append(block)

    flush_line()  # 处理最后一行

    return sorted_blocks


def get_all_block_in_one_page(page_num, all_page_list):
    return [block for block in all_page_list if block.page_num == page_num]


def extract_text_and_font_info(pdf_path):
    blist = []
    doc = fitz.open(pdf_path)
    for page_num in range(623):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        blist.append(
                            Block(
                                text=span["text"],
                                font=span["font"],
                                size=span["size"],
                                pos=span["bbox"],
                                page_num=page_num,
                            )
                        )
    return blist


pdf_path = r"C:\Users\anlan\Desktop\科研入门培养方案\flash4_ug_4p62.pdf"  # 替换为你的PDF文件路径
r = extract_text_and_font_info(pdf_path)
block_index = 0
backup = r[0]
flag = False
last_size = r[0].size
"""while block_index < len(r):
    try:
        if compare_2_blocks(r[block_index], r[block_index + 1]):
            if backup[-1] != ' ' and r[block_index].text[0] != ' ':
                print('', r[block_index].text, end='')
            else:
                print(r[block_index].text, end='')
        else:
            print(r[block_index].text)
            if r[block_index + 1].text[0] != ' ':
                print('New Block│ ', end='')
            else:
                print('New Block│', end='')
    except IndexError:
        print(r[block_index].text, end='')
    backup = r[block_index].text
    block_index += 1"""

total_index = 0
paragraph_list = [paragraph(r[0], 0)]
for page_index in range(623):
    print("\n[", page_index, "]")
    block_index = 0
    t = get_all_block_in_one_page(page_index, r)
    t = sort_pdf_blocks(t)
    font_size_list = [x.size for x in t]
    mode_font_size = mode(font_size_list)
    for block in t:
        if detect_yemei(block, t):
            print(f"[页眉  {block.text}]")
        else:
            if block.size in mode_font_size:
                print(block.text, end=" ")
            else:
                if last_size == block.size:
                    print(block.text, end=" ")
                else:
                    print(f"[/大小{last_size:.1f}]", end=" ")
                    print(f"[大小{block.size:.1f}]{block.text}", end=" ")
                    last_size = block.size

    """
    if len(t) > 0:
        backup = t[0]
    for block in t:
        if detect_yemei(block, t):
            print()
            print(f'页眉[{page_index + 1}]│{block.text}')
        else:
            if flag:
                paragraph_list.append(paragraph(block, page_index))
                flag = False
            try:
                if compare_2_blocks(r[total_index], r[total_index + 1]) and r[total_index].page_num == r[
                    total_index + 1].page_num:
                    paragraph_list[-1].add_Line(r[total_index])
                else:
                    # paragraph_list[-1].add_Line(backup)
                    print(paragraph_list[-1])
                    flag = True
            except IndexError:
                print(r[total_index].text, end='')
            backup = r[total_index]
        block_index += 1
        total_index += 1
    if len(t) > 0:
        paragraph_list[-1].add_Line(t[-1])"""
print()
print(f"处理时间│{time.process_time()}")
print(mode_font_size)
