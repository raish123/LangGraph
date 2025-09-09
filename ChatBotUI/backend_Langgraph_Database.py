from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI,OpenAIEmbeddings #this to above classes we used to interact with llm model.
from dotenv import load_dotenv
from langgraph.graph import StateGraph,END,START #this class we used to build stateful workflows in graphical form mei.
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,List,Dict,TypedDict,Optional
from langchain_core.output_parsers import PydanticOutputParser,StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from typing import Literal,Optional
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langgraph.graph.message import BaseMessage #this parent class of all message class.
import operator
from langgraph.checkpoint.memory import InMemorySaver #saving state in ram memory.
#this object we will create just before adding edges or nodes to graph.

#To save state memory or intermediate level shared Memory throughout the workflow in Database 
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

load_dotenv()

#first creating sqlite database connection.
conn = sqlite3.connect(
    database = "chatbot.db", 
    check_same_thread=False,) #this same database ko we are using with multiple threads thatswhy False




#creating SqliteSaver object.
checkpointer = SqliteSaver(conn=conn)


#Groq Model object
model1 = ChatGroq(
    model="groq/compound-mini",
    temperature=0.2
)
model1

#openAI model object.
model2 = ChatOpenAI(temperature=0.2)

## Hugging Face endpoint define karo OPen source Model chat or Generation Model.
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
)

# Chat model object banao
model3 = ChatHuggingFace(llm=llm)



#defining state schema for chatbot.
from langgraph.graph.message import add_messages
class ChatbotState(TypedDict):
    message : Annotated[list[BaseMessage], add_messages] 
#reducer adding to this state bcoz past history will get added to existing state value mei.

#creating a graph object by using stategraph class.
graph = StateGraph(ChatbotState)



def chat_node(state:ChatbotState) ->ChatbotState:
    #fetching the field(user_query) from state class.
    Human = state['message']
    
    #send to llm model.
    response = model1.invoke(Human)
    
    #now updating the state memory and returning the partial updated state.
    return {
        'message':[response]
    }


#graph mei nodes or edges add karne se phele mujhe ek memorysaver object banana padegha.
graph.add_node(node="chat_node",action=chat_node)

#now adding the edges to graph.
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)


#now compiling the workflow.
workflow = graph.compile(checkpointer=checkpointer)


#now fetching how many  checkpoint exist in database or not.
def retrieve_all_unique_thread():
    
    all_thread_set = set()
    for checkpoint in checkpointer.list(config=None):
        all_thread_set.add(checkpoint.config['configurable']['thread_id'])

    return list(all_thread_set)