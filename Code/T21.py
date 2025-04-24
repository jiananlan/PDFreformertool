import fitz

pdf_path = r"D:\电脑管家迁移文件\微信聊天记录搬家\WeChat Files\wxid_wbjxn8hzlq6w22\FileStorage\File\2024-11\科研入门培养方案\科研入门培养方案\flash4_ug_4p62.pdf"


def extract_images_info(pdf_path):
    doc = fitz.open(pdf_path)
    images_info = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            bbox = page.get_image_rects(xref)
            images_info.append(
                {
                    "page": page_num,
                    "xref": xref,
                    "bbox": [(r.x0, r.y0, r.x1, r.y1) for r in bbox],
                }
            )

    return images_info


if __name__ == '__main__':
    images_info = extract_images_info(pdf_path)
    for info in images_info:
        print(info)


def delete_images_from_pdf(pdf_path, images_info, save_path):
    doc = fitz.open(pdf_path)

    for index, page in enumerate(doc):
        for pageinfo in images_info:
            if pageinfo["page"] == index:
                print(f"pageinfo: {index + 1}", pageinfo["bbox"])
                xref = pageinfo["xref"]
                try:
                    page.delete_image(xref)  # 删除该页面上的所有图片
                    print("success┓")
                except:
                    continue
                finally:
                    print("finally┛")
    doc.save(save_path)


def insert_image_into_pdf(pdf_path, page, pos_and_size, image, save_path):
    doc = fitz.open(pdf_path)
    page = doc[page]
    rect = fitz.Rect(pos_and_size)
    page.insert_image(rect, filename=image)
    doc.save(save_path)
    doc.close()


if __name__ == '__main__':
    insert_image_into_pdf(pdf_path, 0, (0, 0, 100, 100), r"C:\Users\anlan\Desktop\微信图片_20250411121732.png",
                          r"ooutput.pdf")
