"""
Monika Prank - Press 50 times to leave
Every close attempt (X, Alt+F4, Esc, Android back) counts as one press.
At 50 presses, the app finally closes.
"""

import os
import io
import random
import shutil
import urllib.request

# ---- clear Kivy's cached failed image loads ----
cache_dir = os.path.expanduser("~/.kivy/cache")
if os.path.exists(cache_dir):
    shutil.rmtree(cache_dir, ignore_errors=True)

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock

# ---------------- settings ----------------
MONIKA_URL = "https://i.imgur.com/YJwJ82v.jpeg"
PRESSES_TO_LEAVE = 939399939

MESSAGES = [
    "There's no point in saving anymore.",
    "I'm not going anywhere.",
    "Why would you try to leave?",
    "Just Monika.",
    "You can't close me.",
    "Keep trying. It won't help.",
    "I could do this forever.",
]


def load_texture_from_url(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
            "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://imgur.com/",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read()
    ext = "png" if url.lower().endswith(".png") else "jpeg"
    return CoreImage(io.BytesIO(data), ext=ext).texture


# ---------------- UI ----------------
class MonikaPrank(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.presses = 0

        # Background image (canvas fill so no black bars)
        self.bg = Widget(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        with self.bg.canvas:
            self.rect = Rectangle(pos=self.bg.pos, size=self.bg.size)
        self.bg.bind(pos=self.update_rect, size=self.update_rect)
        self.add_widget(self.bg)

        # Dialogue label at the bottom
        self.msg = Label(
            text="Loading...",
            font_size='22sp',
            size_hint=(1, 0.22),
            pos_hint={'x': 0, 'y': 0},
            halign='center',
            valign='middle',
            color=(1, 1, 1, 1),
            outline_color=(0, 0, 0, 1),
            outline_width=2,
        )
        self.msg.bind(size=lambda *a: setattr(self.msg, 'text_size', self.msg.size))
        self.add_widget(self.msg)

        # Small counter at the top
        self.counter = Label(
            text=f"0 / {PRESSES_TO_LEAVE}",
            font_size='16sp',
            size_hint=(1, 0.05),
            pos_hint={'x': 0, 'y': 0.95},
            halign='center',
            valign='middle',
            color=(1, 1, 1, 0.6),
            outline_color=(0, 0, 0, 0.8),
            outline_width=1,
        )
        self.counter.bind(size=lambda *a: setattr(self.counter, 'text_size', self.counter.size))
        self.add_widget(self.counter)

        Clock.schedule_once(self.fetch_image, 0.1)
        Clock.schedule_interval(self.cycle_message, 2.5)

    def update_rect(self, *args):
        self.rect.pos = self.bg.pos
        self.rect.size = self.bg.size

    def fetch_image(self, dt):
        try:
            self.rect.texture = load_texture_from_url(MONIKA_URL)
            self.msg.text = random.choice(MESSAGES)
            print("Image loaded OK")
        except Exception as e:
            self.msg.text = f"Image failed: {e}"
            print("Image load failed:", e)

    def cycle_message(self, dt):
        if not self.msg.text.startswith("Image failed"):
            self.msg.text = random.choice(MESSAGES)

    def register_press(self):
        """Count one close attempt. Return True if the app should now close."""
        self.presses += 1
        remaining = PRESSES_TO_LEAVE - self.presses

        if self.presses >= PRESSES_TO_LEAVE:
            self.counter.text = "Fine. I'll go."
            return True

        # Taunt with a Monika line + show progress
        self.msg.text = random.choice(MESSAGES)
        self.counter.text = f"{self.presses} / {PRESSES_TO_LEAVE}  ({remaining} left)"
        return False


# ---------------- app ----------------
class PrankApp(App):
    def build(self):
        self.title = "Just Monika"

        Window.fullscreen = 'auto'
        Window.borderless = True
        Window.always_on_top = True

        Window.bind(on_request_close=self.on_request_close)
        Window.bind(on_key_down=self.on_key_down)

        return MonikaPrank()

    def on_request_close(self, *args):
        if self.root and self.root.register_press():
            return False   # allow close now that 50 presses happened
        return True        # otherwise block

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        # Esc, Android back, Alt+F4 all count as close attempts
        is_close_key = (
            key in (27, 1001)
            or (key == 1073741926 and 'alt' in modifiers)
        )
        if is_close_key:
            if self.root and self.root.register_press():
                self.stop()
            return True
        return False


if __name__ == "__main__":
    PrankApp().run()