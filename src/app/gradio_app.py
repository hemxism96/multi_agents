"""Renault Intelligence Agent - Gradio Interface Application"""

import gradio as gr
from main import run


def generate_response(question: str) -> str:
    """Generates a response to the provided question using the main run function."""
    response = run(question)
    return response


with gr.Blocks() as app:
    """Gradio application for the Renault Intelligence Agent."""
    gr.Markdown("Renault Intelligence Agent")

    with gr.Row():
        with gr.Column():
            question = gr.Textbox(label="Question")
            submit_button = gr.Button("Submit")
        with gr.Column():
            response = gr.Textbox(label="Response")

    submit_button.click(fn=generate_response, inputs=question, outputs=response)

app.launch()
