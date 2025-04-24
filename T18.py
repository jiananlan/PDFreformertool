import fitz  # PyMuPDF

pdf_path = r"C:\Users\anlan\Documents\WeChat Files\wxid_wbjxn8hzlq6w22\FileStorage\File\2025-04\PhysRevE.111.035406.pdf"

doc = fitz.open(pdf_path)
for page_number in range(len(doc)):
    page = doc[page_number]

    # 获取所有绘制的图形（形状）
    shapes = page.get_drawings()

    for shape in shapes:
        shape_type = shape["type"]
        print()
        for item in shape["items"]:
            print(f"[{page_number}]: {item}")
print()
