from __future__ import print_function
import os
import sys
import time
import fitz  # PyMuPDF

# 输入PDF文件路径
fname = r"C:\Users\anlan\Documents\WeChat Files\wxid_wbjxn8hzlq6w22\FileStorage\File\2025-04\PhysRevE.111.035406.pdf"

if not fname:
    raise SystemExit("No file specified.")

# 配置参数
dimlimit = 0  # 每个图像的边必须大于此值
relsize = 0  # 图像与pixmap大小比率必须大于此值
abssize = 0  # 绝对图像大小限制
imgdir = "images"  # 存储图像的目录

if not os.path.exists(imgdir):
    os.mkdir(imgdir)


def recoverpix(doc, item):
    x = item[0]  # xref of PDF image
    s = item[1]  # xref of its /SMask
    if s == 0:  # 没有SMask，直接返回图像数据
        return doc.extract_image(x)

    def getimage(pix):
        if pix.colorspace.n != 4:
            return pix
        return fitz.Pixmap(fitz.csRGB, pix)

    # 需要重建alpha通道
    pix1 = fitz.Pixmap(doc, x)
    pix2 = fitz.Pixmap(doc, s)

    if not (pix1.irect == pix2.irect and pix1.alpha == pix2.alpha == 0 and pix2.n == 1):
        pix2 = None
        print(f"Warning: unsupported /SMask {s} for {x}.")
        return getimage(pix1)

    pix = fitz.Pixmap(pix1)  # 复制pix1并添加alpha通道
    pix.setAlpha(pix2.samples)
    return getimage(pix)


t0 = time.time()
doc = fitz.open(fname)

page_count = len(doc)
xreflist = []
imglist = []

for pno in range(page_count):
    il = doc[pno].get_images(full=True)
    imglist.extend([x[0] for x in il])
    for img in il:
        xref = img[0]
        if xref in xreflist:
            continue
        width, height = img[2], img[3]
        if min(width, height) <= dimlimit:
            continue
        pix = recoverpix(doc, img)
        if isinstance(pix, dict):
            ext = pix["ext"]
            imgdata = pix["image"]
            imgfile = os.path.join(imgdir, f"img-{xref}.{ext}")
        else:
            imgfile = os.path.join(imgdir, f"img-{xref}.png")
            if pix.colorspace.name not in (fitz.csGRAY.name, fitz.csRGB.name):
                pix = fitz.Pixmap(fitz.csRGB, pix)
            imgdata = pix.tobytes("png")

        if len(imgdata) <= abssize:
            continue

        with open(imgfile, "wb") as fout:
            fout.write(imgdata)
        xreflist.append(xref)

t1 = time.time()
imglist = list(set(imglist))
print(f"{len(imglist)} images in total")
print(f"{len(xreflist)} images extracted")
print(f"Total time: {t1 - t0:.2f} sec")

warnings = fitz.TOOLS.mupdf_warnings()
if warnings:
    print("\nThe following warnings have been issued:")
    print("----------------------------------------")
    print(warnings)
