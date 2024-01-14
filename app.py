import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def send_messages(names, contacts, message, driver, st):
    # Loop through data and send messages
    for idx, (name, number) in enumerate(zip(names, contacts)):
        number = str(number).strip()
        if number == "":
            continue
        try:
            url = f'https://web.whatsapp.com/send?phone={number}&text=Dear {name}, {message}'
            sent = False
            for i in range(2):
                if not sent:
                    driver.get(url)
                    try:
                        # You may need to adjust the delay and element selection based on your needs
                        time.sleep(30)
                        click_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-tab='11']")))
                    except Exception as e:
                        st.error(f"Failed to send message to: {number}, retry ({i+1}/2)")
                        st.error("Make sure your phone and computer are connected to the internet.")
                        # st.error("If there is an alert, please dismiss it.")
                    else:
                        time.sleep(1)
                        click_btn.click()
                        sent = True
                        time.sleep(5)
                        st.write(f"Message sent to: {number}")
        except Exception as e:
            st.error(f"Failed to send message to {number}: {e}")

st.set_page_config(layout="wide", 
                   page_icon='💬', 
                   page_title='WhatsApp Automation')
st.title("💬 _WhatsApp Automation_")
st.markdown("Excel data column names should be as follows: 👇🏻")
code = '''
data = {
    'Column Names': ['Contact', 'Names']
}
'''
st.code(code, language='python')

# UI for uploading file and sending messages
uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx", "xls"])

if 'data' not in st.session_state:
    st.session_state.data = None

if uploaded_file is not None:
    st.session_state.data = pd.read_excel(uploaded_file)

if st.session_state.data is not None:
    # Display the uploaded data
    st.write("Uploaded data:")
    st.write(st.session_state.data)
    names = st.session_state.data.get("Names", [])
    contacts = st.session_state.data.get("Contact", [])
    st.info('Click on QR Code Button, scan your QR code to Web WhatsApp')
    if st.button('Scan QR Code'):
        if 'driver' not in st.session_state:
            service = Service('G:/Habibi/WhatsApp Automation/chromedriver.exe')
            service.start()
            options = Options()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--profile-directory=Default")
            options.add_argument("--user-data-dir=G:/Habibi/WhatsApp Automation/var/tmp/chrome_user_data")

            st.session_state.driver = webdriver.Chrome(service=service, options=options)
            st.session_state.driver.get('https://web.whatsapp.com/')
            time.sleep(5)
    
    message = st.text_area("Enter your message here", "")
    st.info('After scanning QR Code, now you are ready to send bulk messages.')
    
    if st.button("Send Messages"):
        if 'driver' not in st.session_state:
            st.session_state.driver.get('https://web.whatsapp.com/send?phone=+12345678910')
            time.sleep(5)
        
        send_messages(names, contacts, message, st.session_state.driver, st)
