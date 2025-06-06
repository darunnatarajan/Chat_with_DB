import streamlit as st
from pathlib import Path
from langchain.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
#from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
# from langchain.callbacks import StreamlitCallbackHandler
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler


st.set_page_config(page_title="Chat with SQL DB", page_icon='💻')
st.title('Chat with your SQL DB Dynamically!!')

LOCAL_DB = 'USE_LOCALDB'
MYSQL = 'USE_MYSQL'
POSTGRES = 'USE_POSTGRESQL'


# radio_opt = ['Use SQLite 3 Database - prreport.db', 'Connect to your database']
# selected_opt = st.sidebar.radio(label='Choose the DB which you want to chat with', options=radio_opt)

# radio_opt = [
#     'Use SQLite 3 Database - prreport.db',
#     'Connect to MySQL Database',
#     'Connect to PostgreSQL Database'
# ]
# selected_opt = st.sidebar.radio(label='Choose the DB which you want to chat with', options=radio_opt)



# if radio_opt.index(selected_opt) == 1:
#     db_uri = MYSQL
#     mysql_host = st.sidebar.text_input('Provide Host Name')
#     mysql_user = st.sidebar.text_input('MySQL Username')
#     mysql_pass = st.sidebar.text_input('Provide the Password', type='password')
#     mysql_db = st.sidebar.text_input('MySQL Database Name')
# else:
#     db_uri = LOCAL_DB

# POSTGRES = 'USE_POSTGRESQL'

# if radio_opt.index(selected_opt) == 1:
#     db_uri = MYSQL
# elif radio_opt.index(selected_opt) == 2:
#     db_uri = POSTGRES
# else:
#     db_uri = LOCAL_DB

db_uri = POSTGRES
# if db_uri in [MYSQL, POSTGRES]:
#     host = st.sidebar.text_input('Host Name')
#     user = st.sidebar.text_input('Username')
#     password = st.sidebar.text_input('Password', type='password')
#     database = st.sidebar.text_input('Database Name')

# api_key = st.sidebar.text_input(label='Groq API Key', type='password')

# Hardcoded PostgreSQL DB and Groq API credentials
#db_uri = 'USE_POSTGRESQL'  # Force PostgreSQL path

host = "localhost"
user = "postgres"
password = "root"
database = "prreportdb"

api_key = "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"


if not db_uri:
    st.info('Please enter the database information and URI')
if not api_key:
    st.info('Please add the Groq API Key')
    st.stop()  

llm = ChatGroq(groq_api_key=api_key, model_name='Llama3-8b-8192', streaming=True)

# @st.cache_resource(ttl='2h')
# def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_pass=None, mysql_db=None):
#     if db_uri == LOCAL_DB:
#         dbfilepath = (Path(__file__).parent / 'pr_report.db').absolute()
#         return SQLDatabase(create_engine(f'sqlite:///{dbfilepath}'))
    
#     elif db_uri == MYSQL:
#         if not (mysql_host and mysql_user and mysql_pass and mysql_db):
#             st.error('Please provide the MySQL database information')
#             st.stop()
        
#         return SQLDatabase(create_engine(f'mysql+mysqlconnector://{mysql_user}:{mysql_pass}@{mysql_host}/{mysql_db}'))

# @st.cache_resource(ttl='2h')
# def configure_db(db_uri, host=None, user=None, password=None, database=None):
#     if db_uri == LOCAL_DB:
#         dbfilepath = (Path(__file__).parent / 'pr_report.db').absolute()
#         return SQLDatabase(create_engine(f'sqlite:///{dbfilepath}'))

#     if db_uri in [MYSQL, POSTGRES]:
#         if not (host and user and password and database):
#             st.error('Please provide complete database information')
#             st.stop()

#         try:
#             if db_uri == MYSQL:
#                 engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')
#             else:  # POSTGRES
#                 engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{database}')
            
#             # Test connection
#             with engine.connect() as conn:
#                 conn.execute("SELECT 1")

#             return SQLDatabase(engine)
#         except Exception as e:
#             st.error(f"Unable to connect to the database: {e}")
#             st.stop()


from sqlalchemy import create_engine, text  # 👈 ensure this is at the top

@st.cache_resource(ttl='2h')
def configure_db(db_uri, host=None, user=None, password=None, database=None):
    if db_uri == LOCAL_DB:
        dbfilepath = (Path(__file__).parent / 'pr_report.db').absolute()
        return SQLDatabase(create_engine(f'sqlite:///{dbfilepath}'))

    if db_uri in [MYSQL, POSTGRES]:
        if not (host and user and password and database):
            st.error('Please provide complete database information')
            st.stop()

        try:
            if db_uri == MYSQL:
                engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}/{database}')
            else:  # POSTGRES
                engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}/{database}')

            # ✅ Fix here
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            return SQLDatabase(engine)
        except Exception as e:
            st.error(f"Unable to connect to the database: {e}")
            st.stop()

# if db_uri == MYSQL:
#     db = configure_db(db_uri, mysql_host, mysql_user, mysql_pass, mysql_db)
# else:
#     db = configure_db(db_uri)

if db_uri in [MYSQL, POSTGRES]:
    db = configure_db(db_uri, host, user, password, database)
else:
    db = configure_db(db_uri)


toolkit = SQLDatabaseToolkit(db=db,llm=llm)

agent=create_sql_agent(llm=llm,
                       toolkit=toolkit,
                       handle_parsing_errors=True,
                       verbose=True,
                       agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

if 'messages' not in st.session_state or st.sidebar.button('clear message history'):
    st.session_state['messages'] = [{'role': 'assistant','content':'How can i help you'}]
 
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

user_query = st.chat_input(placeholder='Ask anything from the database')

if user_query:
    st.session_state.messages.append({'role': 'user', 'content': user_query})
    st.chat_message('user').write(user_query)

    with st.chat_message('assistant'):
        streamlit_callback = StreamlitCallbackHandler(st.container())

        response = agent.invoke(
            {"input": user_query},
            callbacks=[streamlit_callback],
            handle_parsing_errors=True
        )

        def format_response(res):
            if isinstance(res, list):
                if all(isinstance(row, tuple) for row in res):
                    import pandas as pd
                    try:
                        df = pd.DataFrame(res)
                        return df
                    except Exception:
                        return str(res)
                else:
                    return str(res)
            return res

        formatted_response = format_response(response)
        st.session_state.messages.append({'role': 'assistant', 'content': str(formatted_response)})

        if isinstance(formatted_response, str):
            st.write(formatted_response)
        else:
            st.dataframe(formatted_response)
