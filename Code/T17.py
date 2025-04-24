import pdfplumber

pdf_path = "E:\BaiduNetdiskDownload\Toliss - 空中客车 A320 Neo v1.0.4 [X-PLANE11 12]\ToLissA320_V1p0p4Carda and KOSP\ToLissA320_V1p0p4\manuals\ToLiss_AirbusA320_Tutorial.pdf"

with pdfplumber.open(pdf_path) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
        images = page.images
        for img in images:
            x0, y0, x1, y1 = img["x0"], img["top"], img["x1"], img["bottom"]
            print(f"Page {page_number}: Image at ({x0}, {y0}) - ({x1}, {y1})")
