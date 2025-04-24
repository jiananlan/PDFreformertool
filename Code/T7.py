def sort_pdf_blocks(blocks):
    """
    按照 PDF 文章顺序（从上到下，左到右）排序块
    :param blocks: List[Dict]，每个块是 {'text': str, 'x': float, 'y': float, 'width': float, 'height': float}
    :return: 排序后的文本字符串
    """
    # 1. 按 y 轴排序，确保整体从上到下
    blocks.sort(key=lambda b: b["y"])

    # 2. 逐行排序
    sorted_lines = []
    current_line = []

    def flush_line():
        """按 x 轴排序当前行的块，并加入到结果中"""
        if current_line:
            current_line.sort(key=lambda b: b["x"])  # 按 x 排序
            sorted_lines.append(" ".join(b["text"] for b in current_line))
            current_line.clear()

    line_threshold = 10  # 允许的 y 轴误差，避免相邻行被误判为同一行
    prev_y = None

    for block in blocks:
        if prev_y is None or abs(block["y"] - prev_y) > line_threshold:
            flush_line()
            prev_y = block["y"]
        current_line.append(block)

    flush_line()  # 处理最后一行

    return "\n".join(sorted_lines)


# 示例输入
blocks = [
    {"text": "world!", "x": 90, "y": 100, "width": 40, "height": 10},
    {"text": "Hello", "x": 50, "y": 100, "width": 30, "height": 10},
    {"text": "This", "x": 50, "y": 120, "width": 30, "height": 10},
    {"text": "a", "x": 110, "y": 120, "width": 10, "height": 10},
    {"text": "is", "x": 85, "y": 120, "width": 20, "height": 10},
    {"text": "test.", "x": 130, "y": 120, "width": 30, "height": 10},
]

# 运行排序算法
sorted_text = sort_pdf_blocks(blocks)
print(sorted_text)
