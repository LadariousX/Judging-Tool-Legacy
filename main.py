from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from time import sleep
from PIL import Image
from MultiEmailTool import send_email
from datetime import datetime

# parameters
debug_mode = False
teamName = "Edna"
prevResults = []
chrome_status = True

if debug_mode:
    print("### DEBUG MODE ###")
    update_interval = 5
    load_period = 1
    timeRange = range(0, 24)
    recipients = ["3612357978@mms.att.net", "laydenlblackwell@gmail.com"]

else:
    update_interval = (7 * 60)
    load_period = 5
    timeRange = range(8, 22)
    recipients = ["
                  "number@mms.att.net",  # example adresses
                  "email@domain.com",
                  ]

Odometer = 0


def read_rows():
    new_event_results = {}
    rows_discovered = (len(driver.find_elements(By.TAG_NAME, "a")) - 3)
    for rows in range(rows_discovered):
        # print ("rows: ",rows)
        xpath = f"/html/body/form/div[3]/div[2]/div[2]/div/div/table/tbody/tr[{rows + 1}]/td[2]/a"
        xpath_results = driver.find_element(By.XPATH, xpath).text
        new_event_results[xpath_results] = xpath
    return new_event_results


def screenshot():
    driver.save_screenshot('Results JC Raw.png')
    base_w = 1080
    img = Image.open('Results JC Raw.png')
    w_percent = (base_w / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((base_w, hsize), Image.Resampling.LANCZOS)
    img.save('Results JC post process.png')

service = Service(executable_path=r'/usr/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument("no-sandbox")
options.add_argument("headless")
options.add_argument("disable-gpu")
driver = webdriver.Chrome(service = service, options = options)


while True:
    # Time out loop to stop checking after hours
    currTime = datetime.now()
    while int(currTime.strftime("%H")) not in timeRange:
        if chrome_status:
            driver.close()
            chrome_status = False
        print("outta time one hr nap")
        print("current hour: ", currTime.strftime("%H:%M:%S"))
        sleep(60 * 60)
        currTime = datetime.now()
    if not chrome_status:
        driver = webdriver.Chrome("/usr/bin/chromedriver", options = options)
        chrome_status = True

    driver.get("https://www.judgingcard.com/Results/")

    Odometer += 1
    print("Odometer", Odometer)
    print(currTime.strftime("%H:%M:%S"))
    sleep(load_period)

    # search team
    driver.find_element(By.XPATH,
                        "/html/body/form/div[3]/div[2]/div[1]/table/tbody/tr[1]/td[1]/select/option[45]").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_rbl_SearchBy_1").click()
    driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$txt_SearchString").clear()
    driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$txt_SearchString").send_keys(teamName)
    driver.find_element(By.NAME, "ctl00$ContentPlaceHolder1$txt_SearchString").send_keys(Keys.ENTER)
    sleep(load_period)

    if Odometer > 1:
        # get new results and subtract previous from current then check for changes
        row_dict = read_rows()
        new_Results = row_dict.keys()
        results_change = [z for z in new_Results if z not in prevResults]

        if debug_mode and Odometer == 2:
            # contest name extracted from the 'a' tag in early 2024
            results_change += [
                "Liberty Hill Applied Ag Engineering Invitational - Applied Ag Engineering - Combined - Edna"]

        if not results_change:
            print("No changes detected")
        else:
            print("changes detected: ", results_change[0])
            # isolate new event record, screenshot and email notify
            driver.find_element(By.XPATH, row_dict[results_change[0]]).click()
            sleep(load_period)
            contest_name = driver.find_element(By.XPATH,
                                               "/html/body/form/div[3]/div[2]/div/table/tbody/tr/td/div/span[1]").text
            screenshot()

            for address in recipients:
                send_email(address, results_change[0], driver.current_url)

        prevResults = new_Results

    elif Odometer == 1:
        print("initial census taken")
        prevResults = (read_rows()).keys()

    sleep(update_interval)
    driver.refresh()
