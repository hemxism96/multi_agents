import gradio as gr

from main import run

def generate_response(question: str) -> str:
    response = run(question)
    return response


with gr.Blocks() as app:
    gr.Markdown("Renault Group Corporate Analyst")

    with gr.Row():
        with gr.Column():
            question = gr.Textbox(label="Question")
            submit_button = gr.Button("Submit")
        with gr.Column():
            response = gr.Textbox(label="Response")

    submit_button.click(fn=generate_response, inputs=question, outputs=response)

app.launch()
