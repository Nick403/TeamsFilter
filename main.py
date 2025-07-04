import json, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.properties import StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    text = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos):
            rv = self.parent.parent
            rv.parent.remove_at(self.index)
            return True
        return False

class AllowListView(RecycleView):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.refresh()

    def refresh(self):
        self.data = [{'text': term} for term in self.manager.allow_list]

class AllowListManager(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.file_path = os.path.join(App.get_running_app().user_data_dir, 'allow_list.json')
        self.allow_list = self.load_list()
        self.add_widget(Label(text="Teams Caller Allow‑List", size_hint_y=None, height='40dp'))
        self.input = TextInput(hint_text="Type name/number then Add", size_hint_y=None, height='40dp')
        self.add_widget(self.input)
        buttons = BoxLayout(size_hint_y=None, height='40dp')
        add_btn = Button(text="Add")
        add_btn.bind(on_release=self.add_term)
        save_btn = Button(text="Save")
        save_btn.bind(on_release=self.save_list)
        buttons.add_widget(add_btn)
        buttons.add_widget(save_btn)
        self.add_widget(buttons)
        self.rv = AllowListView(self)
        self.add_widget(self.rv)

    def refresh_rv(self):
        self.rv.refresh()

    def add_term(self, *args):
        term = self.input.text.strip()
        if term and term.lower() not in {t.lower() for t in self.allow_list}:
            self.allow_list.append(term)
            self.input.text = ""
            self.refresh_rv()

    def remove_at(self, index):
        if 0 <= index < len(self.allow_list):
            self.allow_list.pop(index)
            self.refresh_rv()

    def save_list(self, *args):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as fp:
            json.dump(self.allow_list, fp, indent=2, ensure_ascii=False)
        self.refresh_rv()

    def load_list(self):
        try:
            with open(self.file_path, encoding='utf-8') as fp:
                return json.load(fp)
        except Exception:
            return []

class TeamsFilterApp(App):
    def build(self):
        return AllowListManager()

if __name__ == '__main__':
    TeamsFilterApp().run()
