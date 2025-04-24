from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm


# 加载模板


def main_run(file_name, second):
    print("here1")
    doc = DocxTemplate(file_name)
    print("here2")
    # 创建图片对象，设定大小
    print("here3")
    # 填充数据
    import os

    ld = os.listdir(".\\extracted_images")
    context = dict()

    def the_size(filename, pic_path):
        from PIL import Image

        print(filename)
        p = []
        if os.path.exists("size.txt"):
            with open("size.txt", "r") as f:
                p = f.readlines()
        size_dict = {}
        for line in p:
            rid, x, y = eval(line)
            size_dict[rid] = (x, y)
        if filename not in size_dict.keys():
            print(f"🤎 this image was not registered {filename};{pic_path}")
            A4_WIDTH_MM = 210  # A4纸的宽度（毫米）
            MAX_WIDTH_MM = A4_WIDTH_MM * 0.8  # 最大允许宽度（80%）

            img = Image.open(pic_path)
            dpi = img.info.get("dpi", (96, 96))[0]  # 取 x 方向 DPI
            width_mm = (img.width / dpi) * 25.4
            height_mm = (img.height / dpi) * 25.4

            # 如果图片宽度超过最大限制，则缩放
            if width_mm > MAX_WIDTH_MM:
                scale_factor = MAX_WIDTH_MM / width_mm
                width_mm = MAX_WIDTH_MM
                height_mm *= scale_factor  # 高度按比例缩放

            return width_mm, height_mm
        else:
            print(f"🧡 this image has been registered {filename};{pic_path}")
            EMU_PER_INCH = 914400  # 1 英寸 = 914400 EMU
            MM_PER_INCH = 25.4  # 1 英寸 = 25.4 mm
            target_width_emu = size_dict[filename][0]
            target_height_emu = size_dict[filename][1]
            width_mm = (target_width_emu / EMU_PER_INCH) * MM_PER_INCH
            height_mm = (target_height_emu / EMU_PER_INCH) * MM_PER_INCH

            return width_mm, height_mm

    for file in ld:
        x, y = the_size(file, os.path.join(".\\extracted_images", file))
        context[file.split("\\")[-1].split(".")[0]] = InlineImage(
            doc,
            os.path.join(".\\extracted_images", file),
            width=Mm(x),
            height=Mm(y),
        )
    print("here4")
    # 渲染文档
    doc.render(context)
    print("here5")
    # 保存结果
    doc.save(second)
