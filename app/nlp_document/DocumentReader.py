from spacy.matcher import Matcher
from spacy import load
import pdfplumber
from docx import Document
from io import BytesIO
import zipfile
import logging
# Зависимости, которых может и не быть
# pip install pdfplumber
# pip install docx
################################################################
# СИНГТОН
# Он такой один, иначе мы умрем
class DocumentReader:
    def __init__(self):
        #загрузка модели
        self.nlp = load("app/nlp_document/model/model-last")
    # Метод для чтения информации с документа, возвращает два словаря, первый компетенции, второй доп. информация
    def read_document(self, document: bytes, competence_list: list[str]):
        # Загрузка документа в spaCy
        content=""
        buf = BytesIO(document.read())
        header = buf.getvalue()[:8]
        # если файл pdf
        if header.startswith(b'%PDF-'):
            with pdfplumber.open(buf) as pdf:
                text = []
                for page in pdf.pages:
                    text.append(page.extract_text() or "")
                content="\n".join(text)
        # если файл docx
        elif header.startswith(b'PK\x03\x04'):
            with zipfile.ZipFile(buf, 'r') as zip_file:
                if 'word/document.xml' in zip_file.namelist():
                    buf.seek(0)
                    doc = Document(buf)
                    content="\n".join([paragraph.text for paragraph in doc.paragraphs])
        else:
            raise Exception("Invalid file!")

        doc = self.nlp(content)
        # Нахождение всех компетенций в документе
        competences={}
        for token in doc.ents:
            if token.label_ in competence_list:
                competences[token.label_]=0
        # Получение доп данных, нереализовано нормально
        info={
            "PHONE_NUMBER":[],
            "EMAIL":[],
            "URL":[]
        }
        matcher = Matcher(self.nlp.nlp.vocab)
        # регулярки для нахождения доп данных, массивы с вариантами регулярок для одного случая
        email_patterns = [
            [{"TEXT": {"REGEX": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"}}]
        ]
        phone_patterns = [
            [{"ORTH": "+"}, {"SHAPE": "ddd"}, {"ORTH": "("}, {"SHAPE": "ddd"}, {"ORTH": ")"}, {"SHAPE": "ddd-dd-dd"}],
            [{"SHAPE": "ddd"}, {"ORTH": "-"}, {"SHAPE": "ddd"}, {"ORTH": "-"}, {"SHAPE": "dd-dd"}],
            [{"TEXT": {"REGEX": "(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}"}}]
        ]
        url_patterns=[[{"TEXT": {"REGEX": "(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])"}}]
        ]
        #добавления паттернов в мэтчер
        matcher.add("PHONE_NUMBER", phone_patterns)
        matcher.add("EMAIL", email_patterns)
        matcher.add("URL", url_patterns)
        matches = matcher(doc)
        for match_id, start, end in matches:
            info[self.nlp.nlp.vocab.strings[match_id]].append(doc[start:end].text)
        return [competences,info]