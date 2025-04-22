import fitz  # PyMuPDF
import os
import faiss
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from sentence_transformers import SentenceTransformer

#! Code to create basic global variables and import libraries
model = SentenceTransformer("all-MiniLM-L6-v2")

def read_pdfbook_file(file_name):
    print("Reading the file...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir,"data", file_name)

    with fitz.open(file_path) as doc:
        whole_text = ""
        for page in doc:
            whole_text += page.get_text()
    print("File read successfully.")
    return whole_text

def chunk_text(text):
    print("Chunking the text...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    chunks = splitter.split_text(text)
    print(f"Total chunks created.")
    return chunks



#! Embedding the chunks

def embed_chunks_and_save(chunks):
    print("Embedding chunks...")
    embeddings = model.encode(chunks)
    print("Embeddings created.")

    print("Creating FAISS index...")
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    print("FAISS index created.")

    print("Saving chunks and index...")
    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)
    faiss.write_index(index, "index.idx")
    print("Chunks embedded and saved.")


def load_chunks_and_index():
    path = os.path.dirname(os.path.abspath(__file__))
    
    with open("chunks.pkl", "rb") as f:
        chunks = pickle.load(f)
    index = faiss.read_index("index.idx")
    print("Chunks and index loaded.")
    return chunks, index



def query_in_data(question , index,chunks):
    
    query_embedding = model.encode([question])
    top_k = 1

    D,I = index.search(query_embedding, top_k)
    print("Top K results:")
    for i in I[0]:
        print(chunks[i])
        return chunks[i]






# ! call all functions 

# text = read_pdfbook_file("atomic_habits.pdf")
# chunks = chunk_text(text)
# embed_chunks_and_save(chunks)



