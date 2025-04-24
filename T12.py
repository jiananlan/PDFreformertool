import os
from docx import Document

# 确保目标文件夹存在
output_folder = "./extracted_images"
os.makedirs(output_folder, exist_ok=True)


def extract_images_from_docx(docx_path):
    doc = Document(docx_path)
    image_count = 1

    for rel in doc.part.rels:
        if "image" in doc.part.rels[rel].target_ref:
            image_part = doc.part.rels[rel].target_part
            image_bytes = image_part.blob
            ext = image_part.content_type.split("/")[-1]  # 获取图片格式

            image_filename = f"image{image_count}.{ext}"
            image_path = os.path.join(output_folder, image_filename)

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            image_count += 1

    return image_count


# 使用示例
if __name__ == "__main__":
    docx_file = "output3.docx"  # 替换为你的 Word 文件路径
    total_images = extract_images_from_docx(docx_file)
    print(f"总共提取了 {total_images} 张图片，存放于 {output_folder} 目录。")
