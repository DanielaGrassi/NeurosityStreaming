# Crown Recorder

Super simple app to collect data from Neurosity Crown device

## Prerequisites

- Python 3.x installed on your system
- pip installed (usually included with Python)

## Creating a Virtual Environment

1. Open the terminal.
2. Navigate to the project directory where `CrownRecorder.py` is located.
3. Create a virtual environment with the following command:

   ```sh
   python3 -m venv venv
   ```

4. Activate the virtual environment:

   - On macOS and Linux:

     ```sh
     source venv/bin/activate
     ```

   - On Windows:

     ```sh
     .\venv\Scripts\activate
     ```

## Installing PyQt5

With the virtual environment activated, install the required libraries with the following command:

```sh
pip install -r requirements.txt
```

## Set the config.json

1. Copy the `example.config.json` file and rename it to `config.json`.
2. Go to https://console.neurosity.co/settings.
3. Select your device by choosing its ID from the available options.
4. Go to settings
5. Copy the device code.
6. Open the config.json file and paste the device code into the appropriate field, along with your Neurosity account email and password.

## Running the App

With the virtual environment activated, run the app with the following command:

```sh
python src/CrownRecorder.py
```
