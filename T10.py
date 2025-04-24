import zipfile
import os
from docx import Document
from io import BytesIO
from PIL import Image
import re

if os.path.exists("size.txt"):
    os.remove("size.txt")


def extract_images(docx_path, output_dir):
    with zipfile.ZipFile(docx_path, "r") as docx:
        image_files = [
            file for file in docx.namelist() if file.startswith("word/media/")
        ]

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for image_file in image_files:
            img_data = docx.read(image_file)
            image_stream = BytesIO(img_data)

            try:
                img = Image.open(image_stream)
                image_format = img.format.lower()

                image_name = os.path.basename(image_file)
                img_path = os.path.join(output_dir, image_name)
                img.save(img_path, format=image_format.upper())

            except Exception as e:
                print(e)


def get_rid(txt):
    pattern = r'r:embed="(.*?)"/>'
    matches = re.findall(pattern, txt)
    return matches


def get_size(text):
    pattern = r'<wp:extent cx="([^"]+)" cy="([^"]+)"/>'
    matches = re.findall(pattern, text)
    matches = [int(m) for m in list(matches[0])]
    print(matches)
    return matches


def read_word_docx(docx_path):
    import T13

    result_text = ""
    result_image = []
    doc = Document(docx_path)
    count = 1
    t = T13.extract_image_relationships(docx_path)

    # 遍历所有段落，寻找内嵌式图片
    for idx, paragraph in enumerate(doc.paragraphs):
        result_text += paragraph.text + "\n"

        char_count = 0  # 记录段落中字符的累计计数

        # 遍历段落中的每个 run（字符、文本或图片）
        for run_idx, run in enumerate(paragraph.runs):
            run_text_length = len(run.text)  # 获取当前run中的文本长度

            if "a:graphic" in run._r.xml:
                print(
                    f"[{idx + 1, count}]",
                    get_rid(run._r.xml),
                )  # T13.t[get_rid(run._r.xml)[0]])
                print(run._r.xml)
                sz = get_size(run._r.xml)
                if get_rid(run._r.xml)[0] in t:
                    png = t[get_rid(run._r.xml)[0]]
                else:
                    png = "image1.png"
                with open("size.txt", "a+") as f:
                    f.write(f'"{png}",{str(sz)[1:-1]}\n')

                print("==" * 50)
                count += 1
                result_image.append(
                    [
                        idx + 1,
                        char_count + 1,
                        char_count + run_text_length,
                        run_idx,
                        get_rid(run._r.xml),
                    ]
                    + sz
                    + [png]
                )
            # 更新累计字符数
            char_count += run_text_length
    return result_text, result_image


def main():
    docx_path = "output3.docx"  # 替换为你的文件路径
    output_dir = "extracted_images"

    # 提取图片
    extract_images(docx_path, output_dir)

    # 阅读文档并检查图片位置
    text, image = read_word_docx(docx_path)
    text = "\n".join(
        [f"{i}-->{x}" for i, x in enumerate([x for x in text.split("\n") if x])]
    )

    print(image)


if __name__ == "__main__":
    main()


def read_word_file(file_path, path):
    extract_images(file_path, path)
    return read_word_docx(file_path)
