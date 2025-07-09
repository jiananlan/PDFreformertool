

# PDFreformertool / 基于大语言模型的 PDF 文档翻译软件

![GitHub License](https://img.shields.io/github/license/jiananlan/PDFreformertool?style=flat-square)
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg?style=flat-square)
![GitHub Issues](https://img.shields.io/github/issues/jiananlan/PDFreformertool?style=flat-square)

[English](#english) | [中文](#中文)

---

## 简介 / Introduction

**中文**  
PDFreformertool 是一个基于大语言模型（LLM）的 PDF 文档翻译工具，旨在解决现有翻译工具在专业场景下的不足。它支持多语言翻译，精准保留文档格式，适用于技术文档、法律合同、商务报告等复杂场景。项目利用 LLM 的高级语义处理能力，结合 `pymupdf` 和 `pdfplumber` 等库，提取 PDF 内容并生成高质量翻译结果。翻译数据存储在 MongoDB 中，同时实验性支持 HDF5（`T5.py`）作为替代存储方案。

**English**  
PDFreformertool is a PDF document translation tool powered by large language models (LLM), designed to address the shortcomings of existing translation tools in professional scenarios. It supports multilingual translation with precise format preservation, suitable for technical documents, legal contracts, and business reports. Leveraging LLM's advanced semantic processing, combined with libraries like `pymupdf` and `pdfplumber`, it extracts PDF content and delivers high-quality translations. Translation data is stored in MongoDB, with experimental HDF5 support (`T5.py`) as an alternative.

### 项目背景 / Project Background
在全球化和多语言交流需求激增的背景下，文档翻译工具的使用日益广泛。然而，现有商业工具（如 DeepL、Google Translate）在翻译质量和格式保留方面存在显著不足：
- **翻译质量**：无法满足技术文档、法律合同等专业场景的语义准确性和领域化需求。
- **格式问题**：复杂文档的表格错位、图片丢失、段落散乱、字体不一致等问题频发。
- **效率低下**：用户需手动调整排版，浪费时间和精力。

PDFreformertool 提供了一种高效解决方案，通过 LLM 和文档处理技术，实现高质量翻译和格式精准保留。

---

## 功能 / Features

- **精准文本提取**：利用 `pdfplumber` 和 `pymupdf` 高效提取 PDF 内容。  
- **高质量翻译**：通过 OpenAI 或 Azure OpenAI API 提供专业、多语言翻译。  
- **格式保留**：基于 `python-docx` 和 `docxtpl`，确保翻译后文档格式一致。  
- **数据存储**：支持 MongoDB 存储翻译数据，实验性支持 HDF5（`T5.py`）。  
- **灵活配置**：通过 `Tconfig.py` 自定义翻译主题、API 配置等。  

---

## 依赖 / Dependencies

以下是项目所需的 Python 库：

```
rich
docxtpl
pdf2docx
python-docx
pymongo
h5py
openai
pymupdf
pdfplumber
```

通过以下命令安装依赖：
```bash
pip install -r requirements.txt
```

**注意**：需安装 Python 3.8+ 和 MongoDB。HDF5（`T5.py`）为实验性功能，可能不稳定。

---

## 安装与运行 / Installation and Running

### 前置条件 / Prerequisites
1. 安装 Python 3.8 或以上版本。
2. 安装 MongoDB（或使用实验性 HDF5 存储，详见 `T5.py`）。
3. 获取大语言模型的 API Key 和 URL（如 OpenAI 或 Azure OpenAI）。

### 安装步骤 / Installation Steps
1. 克隆仓库：
   ```bash
   git clone https://github.com/jiananlan/PDFreformertool.git
   cd PDFreformertool
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 安装 MongoDB（参考 [MongoDB 官方文档](https://www.mongodb.com/docs/manual/installation/)）。

### 配置 / Configuration
1. 编辑 `Tconfig.py`：
   - 设置 LLM 的 API Key 和 URL。
   - 配置翻译主题（如目标语言）。
   - 若使用 Azure OpenAI（如 ChatGPT），将 `enable_chatgpt` 设为 `True`，并在 `T24.py` 中提供对应的 URL 和 API Key。
2. 在 `Tmain.py` 中更新 PDF 输入文件的路径为实际地址。

### 运行 / Running
运行以下命令启动程序：
```bash
python Tmain.py
```

---

## 工作流程 / Workflow

![工作流程示意](process.png)

1. **输入 PDF**：读取用户指定的 PDF 文件。
2. **文本提取**：通过 `pdfplumber` 和 `pymupdf` 提取文本内容。
3. **翻译处理**：调用 LLM API 进行高质量翻译。
4. **格式处理**：利用 `python-docx` 和 `docxtpl` 重构文档格式。
5. **数据存储**：翻译数据存储至 MongoDB 或实验性 HDF5。
6. **输出**：生成格式保留的翻译文档。

---

## 许可证 / License

本项目采用 **AGPL-3.0 许可证**，符合 `pymupdf` 库要求。详情见 [LICENSE](LICENSE) 文件。

---

## 贡献 / Contributing

欢迎贡献代码！请遵循以下步骤：
1. Fork 本仓库。
2. 创建功能分支（`git checkout -b feature/YourFeature`）。
3. 提交更改（`git commit -m 'Add YourFeature'`）。
4. 推送分支（`git push origin feature/YourFeature`）。
5. 创建 Pull Request。

代码需符合 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范，并附带测试。

---

## 常见问题 / FAQ

**Q: 为什么 HDF5 支持不稳定？**  
A: `T5.py` 是 MongoDB 的实验性替代方案，可能存在数据兼容性或性能问题。

**Q: 支持哪些语言？**  
A: 支持 LLM API 提供的所有语言，具体取决于使用的模型。

**Q: 如何调试运行错误？**  
A: 检查 `Tconfig.py` 中的 API 配置，确保 MongoDB 正常运行，验证 PDF 文件路径。

---

## 联系 / Contact

如有问题或建议，请在 [GitHub Issues](https://github.com/jiananlan/PDFreformertool/issues) 提交。

---

# English

## Introduction
PDFreformertool is a PDF document translation tool powered by large language models (LLM), addressing the limitations of existing translation tools in professional scenarios. It supports multilingual translation with precise format preservation, ideal for technical documents, legal contracts, and business reports. Using LLM's advanced semantic processing and libraries like `pymupdf` and `pdfplumber`, it extracts PDF content and delivers high-quality translations. Data is stored in MongoDB, with experimental HDF5 support (`T5.py`).

### Project Background
With the surge in globalization and multilingual communication, document translation tools are increasingly essential. However, mainstream commercial tools (e.g., DeepL, Google Translate) have notable shortcomings:
- **Translation Quality**: Inadequate for professional domains like technical documents or legal contracts due to poor semantic accuracy.
- **Formatting Issues**: Problems such as misaligned tables, missing images, scattered paragraphs, and inconsistent fonts.
- **Inefficiency**: Users must manually adjust formatting, wasting time and effort.

PDFreformertool offers an efficient solution, combining LLM and document processing to achieve high-quality translation and precise format retention.

## Features
- **Accurate Text Extraction**: Efficiently extracts content using `pdfplumber` and `pymupdf`.  
- **High-Quality Translation**: Provides professional, multilingual translation via OpenAI or Azure OpenAI API.  
- **Format Preservation**: Uses `python-docx` and `docxtpl` to maintain document formatting.  
- **Data Storage**: Supports MongoDB for translation data, with experimental HDF5 support (`T5.py`).  
- **Flexible Configuration**: Customize translation themes and API settings via `Tconfig.py`.  

## Dependencies
The project requires the following Python libraries:

```
rich
docxtpl
pdf2docx
python-docx
pymongo
h5py
openai
pymupdf
pdfplumber
```

Install dependencies using:
```bash
pip install -r requirements.txt
```

**Note**: Requires Python 3.8+ and MongoDB. HDF5 (`T5.py`) is experimental and may be unstable.

## Installation and Running

### Prerequisites
1. Install Python 3.8 or higher.
2. Install MongoDB (or use experimental HDF5 storage, see `T5.py`).
3. Obtain an API Key and URL for a large language model (e.g., OpenAI or Azure OpenAI).

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/jiananlan/PDFreformertool.git
   cd PDFreformertool
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install MongoDB (refer to [MongoDB official documentation](https://www.mongodb.com/docs/manual/installation/)).

### Configuration
1. Edit `Tconfig.py`:
   - Set the API Key and URL for the large language model.
   - Configure the translation theme (e.g., target language).
   - If using Azure OpenAI (e.g., ChatGPT), set `enable_chatgpt` to `True` and provide the URL and API Key in `T24.py`.
2. Update the PDF input file path in `Tmain.py` to the actual file location.

### Running
Run the following command to start the program:
```bash
python Tmain.py
```

## Workflow
![Workflow Diagram](process.png)

1. **Input PDF**: Reads the specified PDF file.
2. **Text Extraction**: Extracts text using `pdfplumber` and `pymupdf`.
3. **Translation Processing**: Performs high-quality translation via LLM API.
4. **Format Processing**: Reconstructs document format using `python-docx` and `docxtpl`.
5. **Data Storage**: Stores translation data in MongoDB or experimental HDF5.
6. **Output**: Generates a translated document with preserved formatting.

## License
This project is licensed under the **AGPL-3.0 License**, as required by `pymupdf`. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a Pull Request.

Code should adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards and include tests.

## FAQ
**Q: Why is HDF5 support unstable?**  
A: `T5.py` is an experimental alternative to MongoDB and may have compatibility or performance issues.

**Q: Which languages are supported?**  
A: Supports all languages provided by the LLM API, depending on the model used.

**Q: How to debug runtime errors?**  
A: Verify API settings in `Tconfig.py`, ensure MongoDB is running, and check the PDF file path.

## Contact
For questions or suggestions, open an issue on [GitHub Issues](https://github.com/jiananlan/PDFreformertool/issues) to contact me.

