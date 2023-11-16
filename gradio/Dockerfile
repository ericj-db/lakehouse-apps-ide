FROM python:3.9.18
RUN mkdir -p /gradio/app
COPY ./app /gradio/app
WORKDIR /gradio/app
RUN pip install -r /gradio/app/requirements.txt
EXPOSE 8050
CMD ["uvicorn", "gradio_app:app", "--reload", "--host", "0.0.0.0", "--port", "8050"]
