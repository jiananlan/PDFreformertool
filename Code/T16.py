from pdf2image import convert_from_path


def pdf_to_images(pdf_path, output_folder="output_images"):
    import os

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 以原始DPI（通常是72或96）保持1:1比例
    images = convert_from_path(pdf_path, dpi=300)  # 可调整 dpi 提高质量

    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i+1}.png")
        image.save(image_path, "PNG")
        print(f"Saved: {image_path}")


pdf_to_images(
    r"D:\电脑管家迁移文件\微信聊天记录搬家\WeChat Files\wxid_wbjxn8hzlq6w22\FileStorage\File\2024-11\科研入门培养方案\科研入门培养方案\flash4_ug_4p62.pdf"
)
