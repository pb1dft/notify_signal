# Notify Signal

`notify_signal.py` is a Python script that sends **Nagios notifications via Signal Messenger** using a **Signal REST API**. It allows Nagios monitoring systems to notify users about host and service states directly via Signal, which is a secure messaging platform.

## Features

- Sends Nagios host and service notifications through Signal.
- Supports both **authenticated** and **unauthenticated** Signal API usage.
- Configurable for custom Signal numbers and API URLs.
- Logs execution and errors to either **systemd journal** or stdout.

## Requirements

- Python 3.6+
- External services:
  - Signal REST API server (e.g., signal-cli-rest-api (https://github.com/bbernhard/signal-cli-rest-api))
- Python libraries:
  - argsparse
  - json
  - os
  - random
  - time
  - requests
  - systemd

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

See **nagios_config_lines.txt** for nagios integration.

### Syntax:
```bash
python3 notify_signal.py -h to see all options
```



