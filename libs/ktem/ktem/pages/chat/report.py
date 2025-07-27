from typing import Optional

import gradio as gr
from ktem.app import BasePage
from ktem.db.models import IssueReport, engine
from sqlmodel import Session


class ReportIssue(BasePage):
    def __init__(self, app):
        self._app = app
        self.on_building_ui()

    def on_building_ui(self):
        with gr.Accordion(label="بازخورد", open=False, elem_id="report-accordion"):
            self.correctness = gr.Radio(
                choices=[
                    (" پاسخ صحیح است ", "correct"),
                    (" پاسخ اشتباه است ", "incorrect"),
                ],
                label="صحت سنجی:",
            )
            self.issues = gr.CheckboxGroup(
                choices=[
                    (" پاسخ نامحترمانه است ", "offensive"),
                    (" مدارک اشتباه است ", "wrong-evidence"),
                ],
                label="دیگر مشکلات:",
            )
            self.more_detail = gr.Textbox(
                placeholder=(
                    "جزئیات بیشتر (مثلا چقدر اشتباه است، پاسخ صحیح چیست، و غیره...)"
                ),
                container=False,
                lines=3,
            )
            alert_text = "این عمل، چت فعلی و تنظیمات کاربر را برای کمک به تحقیق ارسال خواهد کرد"
            gr.Markdown(f'<div dir="rtl"> {alert_text}</div>')
            self.report_btn = gr.Button("گزارش")

    def report(
        self,
        correctness: str,
        issues: list[str],
        more_detail: str,
        conv_id: str,
        chat_history: list,
        settings: dict,
        user_id: Optional[int],
        info_panel: str,
        chat_state: dict,
        *selecteds,
    ):
        selecteds_ = {}
        for index in self._app.index_manager.indices:
            if index.selector is not None:
                if isinstance(index.selector, int):
                    selecteds_[str(index.id)] = selecteds[index.selector]
                elif isinstance(index.selector, tuple):
                    selecteds_[str(index.id)] = [selecteds[_] for _ in index.selector]
                else:
                    print(f"Unknown selector type: {index.selector}")

        with Session(engine) as session:
            issue = IssueReport(
                issues={
                    "correctness": correctness,
                    "issues": issues,
                    "more_detail": more_detail,
                },
                chat={
                    "conv_id": conv_id,
                    "chat_history": chat_history,
                    "info_panel": info_panel,
                    "chat_state": chat_state,
                    "selecteds": selecteds_,
                },
                settings=settings,
                user=user_id,
            )
            session.add(issue)
            session.commit()
        gr.Info("از بازخورد شما متشکریم")
