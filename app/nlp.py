from typing import Annotated

from fastapi.params import Depends

from app.nlp_document.DocumentReader import DocumentReader


nlp: DocumentReader | None = None

def init_nlp_module():
    global nlp
    nlp = DocumentReader()

def get_nlp():
    return nlp

Reader = Annotated[
    DocumentReader,
    Depends(get_nlp)
]