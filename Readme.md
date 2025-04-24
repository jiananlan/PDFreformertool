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
pdf2image
```

## 运行
1.获取一个大语言模型的api-key，以及对应url（Tconfig.py）；  
2.将Tmain.py中的pdf输入地址更换为真实文件地址；  
3.更改Tconfig.py中的文档的主题；  
4.若为azure openai的api（例如这里可以使用chatgpt），将Tconfig.py中的enable_chatgpt设为True。  
