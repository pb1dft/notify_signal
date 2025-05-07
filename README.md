# Notify Signal

`notify_signal.py` is a Python script that sends **Nagios notifications via Signal Messenger** using a **Signal REST API**. It allows Nagios monitoring systems to notify users about host and service states directly via Signal, which is a secure messaging platform.

## Features

- Sends Nagios host and service notifications through Signal.
- Supports both **authenticated** and **unauthenticated** Signal API usage.
- Configurable for custom Signal numbers and API URLs.
- Logs execution and errors to either **systemd journal** or stdout.

## Requirements

- Python 3.6+
- `requests` Python package (for making HTTP requests)
- (Optional) `systemd` for logging to system journal

## Installation

1. **Clone this repository**:
    ```bash
    git clone https://.git
    cd notify_signal
    ```

2. **Install dependencies**:
    ```bash
    pip install requests
    ```

    If you want systemd journal support (optional):
    ```bash
    sudo apt-get install python3-systemd
    ```

3. **Configure the script**:
    - Copy or create `notify_signal_config.json` in the same directory as `notify_signal.py` with the following configuration options:
    
    ```json
    {
      "signal_rest_api_url": "http://localhost:8080/v2/send",
      "signal_rest_api_use_auth": false,
      "signal_rest_api_user": "user",
      "signal_rest_api_password": "password"
    }
    ```

    - Modify the configuration values to fit your Signal API settings.

## Usage

Run the script via the command line to send a Signal notification:

### Syntax:
```bash
python3 notify_signal.py -f <from_number> -o <object_type> --contact <to_number> [additional options]
```



