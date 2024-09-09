import json
import os
import sys
import zipfile
import time
import signal
from neurosity import NeurositySDK  

CONFIG_FILE = "config.json"


def load_config():
    """Load configuration from file"""
    if not os.path.isfile(CONFIG_FILE):
        print(os.getcwd())  
        print(f"Configuration file {CONFIG_FILE} not found!")
        sys.exit(1)

    with open(CONFIG_FILE, 'r') as config_file:
        return json.load(config_file)

def validate_config(config):
    """Validate the configuration variables"""
    email = config.get("email")
    password = config.get("password")
    device_id = config.get("device_id")

    if not email or not password or not device_id:
        print("Error: One or more configuration variables (email, password, device_id) are not set.")
        sys.exit(1)

    return email, password, device_id

def create_sdk_instance(device_id):
    """Create a NeurositySDK instance with the device ID"""
    return NeurositySDK({"device_id": device_id})

def login_to_neurosity(sdk, email, password):
    """Login to the Neurosity account using the provided email and password"""
    sdk.login({"email": email, "password": password})

# Data structures to store streamed data and counters
data_store = {
    "brainwaves": [],
    "calm": [],
    "focus": [],
    "power_by_band": [],
    "status": []
}

# Counters to track the number of data points added
data_counters = {
    "brainwaves": 0,
    "calm": 0,
    "focus": 0,
    "power_by_band": 0,
    "status": 0
}

# Subscription objects (initially set to None)
unsubscribe_brainwaves = None
unsubscribe_calm = None
unsubscribe_focus = None
unsubscribe_power_by_band = None
unsubscribe_status = None

# Function to create json file where to save the data

#def create_json_file(filename):
  #  with open(filename, "r+") as file:
  #      content = file.read()
  #      file.seek(0, 0)
  #      file.write("[" + content)
  #  with open(filename, "a") as file:
  #      file.write("]")


def save_data(filename, data):
    with open(filename, "a") as file:
        file.write(f"{json.dumps(data)}")

# Function to save and zip all data
def save_and_zip_data():
    print("Saving data to files...")  # Debug statement
    files_to_zip = []

    for data_type, data in data_store.items():
        if data:  # Only save non-empty data lists
            save_data(f"{data_type}.json", data)
            #create_json_file(f"{data_type}.json")
            files_to_zip.append(f"{data_type}.json")

    # Create a zip file containing all data files
    if files_to_zip:
        with zipfile.ZipFile("neurosity_data.zip", "w") as zipf:
            for file in files_to_zip:
                zipf.write(file)
                os.remove(file)  # Delete the file after adding it to the zip
        print("Data successfully saved to neurosity_data.zip")  # Debug statement
    else:
        print("No data to save.")  # Debug statement

# Callback functions
def data_callback(data_type, data):
    data_store[data_type].append(data)
    data_counters[data_type] += 1
    if data_counters[data_type] >= 100:
        save_data(f"{data_type}.json", data_store[data_type])
        data_store[data_type].clear()  # Clear the list after saving
        data_counters[data_type] = 0

# Function to start streaming
def start_streaming():

    global unsubscribe_brainwaves, unsubscribe_calm, unsubscribe_focus, unsubscribe_power_by_band, unsubscribe_status
    config = load_config()
    email, password, device_id = validate_config(config)
    sdk = create_sdk_instance(device_id)
    login_to_neurosity(sdk, email, password)

    try:
        unsubscribe_brainwaves = sdk.brainwaves_raw(lambda data: data_callback("brainwaves", data))
        unsubscribe_calm = sdk.calm(lambda data: data_callback("calm", data))
        unsubscribe_focus = sdk.focus(lambda data: data_callback("focus", data))
        unsubscribe_power_by_band = sdk.brainwaves_power_by_band(lambda data: data_callback("power_by_band", data))
        unsubscribe_status = sdk.status(lambda data: data_callback("status", data))
        print("Data streaming started.")
    except Exception as e:
        print(f"Error starting streaming: {e}")

# Function to stop streaming
def stop_streaming():
    try:
        if unsubscribe_brainwaves:
            unsubscribe_brainwaves()
        if unsubscribe_calm:
            unsubscribe_calm()
        if unsubscribe_focus:
            unsubscribe_focus()
        if unsubscribe_power_by_band:
            unsubscribe_power_by_band()
        if unsubscribe_status:
            unsubscribe_status()
        save_and_zip_data()  # Save any remaining data
        print("Data streaming stopped.")
    except Exception as e:
        print(f"Error stopping streaming: {e}")

# Define a safe exit handler to save and zip data
def exit_handler(signum, frame):
    stop_streaming()
    sys.exit(0)

# Set up signal handlers for graceful shutdown
signal.signal(signal.SIGINT, exit_handler)  # Handle Ctrl+C
signal.signal(signal.SIGTERM, exit_handler)  # Handle termination
