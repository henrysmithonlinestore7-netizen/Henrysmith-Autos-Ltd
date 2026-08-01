from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import os
import webbrowser
import threading


class Launcher(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=12, spacing=12, **kwargs)
        self.status = Label(text='Preparing dashboard...', size_hint_y=None, height='40dp')
        self.add_widget(self.status)
        self.open_btn = Button(text='Open dashboard (external browser)', size_hint_y=None, height='48dp')
        self.open_btn.bind(on_release=lambda *_: threading.Thread(target=self.open_dashboard).start())
        self.add_widget(self.open_btn)

    def open_dashboard(self):
        try:
            # Try to read the packaged HTML file from the source tree
            src_path = os.path.join(os.path.dirname(__file__), 'pages', 'dashboard.html')
            if not os.path.exists(src_path):
                # If not found, try relative path (some packaging environments differ)
                src_path = os.path.join(os.getcwd(), 'src', 'pages', 'dashboard.html')

            with open(src_path, 'rb') as f:
                data = f.read()

            # Write to a location the Android browser can access (app user_data_dir)
            dest_dir = App.get_running_app().user_data_dir
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, 'dashboard.html')
            with open(dest_path, 'wb') as f:
                f.write(data)

            url = 'file://' + dest_path
            webbrowser.open(url)
            Clock.schedule_once(lambda dt: self._set_status(f'Opened: {dest_path}'), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self._set_status(f'Failed: {e}'), 0)

    def _set_status(self, text):
        self.status.text = text


class HenrySmithApp(App):
    def build(self):
        return Launcher()


if __name__ == '__main__':
    HenrySmithApp().run()
