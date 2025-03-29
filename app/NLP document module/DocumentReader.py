import spacy
from spacy.matcher import Matcher
from spacy_layout import spaCyLayout
from spacy.matcher import Matcher
from docling_core.types.doc.document import DoclingDocument
from commonDictionaries import listOfSlills
# Зависимости, которых может и не быть
# pip install spacy-layout
# python -m spacy download ru_core_news_sm
################################################################
# СИНГТОН
# Он такой один, иначе мы умрем
class DocumentReader:
    def __init__(self):
        #загрузка модели
        self.nlp = spaCyLayout(spacy.load("ru_core_news_sm"))
    # Метод для чтения информации с документа, возвращает два словаря, первый компитенции, второй доп. информация
    def read_document(self, document: DoclingDocument | bytes):
        # Загрузка документа в spaCy
        doc = self.nlp(document)
        # Нахождение всех скилллов в документе
        Skills={}
        for token in doc:
            if token.pos_ in listOfSlills:
                Skills[token.pos_]=-1
        # Получение доп. данных, нереализовано нормально
        AddInfo={
            "PHONE_NUMBER":[],
            "EMAIL":[],
            "URL":[]
        }
        matcher = Matcher(self.nlp.vocab)
        # регулярки для нахождения доп данных
        emailPattern = [{"TEXT": {"REGEX": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"}}]
        phonePatterns = [
            [{"ORTH": "+"}, {"SHAPE": "ddd"}, {"ORTH": "("}, {"SHAPE": "ddd"}, {"ORTH": ")"}, {"SHAPE": "ddd-dd-dd"}],
            [{"SHAPE": "ddd"}, {"ORTH": "-"}, {"SHAPE": "ddd"}, {"ORTH": "-"}, {"SHAPE": "dd-dd"}],
            [{"TEXT": {"REGEX": "(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}"}}]
        ]
        URLPattern=[{"TEXT": {"REGEX": "(?:(?:https?|ftp|file):\/\/|www\.|ftp\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])"}}]
        matcher.add("PHONE_NUMBER", phonePatterns)
        matcher.add("EMAIL", emailPattern)
        matcher.add("URL", URLPattern)
        matches = matcher(doc)
        for match_id, start, end in matches:
            AddInfo[self.nlp.vocab.strings[match_id]].append(doc[start:end].text)
        return [Skills,AddInfo]