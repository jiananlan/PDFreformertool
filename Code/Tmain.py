import os
import Tfunction
import rich
import Tconfig

resource = r"C:\Users\anlan\Downloads\Digital-radar-data-KLumpur-LSTRP-analysis.pdf"
target = ".\\Output_File"

# import T19
# new = os.path.join(target, Tfunction.generate_random_filename())
# T19.process(pdf_path=resource, output_pdf=new)

# ## PDF转word ## #
import T8

file_save = os.path.join(target, Tfunction.generate_random_filename())
T8.run(pdf_file=resource, docx_file=file_save)
rich.print(f"[blue][bold]File 1 at: [/bold]{file_save}[/blue]")

# ## word提取图片 ## #
import T12

total_images = T12.extract_images_from_docx(file_save)
print(f"总共提取了 {total_images} 张图片，存放于子目录。")

# ## 提取键-图片对应关系 ## #
import T13

t = T13.extract_image_relationships(file_save)
print(f"Key-Image relationship: {t}")

# ## 逐行翻译内容 ## #
'''Old version (awful performance)
import T9

third = os.path.join(target, Tfunction.generate_random_filename())
err = T9.main_run(file_save, third)
if err:
    rich.print(":angry:" * 50000 + f"\n{err} errors" * 500, end="\n")
'''
import T26

third = os.path.join(target, Tfunction.generate_random_filename())
err = T26.modify_paragraphs(file_save, third, process_paragraph_function=T26.process_text)
if err:
    rich.print(":angry:" * 50000 + f"\n{err} errors" * 500, end="\n")

# ## 翻译表格内容 ## #
import T15

if Tconfig.configuration["set_file_name"]:
    sec_file = os.path.join(target, Tconfig.configuration["file_name"])
else:
    sec_file = os.path.join(target, Tfunction.generate_random_filename())
final_file = os.path.join(target, Tfunction.generate_random_filename())
T15.process_shell(file=third, to=sec_file)
rich.print(f"[blue][bold]File Final at: [/bold]{final_file}[/blue]")

# ## 图片注入word ## #
import T11

real_final = os.path.join(target, Tfunction.generate_random_filename())
T11.main_run(sec_file, second=real_final)
rich.print(f"[blue][bold]File 2 at: [/bold]{real_final}[/blue]")

# ## 删除重复文件 ## #
import Tremove

Tremove.find_and_remove_duplicates(target)
print(os.path.exists(real_final), real_final)
os.startfile(real_final)
