import gradio as gr
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile

custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
.gradio-container {font-family: 'Poppins', sans-serif !important; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;}
#header {text-align: center; color: white; padding: 40px 20px; background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); border-radius: 25px; margin: 20px; border: 1px solid rgba(255,255,255,0.3); box-shadow: 0 8px 32px rgba(0,0,0,0.1);}
#header h1 {font-size: 3.2em; font-weight: 700; margin-bottom: 15px; text-shadow: 2px 2px 8px rgba(0,0,0,0.2);}
#header p {font-size: 1.2em; opacity: 0.95;}
.main-box {background: white; padding: 45px; border-radius: 25px; box-shadow: 0 20px 60px rgba(0,0,0,0.25); margin: 20px;}
.translate-btn {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; border: none !important; font-size: 18px !important; font-weight: 600 !important; padding: 16px !important; border-radius: 12px !important;}
.translate-btn:hover {transform: translateY(-3px); box-shadow: 0 12px 24px rgba(102, 126, 234, 0.5) !important;}
#footer {text-align: center; color: white; padding: 30px; margin-top: 30px;}
#footer a {color: white !important; text-decoration: none; margin: 0 15px; font-weight: 600;}
#footer a:hover {text-decoration: underline;}
"""

languages = {
"English": "en", "French": "fr", "Spanish": "es", "German": "de", 
"Arabic": "ar", "Italian": "it", "Japanese": "ja", "Chinese": "zh-CN", 
"Korean": "ko", "Portuguese": "pt"
}

def translate_text(text, src_lang, dest_lang):
    if not text.strip():
        return "⚠️ Please enter text to translate", None
    try:
        src_code = languages[src_lang]
        dest_code = languages[dest_lang]
        translated = GoogleTranslator(source=src_code, target=dest_code).translate(text)
        tts = gTTS(text=translated, lang=dest_code)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            return translated, fp.name
    except Exception as e:
        return f"❌ Error: {str(e)}", None

with gr.Blocks(css=custom_css, theme=gr.themes.Base(), title="CodeAlpha AI Translator") as demo:
    gr.HTML('''
        <div id="header">
            <h1>🌍 CodeAlpha AI Translator</h1>
            <p>Task 1 | CodeAlpha AI Internship 2026</p>
            <p style="font-size: 1em; margin-top: 10px;">Real-time Translation + Text-to-Speech</p>
        </div>
    ''')
    
    with gr.Column(elem_classes="main-box"):
        gr.Markdown("## 🔄 Select Languages")
        with gr.Row():
            src = gr.Dropdown(choices=list(languages.keys()), value="English", label="From Language")
            dest = gr.Dropdown(choices=list(languages.keys()), value="Arabic", label="To Language")
        
        text = gr.Textbox(label="📝 Enter Your Text", value="Hello! I am a CodeAlpha AI Intern.", lines=5, placeholder="Type or paste your text here...")
        btn = gr.Button("✨ Translate Now", variant="primary", elem_classes="translate-btn")
        
        gr.Markdown("## 🎯 Translation Results")
        with gr.Row():
            out_text = gr.Textbox(label="✨ Translation", lines=5, interactive=False)
            out_audio = gr.Audio(label="🔊 Listen to Audio", type="filepath")
    
    btn.click(fn=translate_text, inputs=[text, src, dest], outputs=[out_text, out_audio])
    
    gr.HTML('''
        <div id="footer">
            <p>© 2026 CodeAlpha AI Internship</p>
            <p style="margin-top: 15px;">
                <a href="https://github.com/zineb36-star">💻 GitHub</a>
                <a href="https://huggingface.co/zineb36">🤗 Hugging Face</a>
                <a href="https://codealpha.tech">🚀 CodeAlpha</a>
            </p>
        </div>
    ''')

demo.launch()
