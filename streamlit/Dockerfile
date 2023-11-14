FROM python:3.9.18
RUN mkdir -p /streamlit/app
COPY ./app /streamlit/app
WORKDIR /streamlit/app
RUN pip install -r /streamlit/app/requirements.txt
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8050", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false", "--server.enableWebsocketCompression", "false"]
