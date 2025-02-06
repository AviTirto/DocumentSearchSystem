import chromadb
import os

class CDB:
    def __init__(self):
        self.db = chromadb.PersistentClient(
            path=os.getenv('DB_PATH')
        )

        self.ppts = self.db.get_or_create_collection(
            name="ppts",
        )

    def add_embeddings(self, id, title, slide_num, rag_text, full_text):
        try:
            self.ppts.add(
                ids = [id],
                documents = [rag_text],
                metadatas = [{
                    'title': title,
                    'full_text': full_text,
                    'slide': slide_num
                }]
            )
            return True
        except Exception as e:
            print(e)
            return False
        
    def vector_search(self, query, **kwargs):
        embedding = kwargs.get('embedding', None)
        n_results = kwargs.get('n_results', 5)
        filter = kwargs.get('where', None)
        filter_document = kwargs.get('where_document', None)
        data = kwargs.get('include', ["metadatas", "documents"])

        return self.ppts.query(
            query_embeddings = embedding,
            n_results = n_results,
            where = filter,
            where_document = filter_document,
            query_texts = [query],
            include = data
        )