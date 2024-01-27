from srai_chat.dao.store_document_base import StoreDocumentBase


class DaoBase:
    def __init__(self, store_document: StoreDocumentBase) -> None:
        self.store_document = store_document

    def delete_all(self) -> None:
        self.store_document.delete_all()
