#In this file we again building a chatbot either by using Langgraph or langgraph framework.
#but here i am using Langraph
#below is the class of models using this class we are interacting with LLM Models.
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI,OpenAIEmbeddings
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint

#now adding longterm memory to my chatbot
#it means that all the chat history we accessible any time.
from langgraph.checkpoint.sqlite import SqliteSaver


#creating sqllite database connections
import sqlite3

db_connection = sqlite3.connect(
    database="chatbot_longTermMemory.db",
    check_same_thread=False #Connection ko doosre threads mein bhi use karne do bypassing thread.
    
) 


#creating an checkpointer object of SqliteSaver class
checkpointer_sqlite = SqliteSaver(
    #we have to create sqlite database connections
    conn = db_connection
)


#to load the api key from env file 
from dotenv import load_dotenv 

load_dotenv()
 
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

#below class we used to represent my worklfow to graphical form mei and hold the state memory value by using persistence.
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import InMemorySaver #using langgraph we can add persisitence or short term memory to my workflow

from typing import List,Literal,Annotated

#below class will hold all kind of message init bcoz it parent class
from langgraph.graph.message import BaseMessage

#merge reducer we are using in state Memory.
from langgraph.graph.message import add_messages

import operator #used to perform all type of operations arithmatic,logical,conditional so on

from dataclasses import dataclass
from langchain_core.messages import HumanMessage,AIMessage

#for tracing the workflow by langsmith we are using below class
from langsmith import traceable

from langchain_core.runnables import RunnableSequence


#creating a Model object that we are using for interacting with LMM
model = ChatGroq(
    model="groq/compound-mini",
    temperature=0.2 #creative parameter at each calling of llm reponse will be seen to different.
)



#step:1) defining the state or memory schema that we are passing throughout my workflow.
@dataclass
class ChatBotState():
    #now defining the class variable that commonly using throughout my workflow.
    message : Annotated[list[BaseMessage],add_messages] #thats how reducer will applied [aimessage,humanmessage,almessage..so on]
    
    
#creating an object of stategraph class building empty graph
graph = StateGraph(ChatBotState)


#chat_generate node ka execution function defining.
def chat_generate(state:ChatBotState) ->ChatBotState:
    parser = StrOutputParser()
    
    #now fetching the field from state class
    user_message = state.message
    
    #taking the input from user changing them into structure instruction prompt mei.
    prompt = PromptTemplate(
        template="""
        You are a friendly AI chatbot. Continue the conversation based on the user's message below.
        {user_message}
        
        """,
        input_variables=['user_message']
    )
    
    #now passing this user prompt to llm model so forming sequential chain
    seq_chain = RunnableSequence(prompt,model,parser)
    
    #now invoking the seq_chain
    response = seq_chain.invoke(input={'user_message':user_message})
    
    #now updating the AI response to state memory.
    return {
        'message':[AIMessage(content=response)]
    }


#now adding nodes and edges to my workflow graph.
graph.add_node(node="chat_generate",action=chat_generate)



#now adding edges to nodes.
graph.add_edge(START,"chat_generate")
graph.add_edge("chat_generate",END)

#crating an object of persistence memory class
#checkpointer = InMemorySaver()

#now compiling the graph to visualize and making ready to execute.
workflow = graph.compile(checkpointer=checkpointer_sqlite) #adding short term memory persistence to my workflwo


#now invoking the workflow.
# config1 = {'configurable':{'thread_id':'2'}}
# response = workflow.invoke(input=ChatBotState(
#     message=[HumanMessage(content="which president we are talking about")] #checking long term memory able to store state value or not.
# ),config=config1)

# print(response)

# *****************demo about checkpointer to get threadid from database saver *************

# for each in checkpointer_sqlite.list(config=None):
#     print(each.config['configurable']['thread_id']) #thats how u can get thread_id for each checkpointer step pe
#     break



# ****************very important Note:- ***************************************************

#database saver implement karte time we have to ensure hona
#already kitne unique threads hai un sabhi ko thread list append karengey

def checking_unique_thread_database() ->List:
    distinct = set()
    #now fetching how many  checkpoint exist in database or not.
    for thread_id in checkpointer_sqlite.list(config=None):
        distinct.add(thread_id.config['configurable']['thread_id'])
        
    return list(distinct)
        
