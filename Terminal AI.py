import requests
import uuid
import re
import logging
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import atexit
import webbrowser
import shlex
import os
import platform
from tkinter import messagebox
import subprocess
from tqdm import tqdm
import sys
import glob
import shutil
import base64
import os
import urllib.request
import subprocess
import getpass
import datetime

system = platform.system()

if system == 'Darwin':  # macOS
    folder_path = os.path.expanduser('~/Library/Application Support/TerminalAI')
elif system == 'Windows':
    folder_path = os.path.expanduser('~\AppData\Roaming\TerminalAI')
elif system == 'Linux':
    folder_path = os.path.expanduser('~/.config/TerminalAI')
else:
    raise Exception('Unsupported platform')

log_folder = 'logs'
if not os.path.exists(os.path.join(folder_path, log_folder)):
    os.mkdir(os.path.join(folder_path, log_folder))

# Meathod 1 to delete files (Not quite working)

log_file_path = os.path.join(log_folder, '*.log')
log_files = glob.glob(log_file_path)

if len(log_files) > 15:
    for file in log_files:
        os.remove(file)

# Meathod 2 to delete files

logs_folder2 = os.path.join(folder_path, log_folder)

try:
    # Get a list of files in the folder
    files = os.listdir(logs_folder2)

    # If there are more than 15 files, delete the excess files
    if len(files) > 15:
        # Sort the files by their modification time (oldest first)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(logs_folder2, x)))

        # Calculate the number of files to delete
        num_files_to_delete = len(files)

        # Delete the excess files starting from the oldest
        for i in range(num_files_to_delete):
            file_name = files[i]
            file_path = os.path.join(logs_folder2, file_name)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")
except Exception as e:
    print(f"Error counting files in folder {logs_folder2}: {e}")

logger = logging.getLogger('TerminalAi')
logger.setLevel(logging.DEBUG)

log_file = 'log.log'
log_file_path = os.path.join(folder_path, log_folder, log_file)

# Update the log file path to include a timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = f"log_{timestamp}.log"
log_file_path = os.path.join(folder_path, log_folder, log_file)

file_handler = logging.FileHandler(os.path.join(folder_path, log_folder, log_file))  # Update the file path here

# Configure the log formatter and add the handler to the logger
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_format)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Set the log level for the file handler
file_handler.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter to the file handler
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)



logo = """
                                       
   _____                   _             _      _    _  
  |_   _|__ _ __ _ __ ___ (_)_ __   __ _| |    / \  (_) 
    | |/ _ \ '__| '_ ` _ \| | '_ \ / _` | |   / _ \ | |
    | |  __/ |  | | | | | | | | | | (_| | |  / ___ \| |
    |_|\___|_|  |_| |_| |_|_|_| |_|\__,_|_| /_/   \_\_|
                  A Ai in the Terminal                                                      

"""

logger.info(logo)

if len(sys.argv) > 1:
    logger.debug('TerminalAi Started in system mode (means you cannot send messages to the ai you can only change settings)')

print(logo)
print("By using Terminal AI you agree to share your conversations with model authors.")
print("Note: Terminal Ai Requires firefox to be installed on your system.")

firefox_installed = False


os_name = platform.system()

# Set the command to check if Firefox is installed based on the operating system
if os_name == 'Windows':
    cmd = ['where', 'firefox']
elif os_name == 'Darwin':
    cmd = ['mdfind', 'kMDItemFSName=Firefox.app']
else:
    cmd = ['firefox', '--version']

# Run the command to check if Firefox is installed
cmd = " ".join(cmd)
cmd = shlex.split(cmd)
result = subprocess.run(cmd, stdout=subprocess.PIPE)

# If the command succeeded and returned a path, Firefox is installed
if result.returncode == 0 and result.stdout:
    firefox_installed = True
    logger.debug('Firefox is installed')
else:
    firefox_installed = False
    logger.debug('Firefox is not installed')

# If Firefox is not installed, prompt the user to install it
if not firefox_installed:
    install_firefox = input("Firefox is not installed. Would you like to install it? (y/n) ")
    if install_firefox.lower() == 'y':
        install_firefox()

agree_var = None

class Exception(Exception):
    print("See full log here: " + log_file_path)


conversationid = "64eead065e6c0746c0138735"

def change_conversation(new_id):
    conversationid = new_id

def init():
    change_conversation(conversationid)

def create_folder():
    global folder_path
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        logger.debug('TerminalAi Started on MacOS')
        folder_path = os.path.expanduser('~/Library/Application Support/TerminalAI')
    elif system == 'Windows':
        logger.debug('TerminalAi Started on Windows')
        folder_path = os.path.expanduser('~\AppData\Roaming\TerminalAI')
    elif system == 'Linux':
        logger.debug('TerminalAi Started on Linux')
        folder_path = os.path.expanduser('~/.config/TerminalAI')
    else:
        logger.error('The platform your using is not supported.')
        raise Exception('Unsupported platform')
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logger.debug('Folder path created at ' + folder_path)
    

    modify_file(folder_path=folder_path)
  
terms_of_condition = """

The Conversation will be shared with model authors to help improve it
The owner of TerminalAi is not responsible for any things the Ai said

Terminal Ai uses a HuggingChat for the AI

Please also read the terms of condition for huggingchat.



"""
  
import tkinter as tk
from tkinter import scrolledtext, ttk

def show_terms():
    global agree_var
    terms_popup = tk.Toplevel()
    terms_popup.title("Terms of Condition")

    title_label = tk.Label(terms_popup, text="By continuing you agree to the following:")
    title_label.pack(pady=10)

    separator = ttk.Separator(terms_popup, orient="horizontal")
    separator.pack(fill="x")

    terms_text = scrolledtext.ScrolledText(terms_popup, width=50, height=10)
    terms_text.insert(tk.INSERT, terms_of_condition)
    terms_text.config(state=tk.DISABLED)
    terms_text.pack()

    def agree():
        global agree_var
        agree_var = True
        terms_popup.destroy()
        logger.debug('Destoryed Terms of Condition popup')

    def disagree():
        global agree_var
        agree_var = False
        terms_popup.destroy()
        logger.debug('Destoryed Terms of Condition popup')

    agree_button = tk.Button(terms_popup, text="I Agree", command=agree)
    agree_button.pack(side="left", padx=10, pady=10)

    disagree_button = tk.Button(terms_popup, text="I Disagree", command=disagree)
    disagree_button.pack(side="right", padx=10, pady=10)

    logger.debug('Terms of Condition popup opened')

    terms_popup.grab_set() # disable other windows

    terms_popup.wait_window(terms_popup) # wait for the window to be closed

def get_cookies_from_file(on_error):
  if settings['allow_cookie_storage'] == True:
    cookie_file = os.path.join(folder_path, 'cookies.json')
    with open(cookie_file) as f:
        settings = json.load(f)
        try:
            return settings['hf_chat'], settings['token']
        except:
            return on_error
  else:
    print("To use cookie storage please turn it on from more settings in gui type system open_gui to open gui")
    return on_error

def modify_cookie_file(folder_path, token_cookie, hf_chat_cookie):
 with open(settings_file) as f:
    settings = json.load(f)

 if settings['allow_cookie_storage'] == True:
    global cookie_file
    cookie_file = os.path.join(folder_path, 'cookies.json')

    if not os.path.exists(cookie_file):
        settings = {
            "hf_chat": hf_chat_cookie ,
            "token": token_cookie,
        }

        json_string = json.dumps(settings)
        with open(settings_file, 'w') as f:
            f.write(json_string)

    else:
        with open(cookie_file) as f:
            settings = json.load(f)

            settings['token'] = token_cookie
            settings['hf_chat'] = hf_chat_cookie

            json_string = json.dumps(settings)
            with open(settings_file, 'w') as f:
                f.write(json_string)


def modify_file(folder_path):
    global settings_file
    settings_file = os.path.join(folder_path, 'settings.json')
    if not os.path.exists(settings_file):
        settings = {
            "agree": False ,
            "lan": "en",
            "allow_cookie_storage": False,
        }
        confirm = messagebox.askyesno("Cookie Storage", "Do you want to allow cookie storage? This will make sign in more faster")
        if confirm == True:
            settings['allow_cookie_storage'] = True
            f.write(json_string)
        json_string = json.dumps(settings)
        with open(settings_file, 'w') as f:
            f.write(json_string)
        show_terms()
        if agree_var == True:
            settings['agree'] = True
            json_string = json.dumps(settings)
            with open(settings_file, 'w') as f:
                logger.debug('Writing settings.json')
                f.write(json_string)
        else:
            logger.error('User did not agree to the terms of condition')
            raise Exception('User did not agree to the terms of condition')
    else:
        with open(settings_file) as f:
            settings = json.load(f)
        agree = settings.get('agree', "Invalid Json File")
        if agree == "Invalid Json File":
            raise Exception('Invalid Json File')
        elif agree == False:
            show_terms()
            if agree_var == True:
                settings['agree'] = True
                json_string = json.dumps(settings)
                with open(settings_file, 'w') as f:
                    f.write(json_string)
            else:
                logger.error('User did not agree to the terms of condition')
                raise Exception('User did not agree to the terms of condition')
        elif agree == True:
            pass


create_folder()

#root = tk.Tk()
#root.geometry("300x200")

#button = tk.Button(root, text="Show Terms of Condition", command=show_terms)
#button.pack(pady=50)

#root.mainloop()



init()

webdrivers = []

def quit_webdrivers():
    for driver in webdrivers:
        driver.quit()

# Register the function to be called on program exit
atexit.register(quit_webdrivers)
logger.debug('Registered quit_webdrivers')

class ConnectionError(Exception):
    pass

#Login
    
def login_firefox(username, password):
    url = "https://huggingface.co/login"

    # Configure Firefox WebDriver options
    global firefox_options
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('-headless')  # Run Firefox in headless mode (no visible browser window)

    # Create a new instance of the Firefox WebDriver
    global driver
    driver = webdriver.Firefox(options=firefox_options)
    webdrivers.append(driver)  # Add the driver to the list
    logger.debug('Created webdrivers')

    try:
        # Open the URL
        driver.get(url)

        # Enter login credentials and submit the form
        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")
        username_input.send_keys(username)
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        time.sleep(1)

        driver.get("https://huggingface.co/chat/")

        time.sleep(1)
          # Wait for the page to load
          

        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        driver.execute_script("arguments[0].scrollIntoView();", login_button)
        action = ActionChains(driver)
        driver.execute_script("arguments[0].click();", login_button)

        time.sleep(1)
        driver.save_screenshot("screenshot.png")

        wait = WebDriverWait(driver, 5)

        login_button = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "button")))
        # Iterate through the buttons and click the one with the desired text
        for button in login_button:
            if "Sign in with" in button.text:
                actions = ActionChains(driver)
                actions.click(button).perform()
                break  # Stop iterating after clicking the button

        time.sleep(1)

        hf_chat_cookie = driver.get_cookie("hf-chat")
        token_cookie = driver.get_cookie("token")
        __stripe_mid_cookie = driver.get_cookie("__stripe_mid")
        __stripe_sid_cookie = driver.get_cookie("__stripe_sid")
        logger.debug('Getting Cookies')
        if hf_chat_cookie:
            global hf_chat
            hf_chat = hf_chat_cookie['value']
        else:
            raise Exception("No hf-chat cookie found!")
        if token_cookie:
            global token
            token = token_cookie['value']
        else:
            raise Exception("No token cookie found!")

        # Check if login was successful by checking the URL after logging in
        if "huggingface.co/chat/login" in driver.current_url:
            raise ConnectionError("Wrong username or password")

    except Exception as e:
        driver.quit()  # Quit the driver in case of an exception
        raise e
    
def test_connection():
    cookie = {
       # "__stripe_mid": __stripe_mid,  # Replace with your actual cookie values
        #"__stripe_sid": __stripe_sid,  # Replace with your actual cookie values"
        "hf-chat": hf_chat,  # Replace with your actual cookie values
        "token": token,
}   
    response = None
    response = requests.get('https://huggingface.co/chat/', cookies=cookie, allow_redirects=True)
    if not response == None:
        if response.status_code == 500 or response.status_code == 404 or response.status_code == 403 or response.status_code == 401:
            return False
        elif response.status_code == 200:
            return True

import shlex

def install_firefox():
    # URLs of the Firefox installer executable files for each operating system
    firefox_urls = {
        'Windows': 'https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US',
        'Darwin': 'https://download.mozilla.org/?product=firefox-latest&os=osx&lang=en-US',
        'Linux': 'https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US'
    }

    # File name of the Firefox installer executable file for each operating system
    firefox_filenames = {
        'Windows': 'Firefox Setup 117.0.exe',
        'Darwin': 'Firefox 117.0.dmg',
        'Linux': 'firefox-117.0.tar.bz2'
    }

    # Temporary directory to save the installer file
    temp_dir = os.path.join(os.environ['TEMP'], 'firefox_installer')

    # Create the temporary directory if it does not exist
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Get the URL and file name of the Firefox installer executable file for the current operating system
    os_name = platform.system()
    firefox_url = firefox_urls.get(os_name)
    firefox_filename = firefox_filenames.get(os_name)
    if firefox_url is None or firefox_filename is None:
        print(f"Firefox is not supported on {os_name}.")
        logger.error(f"Firefox is not supported on {os_name} and cannot be installed.")
        raise Exception(f"Firefox is not supported on {os_name} and cannot be installed.")
    else:
        # Download the Firefox installer executable file
        installer_file = os.path.join(temp_dir, firefox_filename)
        logger.debug('Downloading Firefox installer file')
        urllib.request.urlretrieve(firefox_url, installer_file)

        # Run the installer executable silently
        install_command = [installer_file, '/S']
        if os.getuid() == 0:
            # If running as root, no need to prompt for admin username and password
            logger.debug('Installing Firefox')
            install_command = shlex.split(install_command)
            subprocess.run(install_command, check=True, shell=False)
        else:
            # If not running as root, prompt for admin username and password if needed
            try:
                install_command = shlex.split(install_command)
                subprocess.run(install_command, check=True, shell=False)
            except subprocess.CalledProcessError:
                logger.debug('Prompting for admin username and password')
                admin_username = input("Enter admin username: ")
                admin_password = getpass.getpass(prompt='Enter admin password: ')
                if os_name == 'Windows':
                    show_progress()
                    logger.debug('Attempting to install firefox with runas')
                    subprocess.run(['runas', '/user:' + admin_username, installer_file, '/S'], input=admin_password.encode(), check=True)
                else:
                    # On macOS and Linux, use the `sudo` command to run the installer executable with admin privileges
                    sudo_command = ['sudo', '-S', installer_file]
                    show_progress()
                    logger.debug('Attempting to install firefox with sudo')
                    subprocess.run(sudo_command, input=admin_password.encode(), check=True)
        cleanup()

def cleanup():
    # Temporary directory to save the installer file
    temp_dir = os.path.join(os.environ['TEMP'], 'firefox_installer')

    # Delete the temporary directory and its contents
    if os.path.exists(temp_dir):
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
                logger.error(f"Failed to delete {file_path}. Reason: {e}")
        os.rmdir(temp_dir)

def show_progress():
    # Create a new window
    window = tk.Toplevel()
    window.title("Progress")

    # Create a progress bar widget
    progress = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=20)

    # Estimate the time remaining based on the time elapsed
    start_time = time.time()
    total_time = 60  # Estimated total time in seconds
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= total_time:
            break
        progress['value'] = elapsed_time / total_time * 100
        window.update_idletasks()

    # Close the window
    window.destroy()
    

def Login(username, password):
    login_firefox(username, password)
    #login(username, password)
    #location2 = getAuthURL()
    #location = getAuthURL_firefox()
    #if grantAuth_firefox(location2):
    #    cookies = requests.sessions.RequestsCookieJar()
    #    cookies.update(requests.Session().cookies)
    #    return cookies
    #else:
    #    raise Exception(f"Grant auth fatal, please check your email or password\ncookies gained:")

if len(sys.argv) > 1:
    n = sys.argv[1]
else:
    username_input = input("Enter your username to sign in to huggingface: ")
    password_input = input("Enter your password to sign in to huggingface: ")
    if get_cookies_from_file(on_error="Fail") == "Fail":
        print("Attempting to login... This may take a few miniutes")
        logger.debug('Attempting to login via firefox using webdrivers')
        cookies = Login("enter default username", "enter default password")
        print("Login Successful!")
    else:
        cookies_from_file = get_cookies_from_file(on_error="Fail")
        token = cookies_from_file.get("token")
        hf_chat = cookies_from_file.get("hf-chat")
        if test_connection() == False:
            print("Attempting to login... This may take a few miniutes")
            logger.debug('Attempting to login via firefox using webdrivers')
            if not username_input is None or not username_input == '' or not password_input is None or not password_input == '':
                cookies = Login(username_input, password_input)
            print("Login Successful!")

def change_account():
    print("Attempting to login... This may take a few miniutes")
    quit_webdrivers()
    cookies = Login(new_username, new_password)
    print("Login Successful!")


#Chat

def chat(
        self,
        text: str,
        # web_search: bool=False,
        temperature: float=0.9,
        top_p: float=0.95,
        repetition_penalty: float=1.2,
        top_k: int=50,
        truncate: int=1024,
        watermark: bool=False,
        max_new_tokens: int=1024,
        stop: list=["</s>"],
        return_full_text: bool=False,
        stream: bool=True,
        use_cache: bool=False,
        is_retry: bool=False,
        retry_count: int=5,
        conversationid: str=conversationid,
        print: bool=True,
):

    req_json = {
            "inputs": text,
            "parameters": {
                "temperature": temperature,
                "top_p": top_p,
                "repetition_penalty": repetition_penalty,
                "top_k": top_k,
                "truncate": truncate,
                "watermark": watermark,
                "max_new_tokens": max_new_tokens,
                "stop": stop,
                "return_full_text": return_full_text,
                "stream": stream,
            },
            "options": {
                    "use_cache": use_cache,
                    "is_retry": is_retry,
                    "id": str(uuid.uuid4()),
            },
            "stream": True,
        }

    url = f"https://huggingface.co/chat/conversation/{conversationid}"

    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Host": "huggingface.co",
        "Origin": "https://huggingface.co",  # Set the Origin header
        "Referer": f"https://huggingface.co/chat/conversation/{conversationid}",
        "Sec-Fetch-Site": "same-origin",
        "Content-Type": "application/json",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Ch-Ua": "Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Microsoft Edge\";v=\"116",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }

# Adding a cookie to the request
    cookie = {
       # "__stripe_mid": __stripe_mid,  # Replace with your actual cookie values
        #"__stripe_sid": __stripe_sid,  # Replace with your actual cookie values"
        "hf-chat": hf_chat,  # Replace with your actual cookie values
        "token": token,
}

    response = None
    response = requests.post(url, json=req_json, cookies=cookie, headers=headers, timeout=10)
    if not response == None:
        if response.status_code == 500 or response.status_code == 404:
            raise ConnectionError(f"Error: Conversation " + conversationid + " does not exist")
    else:
        print("Request 10 Seconds Timeout")

    extracted_texts = extract(response)
    if print:
        print(extracted_texts)  # You can print the response content to see the result
    else:
        return extracted_texts


def extract(req_response):
    response = req_response.text

    # split the response into individual JSON objects
    json_objects = response.split("\n")

    # extract the generated_text field from each JSON object
    generated_texts = []
    for line in req_response.iter_lines():
        if line:
            res = line.decode("utf-8")
            try:
                obj = json.loads(res[5:])
                if "generated_text" in obj and obj["generated_text"] is not None:
                    generated_texts.append(obj["generated_text"])
            except json.JSONDecodeError:
                pass

    # filter out null values
    generated_texts = [text for text in generated_texts if text is not None]

    if generated_texts:
        return generated_texts[0]
    else:
        return None

def change_llm(to, conversationid=conversationid):
    # Change Model
    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Host": "huggingface.co",
        "Origin": "https://huggingface.co",  # Set the Origin header
        "Referer": f"https://huggingface.co/chat/conversation/{conversationid}",
        "Sec-Fetch-Site": "same-origin",
        "Content-Type": "application/json",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Ch-Ua": "Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Microsoft Edge\";v=\"116",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    cookies = {
        #"__stripe_mid": __stripe_mid,  # Replace with your actual cookie values
        #"__stripe_sid": __stripe_sid,  # Replace with your actual cookie values"
        "hf-chat": hf_chat,  # Replace with your actual cookie values
        "token": token,
}
    llms = ['OpenAssistant/oasst-sft-6-llama-30b-xor', 'meta-llama/Llama-2-70b-chat-hf']
    mdl = ""
    if to == 0:
        mdl = "OpenAssistant/oasst-sft-6-llama-30b-xor",
    elif to == 1:
        mdl = "meta-llama/Llama-2-70b-chat-hf"
    else:
        raise BaseException("Can't switch llm, unexpected index. For now, 0 is `OpenAssistant/oasst-sft-6-llama-30b-xor`, 1 is `meta-llama/Llama-2-70b-chat-hf` :)")
    response = requests.post("https://huggingface.co/chat/settings", headers=headers, cookies=cookies, allow_redirects=True, data={
        "shareConversationsWithModelAuthors": "on",
        "ethicsModalAcceptedAt": "",
        "searchEnabled": "true",
        "activeModel": mdl,
        })
    
def new_conversation_requests():
        _header = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Host": "huggingface.co",
        "Origin": "https://huggingface.co",  # Set the Origin header
        "Referer": f"https://huggingface.co/chat",
        "Sec-Fetch-Site": "same-origin",
        "Content-Type": "application/json",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Ch-Ua": "Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Microsoft Edge\";v=\"116",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
        _cookies = {
        #"__stripe_mid": __stripe_mid,  # Replace with your actual cookie values
        #"__stripe_sid": __stripe_sid,  # Replace with your actual cookie values"
        "hf-chat": hf_chat,  # Replace with your actual cookie values
        "token": token,
}

        resp = ""
        while True:
            try:
                resp = requests.post("https://huggingface.co/chat/conversation", json={"model": "OpenAssistant/oasst-sft-6-llama-30b"}, headers=_header, cookies =_cookies)
                # print("new conversation")
                # print(resp.text)
                logging.debug(resp.text)
                cid = json.loads(resp.text)['conversationId']
                __preserve_context(cid = cid, ending = "1_1")
                return cid
            except:
                pass
            
def __preserve_context(cid: str = None, ending: str = "1_", ref_cid: str = ""):
        # print("preserve_context")
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
            'Accept': "*/*",
        }
        if ref_cid == "":
            headers["Referer"] = "https://huggingface.co/chat"
        else:
            headers["Referer"] = f"https://huggingface.co/chat/conversation/{ref_cid}"
        # print(headers)
        cookie = {
            'hf-chat': hf_chat,
        }
        if cid is None:
            cid = conversationid
        url = f"https://huggingface.co/chat/conversation/{cid}/__data.json?x-sveltekit-invalidated={ending}"
        # response = requests.get(url, cookies = cookie, headers = headers )
        response = requests.get(url, cookies = cookie, headers = headers, data = {})
        # print(response.text)
        import time
        
        # f = open(f"test{str(time.time())}.json", "w", encoding="utf-8")
        # f.write(json.dumps(response.json(), indent=4, ensure_ascii=False))
        # f.close()
        
        if response.status_code == 200:
            # print("OK")
            return {'message': "Context Successfully Preserved", "status":200}
        else:
            return {'message': "Internal Error", "status": 500}
    
def new_conversation():
    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Host": "huggingface.co",
        "Origin": "https://huggingface.co",  # Set the Origin header
        "Referer": f"https://huggingface.co/chat",
        "Sec-Fetch-Site": "same-origin",
        "Content-Type": "application/json",
        "Sec-Ch-Ua-Platform": "Windows",
        "Sec-Ch-Ua": "Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Microsoft Edge\";v=\"116",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    cookies = {
        #"__stripe_mid": __stripe_mid,  # Replace with your actual cookie values
        #"__stripe_sid": __stripe_sid,  # Replace with your actual cookie values"
        "hf-chat": hf_chat,  # Replace with your actual cookie values
        "token": token,
}
    wait = WebDriverWait(driver, 5)
    login_button = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
    # Iterate through the buttons and click the one with the desired text
    for button in login_button:
        if "New Chat" in button.text:
            print("New Chat")
            actions = ActionChains(driver)
            actions.click(button).perform()
            placeholder_value = "Ask anything"
            button_elements = driver.find_elements(By.TAG_NAME, "textarea")
            button_text_list = [button.text for button in button_elements]

            # Print the list of button texts
            for button in button_elements:
                button_text = button.text.strip()  # Strip any leading/trailing whitespace
                if button_text:
                    print(button.text)
                    button.send_keys("")
                    button.send_keys(Keys.RETURN)

            url = driver.current_url
            match = re.search(r'/(\w+)$', url)

            if match:
                conversation_id = match.group(1)
                new_conversationid = conversation_id
                change_conversation(new_conversationid)
            else:
                raise Exception("Could not find conversation ID")

            change_llm(0, conversation_id)
            break  # Stop iterating after clicking the button

    #resp = requests.post("https://huggingface.co/chat/conversation", json={"model": "OpenAssistant/oasst-sft-6-llama-30b"}, headers=headers, cookies=cookies)
    #print(resp.text)

def uninstall(in_test=False, root=None):
  logger.debug('Uninstall function has been called and in_test is ' + str(in_test))
  if in_test != True:
      print("Not in in_test")
  if root != None or '':
    root.withdraw()

  confirm = messagebox.askyesno("Uninstall All Data", "Are you sure you want to uninstall all data?")
  logger.debug('Uninstall comfirmation has been created')
  if confirm:

    # Create a progress bar window
    progress_window = tk.Toplevel()
    progress_window.title("Uninstall Progress")
    progress_label = tk.Label(progress_window, text="Uninstall Progress:")
    progress_label.pack(padx=20, pady=10)
    progress_bar = ttk.Progressbar(progress_window, length=200, mode='determinate')
    progress_bar.pack(padx=20, pady=20)

    # Set the maximum value of the progress bar
    progress_bar["maximum"] = 100

    file_path = folder_path + "/settings.json"

    if in_test != True:
    # Remove the file
        os.remove(file_path)        

    # Check if the path starts with a slash, and if so, remove it
        if folder_path.startswith('/'):
         remove_folder_path = folder_path[1:]

    # Check if the path ends with a slash, and if so, remove it
        if folder_path.endswith('/'):
            remove_folder_path = folder_path[:-1]

    # Define the path of the directory you want to remove
        directory_path = os.path.abspath(remove_folder_path)

    # Remove the directory "foo" and all of its contents
        shutil.rmtree(directory_path)


    # Update the progress bar smoothly
    for i in tqdm(range(100), desc="Uninstalling", leave=False):
        progress_bar["value"] = i
        progress_window.update()
        time.sleep(0.07)

    # Close the progress window
    progress_window.destroy()

    logger.debug('Delete python file comfirmation has been created')
    confirm = messagebox.askyesno("Uninstall All Data", "Do you want to delete this python file?")
    if confirm:
        script_path = os.path.abspath(__file__)
        logger.debug('Deleting python file.')

        if in_test != True:
            # Remove the script file
            os.remove(script_path)

    # Display a message when the uninstall is complete
    messagebox.showinfo("Uninstall", "Uninstall complete.")
    root.deiconify()  # Show the main window again
  else:
      try:
        progress_window.destroy()
        logger.debug('Destroyed comfirmation window')
      except UnboundLocalError:
        pass
      
sidebar = None
sidebar_visible = None
      
import tkinter as tk
from tkinter import simpledialog
from tkinter import scrolledtext
from ttkthemes import ThemedStyle
      
def send_message():
    message = user_input.get()
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f"You: {message}\n")
    chat_area.config(state=tk.DISABLED)
    
    # Simulate AI response (replace this with your actual AI interaction)
    ai_response = f"AI: Hello, you said '{message}'."
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, ai_response + "\n")
    chat_area.config(state=tk.DISABLED)
    
    user_input.delete(0, tk.END)

def toggle_sidebar():
    global sidebar
    if sidebar_visible.get():
        sidebar.pack_forget()
    else:
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
    sidebar_visible.set(not sidebar_visible.get())

def open_gui():
    gui = tk.Tk()
    gui.title("AI GUI")
    
    # Configure theme style for modern appearance
    style = ThemedStyle(gui)
    style.set_theme("arc")
    
    # Sidebar for conversations
    global sidebar, sidebar_visible
    sidebar_visible = tk.BooleanVar()
    sidebar_visible.set(True)
    
    sidebar = tk.PanedWindow(gui, orient=tk.VERTICAL)
    sidebar_button = tk.Button(sidebar, text="Toggle Sidebar", command=toggle_sidebar)
    sidebar.add(sidebar_button)
    
    # Chat display area
    global chat_area
    chat_area = scrolledtext.ScrolledText(gui, state=tk.DISABLED, wrap=tk.WORD, height=15, width=50)
    chat_area.pack(padx=20, pady=20)
    
    # User input field
    global user_input
    user_input = tk.Entry(gui, width=40)
    user_input.pack(padx=20, pady=5)
    
    # Send button
    send_button = tk.Button(gui, text="Send", command=send_message)
    send_button.pack(padx=20, pady=10)
    
    sidebar.pack(side=tk.LEFT, fill=tk.Y)  # Initialize sidebar
    
    gui.mainloop()

def get_settings_data(data, on_error="Error!"):
    logger.debug('Get settings data: ' + str(data))
    #allow_cookie_storage
    with open(settings_file) as f:
        settings = json.load(f)

    data_to_return = settings.get(data, on_error)
    return data_to_return

def set_settings_data(data, value):
    logger.debug('Set settings data: ' + str(data))
    with open(settings_file) as f:
        settings = json.load(f)

    settings[data] = value
    json_string = json.dumps(settings)
    with open(settings_file, 'w') as f:
        f.write(json_string)

def open_gui_class():
 logger.debug('Opening GUI class')
 from PIL import Image, ImageTk
 #import cairosvg
 from tkinter import PhotoImage
 #from PIL.SvgImagePlugin import PyImagePlugin

 class AIChatGUI:
    def __init__(self, root):
        logger.debug('Attempting to create AI chat GUI')
        self.root = root
        self.root.title("AI Chat GUI")
        self.root.geometry("1000x850")  # Larger window size
        
        self.style = ThemedStyle(self.root)
        #self.style = ThemedStyle("breeze")
        #self.style.set_theme("equilux")
        self.style.set_theme("equilux")

        try:
            self.background_image = tk.PhotoImage(file="background.png")  # Replace with your background image
        except:
            self.background_image = tk.PhotoImage(file=os.path.expanduser("~/Documents/TerminalAi/background.png"))
        
        
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)
        
        self.sidebar = tk.Frame(self.root, bg="gray", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.sidebar_label = tk.Label(self.sidebar, text="Options:", bg="gray")
        self.sidebar_label.pack(pady=5)
        
        self.new_chat_button = tk.Button(self.sidebar, text="New Chat", command=self.start_new_chat)
        self.new_chat_button.pack()

        self.change_conversation_button = tk.Button(self.sidebar, text="Change Conversation", command=self.change_conversation)
        self.change_conversation_button.pack()

        self.user_change_button = tk.Button(self.sidebar, text="Change User", command=self.switch_users)
        self.user_change_button.pack()

        self.close_gui_button = tk.Button(self.sidebar, text="Close GUI", command=self.close_gui)
        self.close_gui_button.pack()

        self.quit_button = tk.Button(self.sidebar, text="Quit", command=self.quit_whole_thing)
        self.quit_button.pack()

        self.uninstall_button = tk.Button(self.sidebar, text="Uninstall TerminalAI", command=self.uninstall_button_press)
        self.uninstall_button.pack()

        self.uninstall_test_button = tk.Button(self.sidebar, text="Uninstall TerminalAI (Test)", command=self.uninstall_test_button_press)
        self.uninstall_test_button.pack()

        self.more_settingsbutton = tk.Button(self.sidebar, text="More Settings", command=self.more_settings)
        self.more_settingsbutton.pack()
        
        self.chat_area = scrolledtext.ScrolledText(self.root, state=tk.DISABLED, wrap=tk.WORD)
        self.chat_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=20)  # Place at the top
        
        self.text_entry = tk.Entry(self.root)
        self.text_entry.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)  # Place at the bottom

        import io

        svg_data = """
        <?xml version="1.0" standalone="no"?>
        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
         "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
        <svg version="1.0" xmlns="http://www.w3.org/2000/svg"
         width="512.000000pt" height="512.000000pt" viewBox="0 0 512.000000 512.000000"
         preserveAspectRatio="xMidYMid meet">
        <metadata>
        Created by potrace 1.16, written by Peter Selinger 2001-2019
        </metadata>
        <g transform="translate(0.000000,512.000000) scale(0.100000,-0.100000)"
         fill="#000000" stroke="none">
        <path d="M0 3902 l0 -859 33 -5 c17 -3 823 -111 1789 -239 967 -129 1758 -236
        1758 -239 0 -3 -804 -112 -1787 -243 -983 -131 -1789 -239 -1790 -241 -2 -2
        -2 -388 -1 -859 l3 -856 2558 1096 c1406 603 2557 1099 2557 1103 0 4 -1149
        498 -2552 1100 -1404 601 -2556 1095 -2560 1097 -5 2 -8 -382 -8 -855z"/>
        </g>
        </svg>
        """

        # Convert the SVG data to PNG using cairosvg
        #self.image.save(os.path.join(folder_path, "background.png"))
        #image_data = base64.b64decode(base64_send)
        try:
            send_button_image = Image.open("send-button.png")
        except:
            send_button_image = None
        finally:
            if send_button_image is None:
                send_button_image.close()
                send_button_image = None

        if not send_button_image:
            send_button_image = Image.open(os.path.expanduser("~/Documents/TerminalAi/send-button.png"))
        #send_button_image = Image.open(io.BytesIO(Svg2.generate(svg_data).read()))
        #self.send_button = ImageTk.PhotoImage(image)
        #send_button_image = Image.open(Image.open(base64_send))  # Replace with your send button image
        send_button_image = send_button_image.resize((24, 24), Image.LANCZOS)  # Resize the image
        send_button_image = ImageTk.PhotoImage(send_button_image)

        def on_send_button_click(self):
            # Handle the send button click event
            print("Send button clicked")
        
        self.send_button = tk.Button(self.root, image=send_button_image, command=self.send_message, borderwidth=0)
        self.send_button.image = send_button_image
        self.send_button.pack(side=tk.RIGHT, padx=20, pady=10)
        
        self.guiai_label = tk.Label(self.root, text="TerminalAI Gui", bg="gray")
        self.guiai_label.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        self.chat_history = []
        
        self.load_chat_history()  # Load conversation history from file
        self.root.bind("<Return>", self.send_message)  # Bind Enter key to send message

    def quit_whole_thing(self):
        quit_webdrivers()
        sys.exit(0)

    def uninstall_button_press(self):
            root = tk.Tk()
            root.attributes('-topmost', False)

            # Call uninstall function here when needed
            uninstall(root=root)

            root.mainloop()  # Start the main event loop

    def uninstall_test_button_press(self):
            root = tk.Tk()
            root.attributes('-topmost', False)

            # Call uninstall function here when needed
            uninstall(in_test=True, root=root)

            root.mainloop()  # Start the main event loop

    def more_settings(self):
        root = tk.Tk()
        root.title("More Settings")
        #root.geometry("800x600")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

# Set the desired window size
        desired_width = 800
        desired_height = 600

        # Adjust the window size if necessary
        if screen_width < desired_width or screen_height < desired_height:
            root.geometry("%dx%d" % (screen_width, screen_height))
        else:
            root.geometry("%dx%d" % (desired_width, desired_height))

# Set the minimum size of the window
        root.minsize(400, 300)      

        def toggle():
            if var.get() == 1:
                canvas.itemconfig(switch, fill="#4CAF50")
                canvas.coords(slider, 35, 5, 55, 25)
                set_settings_data("allow_cookie_storage", True)
                var.set(0)
            else:
                canvas.itemconfig(switch, fill="#ccc")
                canvas.coords(slider, 5, 5, 25, 25)
                set_settings_data("allow_cookie_storage", False)
                var.set(1)

        def show_tooltip(event, text):
            global tooltip
            tooltip = tk.Toplevel(root)
            tooltip.geometry("+%d+%d" % (event.x_root, event.y_root))
            tooltip.overrideredirect(True)
            label = tk.Label(tooltip, text=text, bg="white", padx=5, pady=5)
            label.pack()

        def hide_tooltip(event):
            tooltip.destroy()


        var = tk.IntVar(value=1)

        switch_togle = get_settings_data("allow_cookie_storage", "Error")

        if switch_togle != "Error":
            if switch_togle == "True":
                var.set(1)
            else:
                var.set(0)
        else:
            var.set(1)
            set_settings_data("allow_cookie_storage", False)

        default_label = tk.Label(root, text="More Settings:", font=("Helvetica", 24))
        default_label.pack(padx=20, pady=10)

        cookies_storage_label = tk.Label(root, text="Allow Cookie Storage?")
        cookies_storage_label.bind("<Enter>", lambda event: show_tooltip(event, text="This will let the program save cookies to a file so next time it would be faster to login. (Note everytime you open this setting requires you to reset it)"))
        cookies_storage_label.bind("<Leave>", lambda event: hide_tooltip(event))
        cookies_storage_label.pack(padx=20, pady=10)

        canvas = tk.Canvas(root, width=60, height=30, highlightthickness=0)
        canvas.pack()

        switch = canvas.create_rectangle(0, 0, 60, 30, fill="#4CAF50", width=0)
        slider = canvas.create_rectangle(5, 5, 25, 25, fill="#fff", width=0)

        canvas.tag_bind(switch, "<Button-1>", lambda event: toggle())

        done_button = tk.Button(root, text="Done", command=root.destroy)
        done_button.pack(side="bottom", padx=20, pady=10)
        #button.grid(row=1, column=3)

        root.mainloop()

    def switch_users(self):
        root = tk.Tk()

        # create two Entry widgets
        label1 = tk.Label(root, text="Enter Username:")
        entry1 = tk.Entry(root)
        label2 = tk.Label(root, text="Enter Password:")
        entry2 = tk.Entry(root)

        # position the widgets on the window
        label1.grid(row=0, column=0)
        entry1.grid(row=0, column=1)
        label2.grid(row=1, column=0)
        entry2.grid(row=1, column=1)

        # get the input values when OK button is clicked
        def ok():
            global new_username
            new_username = entry1.get()
            global new_password
            new_password = entry2.get()
            change_account()
            root.destroy()
        def cancel():
            root.destroy()

        button = tk.Button(root, text="Done", command=ok)
        button.grid(row=1, column=3)

        button_cancel = tk.Button(root, text="Cancel", command=cancel)
        button_cancel.grid(row=0, column=3)

        root.mainloop()

    def change_conversation(self):
            new_id = simpledialog.askstring("New Conversation ID", "Enter new conversation ID:")
            if new_id is not None:
                self.conversation_id = new_id
                print("Conversation ID set to:", self.conversation_id)

    def close_gui(self):
            root.destroy()
            self.root.destroy()

    def send_message(self, event=None):
        message = self.text_entry.get()
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"You: {message}\n")
        self.chat_area.config(state=tk.DISABLED)
        
        # Simulate AI response (replace this with your actual AI interaction)
        #ai_response = f"AI: Hello, you said '{message}'."
        if not len(sys.argv) > 1:
            ai_response = "AI: " + chat(message, message, print=False)
        else:
            logger.debug("System: " + 'In system mode, only system commands work')
            ai_response = "System: " + "In system mode, only system commands work"
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, ai_response + "\n")
        self.chat_area.config(state=tk.DISABLED)
        
        self.chat_history.append((f"You: {message}", ai_response))
        self.text_entry.delete(0, tk.END)
        self.save_chat_history()  # Save conversation history to file
    
    def start_new_chat(self):
        logger.debug('Starting new conversation')
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.config(state=tk.DISABLED)
        self.chat_history = []
    
    def load_chat_history(self):
        try:
            with open(folder_path + "gui_chat_history.txt", "r") as file:
                self.chat_history = [tuple(line.strip().split(": ", 1)) for line in file.readlines()]
        except FileNotFoundError:
            self.chat_history = []
    
    def save_chat_history(self):
        logger.debug('Saving chat history')
        with open(folder_path + "gui_chat_history.txt", "w") as file:
            for chat_pair in self.chat_history:
                file.write(": ".join(chat_pair) + "\n")

 if __name__ == "__main__":
    root = tk.Tk()
    app = AIChatGUI(root)
    root.mainloop()


print("For a list of system commands type system help")

while True:
    prompt = input("Prompt: ")
    if not "system" in prompt:
        if not len(sys.argv) > 1:
            chat("Hello", prompt)
        else:
            print("In system mode, only system commands work")
    else:
        if "new_conversation" in prompt:
            new_conversation_requests()
        elif "change_conversation" in prompt:
            conversationid = prompt.split(" ")[2]
            change_conversation(conversationid)
            logger.debug('Conversation has been switched to ' + conversationid)
            print("Conversation has been switched to " + conversationid)
        elif "help" in prompt:
            help = """
            Note: All commands must start with system (example: system new_conversation)

            System commands:
            new_conversation - Starts a new conversation (Not working yet)
            change_conversation - Switches to a conversation (Not working yet)
            uninstall - Uninstalls Terminal AI (Not working yet)
            help - Prints this help message
            """
            print(help)
        elif "uninstall" in prompt and not "test" in prompt:
            root = tk.Tk()
            root.attributes('-topmost', False)

            # Call uninstall function here when needed
            uninstall(root=root)

            root.mainloop()  # Start the main event loop
        elif "uninstall test" in prompt:
            root = tk.Tk()
            root.attributes('-topmost', False)

            # Call uninstall function here when needed
            uninstall(root=root, in_test=True)

            root.mainloop()  # Start the main event loop
        elif "open_gui" in prompt:
            #open_gui()
            open_gui_class()

        else:
            print("Unknown system command")
