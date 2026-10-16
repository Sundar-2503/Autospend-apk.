import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.utils import platform
import requests

# Optional: Set your hosted FastAPI Backend URL here if you deploy the backend
BACKEND_URL = "http://127.0.0.1:8000/log-expense"

class ExpenseTrackerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        self.status_label = Label(
            text="Automated Expense Tracker\nTap below to scan bank SMS", 
            size_hint=(1, 0.15),
            halign="center"
        )
        self.layout.add_widget(self.status_label)

        scan_btn = Button(
            text="Scan Inbox for Expenses", 
            size_hint=(1, 0.12),
            background_color=(0.1, 0.6, 0.8, 1)
        )
        scan_btn.bind(on_press=self.scan_sms)
        self.layout.add_widget(scan_btn)

        self.scroll = ScrollView(size_hint=(1, 0.73))
        self.list_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        self.scroll.add_widget(self.list_layout)
        self.layout.add_widget(self.scroll)

        if platform == 'android':
            self.request_android_permissions()

        return self.layout

    def request_android_permissions(self):
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.READ_SMS, 
            Permission.RECEIVE_SMS, 
            Permission.INTERNET
        ])

    def scan_sms(self, instance):
        self.list_layout.clear_widgets()
        if platform == 'android':
            self.read_android_sms()
        else:
            # Dummy test data when testing on Laptop
            sample_msgs = [
                "Rs. 250.00 debited from A/c XX1234 on 16-10-26 to VPA swiggy@upi.",
                "INR 1,200.50 spent on HDFC Card XX5678 at Amazon.",
                "Dear Customer, Rs.75.00 paid via UPI to Zomato.",
                "Your OTP is 458921. Do not share it."
            ]
            self.process_messages(sample_msgs)

    def read_android_sms(self):
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Uri = autoclass('android.net.Uri')
            
            activity = PythonActivity.mActivity
            content_resolver = activity.getContentResolver()
            uri = Uri.parse("content://sms/inbox")
            
            # Fetch latest 100 SMS messages
            cursor = content_resolver.query(uri, ["address", "body", "date"], None, None, "date DESC LIMIT 100")
            
            messages = []
            if cursor and cursor.moveToFirst():
                body_idx = cursor.getColumnIndex("body")
                while True:
                    body = cursor.getString(body_idx)
                    if body:
                        messages.append(body)
                    if not cursor.moveToNext():
                        break
                cursor.close()
            
            self.process_messages(messages)
        except Exception as e:
            self.status_label.text = f"Error reading SMS: {str(e)}"

    def process_messages(self, messages):
        expense_pattern = re.compile(
            r'(?:Rs\.?|INR)\s*([\d,]+\.?\d*).*?(?:debited|spent|paid|sent)', 
            re.IGNORECASE
        )
        
        found_count = 0
        for msg in messages:
            match = expense_pattern.search(msg)
            if match:
                amount = match.group(1).replace(',', '')
                found_count += 1
                
                item = Label(
                    text=f"Spent: Rs. {amount}\n{msg[:70]}...", 
                    size_hint_y=None, 
                    height=110,
                    halign="left",
                    valign="middle"
                )
                item.bind(size=item.setter('text_size'))
                self.list_layout.add_widget(item)
                
                # Optional backend sync
                self.sync_to_backend(amount, msg)

        self.status_label.text = f"Found {found_count} expense transactions."

    def sync_to_backend(self, amount, raw_sms):
        try:
            requests.post(
                BACKEND_URL, 
                json={"amount": float(amount), "description": raw_sms}, 
                timeout=2
            )
        except Exception:
            pass

if __name__ == '__main__':
    ExpenseTrackerApp().run()
