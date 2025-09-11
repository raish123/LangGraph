from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Simple one-line prompt
prompt = PromptTemplate.from_template("{question}")

load_dotenv()


# STEP:1 creating a Model object that we are using for interacting with LMM
model = ChatGroq(
    model="groq/compound-mini",
    temperature=0.2 #creative parameter at each calling of llm reponse will be seen to different.
)


model2 = ChatOpenAI(model="gpt-3.5-turbo",temperature=0.2)
parser = StrOutputParser()

# Chain: prompt → model → parser
chain = prompt | model | parser

# Run it
result = chain.invoke({"question": "What is the capital of India?"})
print(result)
