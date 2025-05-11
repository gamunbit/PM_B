from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.text import LabelBase
import os
import json

# ===== 한글 폰트 등록 =====
LabelBase.register(
    name="NotoSansKR",
    fn_regular="NotoSansKR-Regular.ttf"
)

# ===== 앱 UI 레이아웃 =====
class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.server_url = self.load_server_url()

        self.label = Label(
            text="QR 스캔을 시작하려면 아래 버튼을 누르세요",
            font_name="NotoSansKR",
            font_size=20
        )
        self.add_widget(self.label)

        self.scan_button = Button(
            text="QR 스캔",
            font_name="NotoSansKR",
            font_size=24,
            size_hint=(1, 0.3)
        )
        self.scan_button.bind(on_press=self.scan_qr)
        self.add_widget(self.scan_button)

    def load_server_url(self):
        path = "/sdcard/PMApp/server_url.json"
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)["url"]
        except Exception as e:
            print(f"[경고] 서버 주소 로드 실패: {e}")
            return "https://example.ngrok-free.app"  # 기본 주소

    def scan_qr(self, instance):
        dummy_qr = "PM123"
        self.label.text = f"스캔된 ID: {dummy_qr}"
        self.send_to_server(dummy_qr)

    def send_to_server(self, device_id):
        import requests
        try:
            res = requests.post(
                self.server_url,
                json={"device_id": device_id}
            )
            result = res.json().get("result", "응답 없음")
            self.label.text = f"서버 응답: {result}"
        except Exception as e:
            self.label.text = f"[에러] 서버 연결 실패\n{e}"

# ===== 앱 실행부 =====
class QRApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    QRApp().run()
