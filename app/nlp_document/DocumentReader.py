from spacy.matcher import Matcher
from spacy import load
import pdfplumber
from docx import Document
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
        with pdfplumber.open(document) as pdf:
            text = []
            for page in pdf.pages:
                text.append(page.extract_text() or "")

        doc = self.nlp("\n".join(text))
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