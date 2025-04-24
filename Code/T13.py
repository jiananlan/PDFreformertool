from zipfile import ZipFile
import xml.etree.ElementTree as ET


def extract_image_relationships(docx_path):
    count = 0
    result = {}
    with ZipFile(docx_path, "r") as docx_zip:
        # 读取 document.xml.rels 文件
        rels_path = "word/_rels/document.xml.rels"
        if rels_path not in docx_zip.namelist():
            print("未找到 document.xml.rels 文件！")
            return

        with docx_zip.open(rels_path) as rels_file:
            tree = ET.parse(rels_file)
            root = tree.getroot()

            # 命名空间（Microsoft Office Open XML 格式）
            ns = {"rel": "http://schemas.openxmlformats.org/package/2006/relationships"}

            # 解析所有 Relationship 元素
            image_relationships = {}
            for rel in root.findall("rel:Relationship", ns):
                r_id = rel.get("Id")
                target = rel.get("Target")

                # 只存储指向 media/ 目录的图片资源
                if target.startswith("media/"):
                    image_relationships[r_id] = "word/" + target

            # 输出结果
            if image_relationships:
                print("图片 ID 与路径对应关系：")
                for r_id, path in image_relationships.items():
                    print(f"{r_id} -> {path}")
                    result[r_id] = path.split("/")[-1]
                    count += 1
            else:
                print("未找到任何图片资源。")
    print(count)
    with open("data.txt", "w") as f:
        f.write(str(result))
    return result


# 使用示例
if __name__ == "__main__":
    t = extract_image_relationships("output3.docx")
    print(t)
