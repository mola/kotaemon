import gradio as gr
from ktem.app import BasePage
from theflow.settings import settings as flowsettings

KH_DEMO_MODE = getattr(flowsettings, "KH_DEMO_MODE", False)

if not KH_DEMO_MODE:
    PLACEHOLDER_TEXT = (
        ".این شروع یک گفتگوی جدید است\n"
        ".با بارگذاری یک فایل یا یک آدرس وب شروع کنید\n "
        ".برای گزینه های بیشتر به برگه فایل ها مراجعه کنید "
    )
else:
    PLACEHOLDER_TEXT = (
        ".به دموی دیتال چت خوش آمدید \n"
        ".برای شروع، مکالمات قبلی بارگذاری شده را مرور کنید\n"
        ".برای نکات بیشتر به بخش راهنمایی مراجعه کنید"
    )


class ChatPanel(BasePage):
    def __init__(self, app):
        self._app = app
        self.on_building_ui()

    def on_building_ui(self):
        self.chatbot = gr.Chatbot(
            label=self._app.app_name,
            placeholder=PLACEHOLDER_TEXT,
            show_label=False,
            rtl = True,
            elem_id="main-chat-bot",
            show_copy_button=True,
            likeable=True,
            bubble_full_width=False,
        )
        with gr.Row():
            self.text_input = gr.MultimodalTextbox(
                interactive=True,
                scale=20,
                rtl=True,
                file_count="multiple",
                placeholder=(
                    "یک پیام بنویسید"
                ),
                container=False,
                show_label=False,
                elem_id="chat-input",
            )

    def submit_msg(self, chat_input, chat_history):
        """Submit a message to the chatbot"""
        return "", chat_history + [(chat_input, None)]
