# Crown Recorder

App description goes here.

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

With the virtual environment activated, install PyQt5 using pip:

```sh
pip install PyQt5
```

## Set the config.json

1. Go to https://console.neurosity.co/settings.
2. Select your device by choosing its ID from the available options.
3. Go to settings
4. Copy the device code.
5. Open the config.json file and paste the device code into the appropriate field.

## Running the App

With the virtual environment activated, run the app with the following command:

```sh
python CrownRecorder.py
```