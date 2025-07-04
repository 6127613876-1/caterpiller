from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma

# Load env vars
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Embeddings + DB
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vectordb = Chroma(persist_directory="db", embedding_function=embedding)

# Retriever
retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 5})

# Prompt
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant answering questions based on a product/user manual.
Use only the information in the context below.
If you don't know the answer, say "I'm not sure based on the manual."

Context:
{context}

Question: {question}
Answer:"""
)

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

# QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt_template}
)

# Flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question")
    if not user_question:
        return jsonify({"answer": "Please enter a question."})
    
    try:
        response = qa_chain({"query": user_question})
        return jsonify({"answer": response["result"]})
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
