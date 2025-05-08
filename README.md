# Description

`notify_signal.py` is a Python script that sends **Nagios notifications via Signal Messenger** using a **Signal REST API**. It allows Nagios monitoring systems to notify users about host and service states directly via Signal, which is a secure messaging platform.

## Features

- Sends Nagios host and service notifications through Signal.
- Supports both **authenticated** and **unauthenticated** Signal API usage.
- Configurable for custom Signal numbers and API URLs.
- Logs execution and errors to either **systemd journal** or stdout.

## Setup

* 1 Using a venv   
  * 1.1 Create the venv   
    ```bash
       python3 -m venv notify_signal
       cd notify_signal
       source bin/activate
    ```

  * 1.2 Clone the Repository   
    ```bash
       git clone https://github.com/pb1dft/notify_signal/
       cd notify_signal
    ```
  * 1.3 Install Requirements   
    ```bash
    pip install -r requirements.txt
    ```
* 2 Using a RHEL based system with default packages
  * 2.1 Clone the Repository   
    ```bash
       git clone https://github.com/pb1dft/notify_signal/
       cd notify_signal
       chmod +x notify_signal.py
    ```
    
## Requirements

- Python 3.6+
- External services:
  - Signal REST API server (e.g., signal-cli-rest-api (https://github.com/bbernhard/signal-cli-rest-api))
- Python libraries:
  - argparse
  - requests
  - systemd

## Configuration

1. **Configure the script**:
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
      
 2. **Add command lines to nagios**:
    - Copy the contents from **nagios_config_lines.txt** to your nagios config
    - Configure your nagios contact with a pager. Set the pager to the contacts phone/uuid or groupId
    - Example contact:
      ```text
      define contact{
        contact_name                    signal   ; Signal group
        alias                           signal
        use                             generic-contact
        service_notification_commands   notify-service-by-signal    ; send service notifications via signal
        host_notification_commands      notify-host-by-signal    ; send host notifications via signal
        email                           contact@localhost
        pager                           group.iuyeoqiwuyoiushuih0=
      }
      ```

### Syntax:
```bash
python3 notify_signal.py -h to see all options
```



