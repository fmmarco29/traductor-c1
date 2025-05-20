import gradio as gr
import os
import openai
import anthropic
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
APP_PASSWORD = os.getenv("APP_PASSWORD")

# Inicializar clientes
openai_client = openai.OpenAI()
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# Función principal de traducción
def translate_and_transform(text, transformation, openai_model, anthropic_model, llama_model):
    prompt = f"""
Traduce el siguiente texto al inglés nivel C1, aplicando esta transformación gramatical: {transformation}.

Texto: {text}

Formato de salida:
B2: ...
C1: ...
Diferencias: ...
"""
    try:
        openai_response = openai_client.chat.completions.create(
            model=openai_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        ).choices[0].message.content.strip()
    except Exception as e:
        openai_response = f"❌ OpenAI error: {str(e)}"

    try:
        anthropic_response = anthropic_client.messages.create(
            model=anthropic_model,
            max_tokens=1000,
            temperature=0.7,
            system="Eres un traductor experto en inglés C1.",
            messages=[{"role": "user", "content": prompt}]
        ).content[0].text.strip()
    except Exception as e:
        anthropic_response = f"❌ Anthropic error: {str(e)}"

    # Aquí deberías integrar LLaMA si tienes acceso o usar Hugging Face Inference API
    llama_response = f"(Simulación) Traducción con modelo {llama_model}:\n\nB2: [traducción simulada]\n\nC1: [versión avanzada simulada]\n\nDiferencias: explicación simulada"

    return openai_response, anthropic_response, llama_response

# Función de acceso con contraseña
def verify_password(password):
    if password == APP_PASSWORD:
        return gr.update(visible=False), gr.update(visible=True), ""
    else:
        return gr.update(visible=True), gr.update(visible=False), "❌ Contraseña incorrecta"

# Interfaz Gradio
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# 🔐 Traductor C1 - Acceso restringido")

    with gr.Column(visible=True) as login:
        pwd = gr.Textbox(label="Introduce la contraseña", type="password")
        login_btn = gr.Button("Entrar")
        login_msg = gr.Markdown("")

    with gr.Column(visible=False) as app:
        gr.Markdown("## 🧠 Traductor avanzado de español a inglés - Nivel C1")

        input_text = gr.Textbox(label="Texto en español", lines=3)

        transformation = gr.Radio(
            choices=[
                "3ª Condicional Invertida",
                "Inversión Enfática",
                "Cleft Sentence",
                "Relative Clause"
            ],
            label="Transformación gramatical",
            elem_classes="uniform-buttons"
        )

        with gr.Row():
            openai_model = gr.Dropdown(
                choices=["gpt-4o", "gpt-4", "gpt-3.5-turbo"],
                label="Modelo OpenAI",
                value="gpt-4o"
            )
            anthropic_model = gr.Dropdown(
                choices=["claude-3-opus-20240229", "claude-3-sonnet-20240229"],
                label="Modelo Anthropic",
                value="claude-3-opus-20240229"
            )
            llama_model = gr.Dropdown(
                choices=["meta-llama/Meta-Llama-3-8B-Instruct", "meta-llama/Meta-Llama-2-13B-chat"],
                label="Modelo LLaMA",
                value="meta-llama/Meta-Llama-3-8B-Instruct"
            )

        translate_button = gr.Button("🔁 Traducir")

        with gr.Row():
            openai_output = gr.Textbox(label="🧠 OpenAI", lines=10)
            anthropic_output = gr.Textbox(label="🤖 Anthropic", lines=10)
            llama_output = gr.Textbox(label="🦙 LLaMA (simulado)", lines=10)

    login_btn.click(verify_password, inputs=[pwd], outputs=[login, app, login_msg])
    translate_button.click(
        translate_and_transform,
        inputs=[input_text, transformation, openai_model, anthropic_model, llama_model],
        outputs=[openai_output, anthropic_output, llama_output]
    )

demo.launch()
