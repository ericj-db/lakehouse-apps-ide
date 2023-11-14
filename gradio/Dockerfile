FROM python:3.9.18
RUN mkdir -p /gradio/app
COPY ./app /gradio/app
WORKDIR /gradio/app
RUN pip install -r /gradio/app/requirements.txt
CMD ["gradio", "gradio_app.py"]
