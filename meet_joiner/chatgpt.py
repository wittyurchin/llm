import random
import traceback

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent import futures
from faker import Faker
import time
MEETING_JOIN_TIME_IN_MINS=60
meeting_url = "https://teams.live.com/meet/9560172420920?p=mqew0kk5c4Cb1Uij"
meeting_url = "https://teams.live.com/meet/9528992746395?p=DT9nlVXFGyGQECgV"

def join_teams_meeting(tuplea):
    meeting_url=tuplea[0]
    guest_name=tuplea[1]
    # Initialize the WebDriver (you may need to download the appropriate webdriver for your browser)
    # driver = webdriver.Chrome()  # You can use other browsers like Firefox, Edge, etc.

    # Set Chrome options
    chrome_options = webdriver.ChromeOptions()

    # Disable microphone and camera permissions
    # https://stackoverflow.com/questions/66825943/how-to-reduce-chromedriver-cpu-usage-in-selenium-python
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-renderer-backgrounding");
    chrome_options.add_argument("--disable-background-timer-throttling");
    chrome_options.add_argument("--disable-backgrounding-occluded-windows");
    chrome_options.add_argument("--disable-client-side-phishing-detection");
    chrome_options.add_argument("--disable-crash-reporter");
    chrome_options.add_argument("--disable-oopr-debug-crash-dump");
    chrome_options.add_argument("--no-crash-upload");
    chrome_options.add_argument("--disable-gpu");
    chrome_options.add_argument("--disable-extensions");
    chrome_options.add_argument("--disable-low-res-tiling");
    chrome_options.add_argument("--log-level=3");
    chrome_options.add_argument("--silent");

    # Initialize the WebDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)
    print("chrome_options set")

    # Enter the meeting URL
    driver.get(meeting_url)
    print("accessed meeting link")

    # Wait for the meeting page to load
    # time.sleep(3)

    # elem = driver.find_element("xpath", "//*")
    # source_code = elem.get_attribute("outerHTML")
    # source_code=driver.getPageSource();

    # with open('./html_source_code_page1.html', 'w') as f:
    #     f.write(driver.page_source)
        # f.write(source_code.encode('utf-8'))
    try:
        # Click on the "Join as a guest" button. This step is not required on ubuntu
        join_as_guest_button=driver.find_element("xpath","//*[@data-tid='joinOnWeb']")
        # join_as_guest_button = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//*[@data-tid='joinOnWeb']"))
        # )
        join_as_guest_button.click()
    except:
        pass
    finally:
        print("Join as guest clicked")
        time.sleep(5)

    # elem = driver.find_element("xpath", "//*")
    # source_code = elem.get_attribute("outerHTML")
    # source_code=driver.getPageSource();

    # with open('./html_source_code.html', 'w') as f:
    #     f.write(driver.page_source)
        # f.write(source_code.encode('utf-8'))

    # select iframe first
    # iframe = driver.find_element("xpath", "//iframe[contains(@id, 'experience')]")
    iframe = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, "//iframe[contains(@id, 'experience')]"))
    )
    # iframe = driver.find_element("xpath","//iframe[@id='experience-container-1dbc2e5e-170f-4324-9f78-2ae6e10097ce']")
    driver.switch_to.frame(iframe)
    print("selected iframe")
    # Wait for the element to be present on the page
    name_input = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @placeholder='Type your name']"))
    )
    name_input.send_keys(guest_name)
    print("filled name")
    # inpiutname=driver.find_element("xpath","//input[@type='text' and @placeholder='Type your name']")
    # turn camera off
    video_btn = driver.find_element("xpath","//*[@data-tid='toggle-video']")
    video_is_on = video_btn.get_attribute("aria-checked")
    print(video_is_on)
    if video_is_on == "true":
        print('DEBUG: Video Turned Off')
        video_btn.click()


    # turn mute off
    audio_btn = driver.find_element("xpath","//*[@data-tid='toggle-mute']")
    audio_is_on = audio_btn.get_attribute("aria-checked")
    print(audio_btn, type(audio_btn))
    if audio_is_on == "true":
        print('DEBUG: Audio Turned Off')
        audio_btn.click()

    time.sleep(10)

    # /html/body/div[1]/div/div/div/div[4]/div/div/div/div/div[1]/div/div[2]/span/input
    #//*[@id="app"]/div/div/div/div[4]/div/div/div/div/div[1]/div/div[2]/span/input
    # Click on the "Join now" button
    join_now_button=driver.find_element("xpath","//*[@data-tid='prejoin-join-button']")
    join_now_button.click()
    print("joined meeting ", guest_name)

    #
    # # Wait for the meeting to start
    time.sleep(MEETING_JOIN_TIME_IN_MINS*60)
    print("Left meeting ", guest_name, "time after", MEETING_JOIN_TIME_IN_MINS*60)

    # Close the browser after joining the meeting (you may want to handle this differently based on your needs)
    # driver.quit()
def join_teams_meeting_wrapper(tuplea):
    try:
        join_teams_meeting(tuplea)
    except Exception as err:
        traceback.print_exc()

def main_process(tabs):
    links = []
    print("tabs", tabs)
    fake = Faker('en_IN')
    fake.seed_instance(random.randint(1, 99999))
    for i in range(int(tabs)):
        links.append([meeting_url, fake.name()])
    print("links", links)
    with futures.ThreadPoolExecutor(max_workers=int(tabs)) as executor: # default/optimized number of processes
        print("starting threads")
        executor.map(join_teams_meeting_wrapper, links)

# /html/body/div[1]/div/div/div/div[4]/div/div/div/div/div[1]/div/div[2]/span/input
if __name__ == '__main__':
    processes = input('Process count')
    threads = input('Thread count')

    # Example usage
    guest_name = "Your Guest Name"
    guests = ["ABC", "DEF", "SASD"]
    links = []
    for i in range(int(processes)):
        links.append(threads)
    with futures.ProcessPoolExecutor() as executor: # default/optimized number of processes
        print("1:looping")
        executor.map(main_process, links)
    # for x in range(10):
    #     join_teams_meeting([meeting_url, fake.name()])
    # join_teams_meeting([meeting_url, fake.name()])
    #setup on ubuntu - https://tecadmin.net/setup-selenium-with-python-on-ubuntu-debian/

    # import multiprocessing
    # pool = multiprocessing.Pool()
    # pool = multiprocessing.Pool(processes=4)
    # pool.map(join_teams_meeting, links)
    # outputs = pool.map(join_teams_meeting, links)
    # print("Output: {}".format(outputs))
    # https://docs.digitalocean.com/developer-center/install-ubuntu-desktop-on-a-droplet/

    # nohup ./hello.sh > myoutput.txt >2&1
