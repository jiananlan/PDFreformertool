# 基于llm的pdf文档翻译软件
## 依赖
```
rich
docxtlp
pdf2docx
python-docx
pymongo
h5py
openai
pymupdf
pdfplumber
```
或者安装  
```bash
python -m pip install -r requirement.txt
```

## 运行
**0.安装**好python3；以上依赖库；mongodb（T5.py是我对替代mongodb的一个尝试，利用hdf5，但是尚有问题🤨🤨🤨）；  
**1.获取**一个大语言模型的api-key，以及对应url（Tconfig.py）；  
**2.将T**main.py中的pdf输入地址更换为真实文件地址；  
**3.更改**Tconfig.py中的文档的主题；  
**4.若为**azure openai的api（例如这里可以使用chatgpt），将Tconfig.py中的enable_chatgpt设为True，并在T24.py中提供url、api-key。  
```bash
python Tmain.py
```
## 本程序依据AGPL协议，这是pymupdf库的要求。
