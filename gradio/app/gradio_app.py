import os
from dataclasses import dataclass
from typing import Dict, List
import jwt
import uvicorn
from fastapi import FastAPI
import gradio as gr
# START NEW
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain import OpenAI
# END NEW

@dataclass
class Message:
    role: str
    content: str

DBX_USER_ACCESS_TOKEN = "ws_access_token"

app = FastAPI()


def get_user_info(id_token):
    claims = jwt.decode(id_token, options={"verify_signature": False})
    return {
        "user_email": claims["sub"],
    }


history: Dict[str, List[Message]] = {}

PROMPT = "You are a Lakehouse Application chatbot tha answers questions about the NYC Taxi dataset."

CSS = """
.contain { display: flex; flex-direction: column; background-color: red; }
.gradio-container { height: 100vh !important; }
#component-0 { height: 100%; }
#chatbot { flex-grow: 1; overflow: auto;}
"""

with gr.Blocks(css=CSS) as demo:
    chatbot = gr.Chatbot(elem_id="chatbot", layout="panel")
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history, request: gr.Request):
        databricks_token = request.request.cookies.get(DBX_USER_ACCESS_TOKEN)

        user_info = get_user_info(databricks_token)
        user_email = user_info["user_email"]

        # If this user has no chat history, initialize an empty history
        if user_email not in history:
            history[user_email] = [{"role": "system", "content": PROMPT}]
        history[user_email].append({"role": "user", "content": message.strip()})
        
        # START NEW
        db = SQLDatabase.from_databricks(
            warehouse_id="edbc05107238f51d",
            catalog="samples",
            schema="nyctaxi",
            host=os.getenv("DATABRICKS_HOST"),
            api_token=databricks_token
        )
        
        llm = OpenAI(temperature=.7)
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)
        response = agent.run(message)

        # END NEW
        print(response)
        history[user_email].append({"role": "assistant", "content": response})
        print(history[user_email])
        chat_history.append((message, response))
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])

app = gr.mount_gradio_app(app, demo, "/")

if __name__ == "__main__":
    uvicorn.run(app)