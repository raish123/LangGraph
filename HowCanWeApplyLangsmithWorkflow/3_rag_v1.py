# pip install -U langchain langchain-openai langchain-community faiss-cpu pypdf python-dotenv

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()  # expects OPENAI_API_KEY in .env

#want to show new project name  "RAG TRACING V1"
os.environ["LANGCHAIN_PROJECT"] =  "RAG TRACING V1"
parser = StrOutputParser()

# *********************************Loading Document **********************************************************
#loading PDF document.
PDF_PATH = "Langsmith_Tracing\islr.pdf"  # <-- change to your PDF filename

# 1) Load the document by using PDF DocumentLoader
#creating an object of PDF DocumentLoader class.
loader = PyPDFLoader(PDF_PATH)

#from loader object loading document into my working space.
docs = loader.load()  # one Document per page


# *********************************Splitting Documents **********************************************************
# 2) spliiting the document by using Text Splitter Technique.
#creating an object of RecursiveCharacterTextSplitter class
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)

#splitting the documents into chunks.
splits = splitter.split_documents(docs)


# *********************************Converting Chunks to Vectors **********************************************************
# 3) chunks of document converting into embedding vectors.
emb = OpenAIEmbeddings(model="text-embedding-3-small")


# *********************************Storing Embedding Vectors To Vector Store **********************************************************
#saving those embedding vectors to my vector database or vector store.
vs = FAISS.from_documents(splits, emb)


# *********************************Retrievers **********************************************************
#changing vector database or vector store to retrievers so that based on user query 
#retrieving the relvant document from vector DB
retriever = vs.as_retriever(search_type="similarity", search_kwargs={"k": 4}) #note retrievers is runnable


# *********************************Forming Structure Instruction Prompt **********************************************************
# 4) creating systemQueryPrompt --> means (userquery+retrieval documet) combining together known as systemQuery
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY from the provided context. If not found, say you don't know."),
    ("human", "Question: {question}\n\nContext:\n{context}")
])

# 5) creating an model to interact with system query and generate response.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


#combining or joining together retrieval document together
def format_docs(docs): 
    return "\n\n".join(d.page_content for d in docs)


# *********************************Forming Parallel Chains **********************************************************
#forming Parallel chains together.(Parallel chain input they want same type and output dtype will be dictatonary)
parallel = RunnableParallel({
    #userquery--->retriever-->relevance document fetching in docs-->merging all doc as single string
    "context": retriever | RunnableLambda(format_docs), 
    "question": RunnablePassthrough() #simply passing user query 
})

#forming chain
chain = parallel | prompt | llm | parser


# *********************************Asking Question **********************************************************
# 6) Ask questions
print("PDF RAG ready. Ask a question (or Ctrl+C to exit).")
q = input("\nQ: ")
ans = chain.invoke(q.strip())
print("\nA:", ans)
