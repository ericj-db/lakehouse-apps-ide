import random
import gradio as gr

def random_response(message, history):
    return random.choice(["Yes", "No", "Maybe"])

demo = gr.ChatInterface(random_response)

demo.launch()
