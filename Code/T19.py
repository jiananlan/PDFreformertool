import fitz  # PyMuPDF


def process(pdf_path, output_pdf):

    doc = fitz.open(pdf_path)

    for page in doc:
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            img_bytes = base_image["image"]
            img_format = base_image["ext"]

            # 只处理非 RGB 图片
            pix = fitz.Pixmap(doc, xref)
            if pix.n >= 4:  # 包含透明通道或CMYK
                pix = fitz.Pixmap(fitz.csRGB, pix)  # 转换为 RGB

            # 替换 PDF 中的图片
            img_rect = page.get_image_rects(xref)
            page.insert_image(
                img_rect[0], stream=pix.tobytes("png"), filename=f"temp_{img_index}.png"
            )

    # 保存处理后的 PDF
    doc.save(output_pdf)
    doc.close()


# 使用 pdf2docx 转换处理后的 PDF
