from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

#to set the new project name in Lnagsmith or override the existing Name.
os.environ['LANGCHAIN_PROJECT'] = "Sequential LLM App"

load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

# STEP:1 creating a Model object that we are using for interacting with LMM
model = ChatGroq(
    model="groq/compound-mini",
    temperature=0.2 #creative parameter at each calling of llm reponse will be seen to different.
)


model2 = ChatOpenAI(model="gpt-3.5-turbo",temperature=0.2)

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

#how to set metadata which will be usefull for tracing by Langsmith Tool.
config = {
    'run_name':'Sequential Chain Prompting',
    'tags':{'llm_app','report_generation','summarization'},
    'metadata':{'model1':"groq/compound-mini","model2":"groq/compound-mini",'parser':'stroutputparser','creative_parameter':0.2}
}

result = chain.invoke({'topic': 'Unemployment in India'},config=config)

print(result)
