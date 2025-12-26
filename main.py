from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import sqlite3
import database

logged_agent = ""

class LoginScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10)
        self.app = app

        self.username = TextInput(hint_text="Username")
        self.password = TextInput(hint_text="Password", password=True)

        login_btn = Button(text="Login")
        login_btn.bind(on_press=self.login)

        self.msg = Label(text="")

        self.add_widget(self.username)
        self.add_widget(self.password)
        self.add_widget(login_btn)
        self.add_widget(self.msg)

    def login(self, instance):
        global logged_agent
        conn = sqlite3.connect("crm.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT username FROM agents
        WHERE username=? AND password=?
        """, (self.username.text, self.password.text))

        row = cursor.fetchone()
        conn.close()

        if row:
            logged_agent = row[0]
            self.app.show_crm()
        else:
            self.msg.text = "Invalid Login"

class CRM(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10)

        self.name = TextInput(hint_text="Customer Name")
        self.phone = TextInput(hint_text="Phone Number")
        self.status = TextInput(hint_text="Call Status")
        self.notes = TextInput(hint_text="Notes")

        save_btn = Button(text="Save Call")
        save_btn.bind(on_press=self.save_call)

        self.msg = Label(text="")
        self.list_box = BoxLayout(orientation='vertical', size_hint_y=None)
        self.list_box.bind(minimum_height=self.list_box.setter('height'))

        scroll = ScrollView()
        scroll.add_widget(self.list_box)

        self.add_widget(Label(text=f"Logged Agent: {logged_agent}"))
        self.add_widget(self.name)
        self.add_widget(self.phone)
        self.add_widget(self.status)
        self.add_widget(self.notes)
        self.add_widget(save_btn)
        self.add_widget(self.msg)
        self.add_widget(scroll)

    def save_call(self, instance):
        conn = sqlite3.connect("crm.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO calls
        (customer_name, phone_number, agent_name, call_status, notes)
        VALUES (?, ?, ?, ?, ?)
        """, (
            self.name.text,
            self.phone.text,
            logged_agent,
            self.status.text,
            self.notes.text
        ))

        conn.commit()
        conn.close()

        self.msg.text = "Call Saved Successfully!"

        self.name.text = ""
        self.phone.text = ""
        self.status.text = ""
        self.notes.text = ""

class CallCenterCRM(App):
    def build(self):
        database.init_db()
        self.root_widget = BoxLayout()
        self.show_login()
        return self.root_widget

    def show_login(self):
        self.root_widget.clear_widgets()
        self.root_widget.add_widget(LoginScreen(self))

    def show_crm(self):
        self.root_widget.clear_widgets()
        self.root_widget.add_widget(CRM())

CallCenterCRM().run()