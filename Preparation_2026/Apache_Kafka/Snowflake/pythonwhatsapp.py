import pywhatkit as kit
import pyautogui
import time

phone_number = "+918618175504"
message = "Hello Vank peka, automated message 🚀"

# Step 1: Open WhatsApp Web and type message
kit.sendwhatmsg_instantly(phone_number, message, wait_time=20, tab_close=False)

# Step 2: Wait for message box to load
time.sleep(10)

# Step 3: Press Enter automatically
pyautogui.press("enter")

# Optional: close tab after sending
time.sleep(2)
pyautogui.hotkey("ctrl", "w")