
import gradio as gr
import openai
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
APP_PASSWORD = os.getenv("APP_PASSWORD")

anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)

def translate_and_transform(text, transformation, openai_model, anthropic_model, llama_model):
    prompt = f"""
    Traduce el siguiente texto al inglés nivel C1, aplicando esta transformación gramatical: {transformation}.

    Texto: {text}

    Formato de salida:
    B2: ...
    C1: ...
    Diferencias: ...
    """
    openai_response = openai.ChatCompletion.create(
        model=openai_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )["choices"][0]["message"]["content"]

    anthropic_response = anthropic_client.messages.create(
        model=anthropic_model,
        max_tokens=1000,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    ).content[0].text

    llama_response = f"(Simulación) Traducción con modelo {llama_model}:
" + prompt

    return openai_response, anthropic_response, llama_response

def verify_password(password):
    if password == APP_PASSWORD:
        return gr.update(visible=False), gr.update(visible=True), ""
    else:
        return gr.update(visible=True), gr.update(visible=False), "❌ Contraseña incorrecta"

with gr.Blocks(theme=gr.themes.Base(dark=True)) as demo:
    gr.Markdown("# 🔐 Traductor C1 - Acceso restringido")

    with gr.Column(visible=True) as login:
        pwd = gr.Textbox(label="Introduce la contraseña", type="password")
        login_btn = gr.Button("Entrar")
        login_msg = gr.Markdown("")

    with gr.Column(visible=False) as app:
        gr.Markdown("## 🧠 Traductor avanzado de español a inglés C1")
        input_text = gr.Textbox(label="Texto en español", lines=3)
        transformation = gr.Radio(
            choices=["3ª Condicional Invertida", "Inversión Enfática", "Cleft Sentence", "Relative Clause"],
            label="Transformación gramatical"
        )
        with gr.Row():
            openai_model = gr.Dropdown(["gpt-4o-mini-2024-07-18", "gpt-4.1-mini-2025-04-14"], label="Modelo OpenAI", value="gpt-4o-mini-2024-07-18")
            anthropic_model = gr.Dropdown(["claude-3-5-haiku-20241022", "claude-3-haiku-20240307"], label="Modelo Anthropic", value="claude-3-opus-20240229")
            llama_model = gr.Dropdown(["meta-llama/Llama-2-7b-chat-hf"], label="Modelo LLaMA", value="meta-llama/Llama-2-7b-chat-hf")
        translate_button = gr.Button("Traducir")
        with gr.Row():
            openai_output = gr.Textbox(label="OpenAI", lines=10)
            anthropic_output = gr.Textbox(label="Anthropic", lines=10)
            llama_output = gr.Textbox(label="LLaMA", lines=10)
    login_btn.click(verify_password, inputs=[pwd], outputs=[login, app, login_msg])
    translate_button.click(translate_and_transform, inputs=[input_text, transformation, openai_model, anthropic_model, llama_model], outputs=[openai_output, anthropic_output, llama_output])

demo.launch()
