# import the required packages
import urllib
import os
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms import AzureOpenAI

# Connect to your database
server = 'YOUR-SERVER-NAME'
database = 'YOUR-DATABASE-NAME'
username = 'YOUR-USERNAME'
pwd = 'YOUR-PASSWORD'
driver= 'ODBC Driver 17 for SQL Server'

def db_instance():
    #Creating SQLAlchemy connection sting
    params = urllib.parse.quote_plus('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ pwd+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
    db_instance = SQLDatabase.from_uri(conn_str)
    return db_instance

db = db_instance()

# Setting API Key and API endpoint for OpenAI
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_KEY"] =  "YOUR-AZURE-OPENAI-KEY"
os.environ["OPENAI_API_BASE"] = "https://<YOUR-OPENAI-ENDPOINT>.openai.azure.com/"
os.environ["OPENAI_API_VERSION"] = "2022-12-01"

llm = AzureOpenAI(deployment_name="text-davinci-003", model_name="text-davinci-003") # replace with your details

# LangChain Agent
toolkit = SQLDatabaseToolkit(db=db, llm = llm)

agent_executor = create_sql_agent(
    llm= llm,
    toolkit=toolkit,
    verbose=True,
    top_k = 5
)

# Test
agent_executor.run("'What is the total payments value for 2021?'")
