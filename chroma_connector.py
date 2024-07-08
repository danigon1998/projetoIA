import os
import chromadb
from sentence_transformers import SentenceTransformer
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class ChromaDBConnection:
    def __init__(self):
        # Inicializa o cliente ChromaDB com a rota do arquivo de configuração
        chroma_db_path = os.getenv('CHROMA_DB_PATH')
        if chroma_db_path is None:
            raise ValueError("CHROMA_DB_PATH não está configurado no arquivo .env")
        
        if not os.path.exists(chroma_db_path):
            os.makedirs(chroma_db_path)
            print(f"Diretorio {chroma_db_path} criado.")
        
        self.client = chromadb.PersistentClient(path=chroma_db_path)

        try:
            self.collection = self.client.get_collection("FAQs")
        except Exception as e:
            print(f"Erro obtendo a coleção de FAQs: {e}. Criando uma nova coleção.")
            self.collection = self.client.create_collection("FAQs")
            self.index_faqs()

        # Inicializa o modelo de embeddings
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    def index_faqs(self):
        # Conecta à base de datos e recupera as FAQs
        connection = self._connect_to_db()
        cursor = connection.cursor()
        cursor.execute("SELECT id, title, content FROM faqs_faq")
        faqs = cursor.fetchall()

        # Prepara os documentos para a indexação
        documents = [
            {"id": str(faq[0]), "title": faq[1], "content": faq[2]}
            for faq in faqs
        ]

        # Gera embeddings para os documentos
        embeddings = self._embed_documents(documents)

        # Coloca os documentos e seus embeddings na coleção ChromaDB
        for doc, emb in zip(documents, embeddings):
            try:
                self.collection.add(documents=[doc["content"]], embeddings=[emb], ids=[doc["id"]])
            except Exception as e:
                print(f"Erro colocando o documento {doc['id']} a ChromaDB: {e}")

        cursor.close()
        connection.close()

    def _embed_documents(self, documents):
        embeddings = []
        for doc in documents:
            try:
                # Gera o embedding para o conteudo do documento
                encoding = self.embedder.encode(doc['content'])
                if encoding is not None:
                    embedding_list = encoding.tolist()
                    embeddings.append(embedding_list)
            except TypeError as e:
                print(f"Erro codificando o documento {doc['id']}: {e}")
        return embeddings

    def search(self, query_text: str, top_k=5):
        # Gera o embedding para a consulta
        query_embedding = self.embedder.encode(query_text)
        query_embedding_list = query_embedding.tolist()
        
        # Realiza a consulta em ChromaDB
        try:
            results = self.collection.query(query_embeddings=[query_embedding_list], n_results=top_k)
            
            return results
        except Exception as e:
            print(f"Erro realizando a consulta em ChromaDB: {e}")
            return []

    def _connect_to_db(self):
        return psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )