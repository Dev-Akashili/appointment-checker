from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

# Create an object as reference for parsing the data from the site
obj = [ {"name": "slot_name", "type": "slot_type"} ]

# Create a new instance of the Chrome browser
driver = webdriver.Chrome()

def goToSite():
    try:
        # Navigate to the website
        driver.get("https://sample_site.com")
        time.sleep(5)  # Give some time for the site to load completely
        driver.find_element(By.ID, "username").send_keys("your_username")
        driver.find_element(By.ID, "password").send_keys("your_password")
        time.sleep(5)
        print("Opened site successfully.")
    except Exception as error:
        print("Site Opening Error:", error)

def logIn():
    try:
        goToSite()
        driver.find_element(By.ID, "the_site_login_button_id").click()
        time.sleep(5)
        print("Logged in successfully.")
    except Exception as error:
        print("Login Error:", error)

def openNewTab():
    try:
        logIn()
        global tab1, tab2
        tab1 = driver.current_window_handle
        driver.execute_script("window.open('');")
        tabs = driver.window_handles
        driver.switch_to.window(tabs[1])
        tab2 = driver.current_window_handle
        time.sleep(2)
        print("Tab opened successfully")
    except Exception as error:
        print("Opening New Tab Error:", error)

def sendEmail(email):
    try:
        response = requests.post("https://api.emailjs.com/api/v1.0/email/send", json=email)
        if response.status_code == 200:
            print("Email successfully sent!")
        else:
            print("Error sending email:", response.text)
    except Exception as error:
        print("Error sending email:", error)

def getSlots(data, name):
    slots = []
    for date, times in data.items():
        for time, value in times.items():
            if value != 0:
                slots.append({"Date": date, "Time": time, "Value": value})

    if slots:
        emailContent = "Available slots:\n"
        for slot in slots:
            emailContent += f"{slot['Date']} {slot['Time']} {slot['Value']}\n"

        email = {
            "service_id": "your_service_id",
            "template_id": "your_template_id",
            "user_id": "your_public_key",
            "template_params": {
                "message": emailContent,
                "email": "your_email"
            }
        }

        sendEmail(email)
    else:
        print(f"No {name} Slots Available Yet...")

def fetchData():
    for item in obj:
        if not item["type"]:
            print("No Weekend Slots Available Yet...")
            continue

        try:
            driver.get(item["type"])
            time.sleep(3)
            pageSource = driver.page_source
            startIndex = pageSource.find("{")
            endIndex = pageSource.rfind("}")
            jsonString = pageSource[startIndex:endIndex + 1]
            jsonData = eval(jsonString)  # Using eval to parse JSON string to dictionary

            getSlots(jsonData, item["name"])
        except Exception as error:
            print("Get Data Error:", error)

    global count
    count += 1
    print("Check Count:", count)

# Refresh the site every few minutes to keep session
def refreshTLS():
    try:
        driver.switch_to.window(tab1)
        driver.refresh()
        time.sleep(3)
        driver.switch_to.window(tab2)
        print("Site refreshed successfully")
    except Exception as error:
        print("Refreshing TLS Error:", error)

openNewTab()

# Run the Task
count = 0
while True:
    fetchData()
    if count % 10 == 0:
        refreshTLS()
    time.sleep(60)
