#!/usr/bin/env python3
"""Send Nagios notifications via Signal Messenger using a REST API."""

import argparse
import json
import os
import random
import time

import requests

try:
    from systemd import journal

    def log_invocation(delay):
        """Log the command invocation with delay to stdout (fallback if systemd journal is not available)."""
        import sys
        full_command = ' '.join(sys.argv)
        journal.send(f'Command executed ({delay}): {full_command}', SYSLOG_IDENTIFIER='notify_signal')


except ImportError:

    def log_invocation(delay):
        """Log the command invocation with delay to stdout (fallback if systemd journal is not available)."""
        import sys
        full_command = ' '.join(sys.argv)
        print(f'Command executed ({delay}): {full_command}')


def load_config():
    """
    Load configuration from 'notify_signal_config.json' located in the same directory.

    Returns:
        dict: Configuration values including API URL, auth settings, user, and password.
    """
    config_path = os.path.join(os.path.dirname(__file__), 'notify_signal_config.json')
    with open(config_path, 'r') as f:
        return json.load(f)


config = load_config()


def parse_args():
    """
    Parse command-line arguments used for generating Nagios notifications.

    Returns:
        argparse.Namespace: Parsed arguments for host/service notification.
    """
    parser = argparse.ArgumentParser(description='Nagios notification via Signal')
    parser.add_argument('-f', '--from_number', nargs='?', required=True, help='Sender Signal number')
    parser.add_argument('-o', '--object_type', nargs='?', required=True)
    parser.add_argument('--contact', nargs='?', required=True, help='Receiver Signal number')
    parser.add_argument('--notificationtype', nargs='?')
    parser.add_argument('--hoststate', nargs='?')
    parser.add_argument('--hostname', nargs='?')
    parser.add_argument('--hostaddress', nargs='?')
    parser.add_argument('--servicestate', nargs='?')
    parser.add_argument('--servicedesc', nargs='?')
    parser.add_argument('--ackcomment', nargs='?')
    parser.add_argument('--author', nargs='?')
    parser.add_argument('--output', nargs='?')
    return parser.parse_args()


def send_notification(from_number, to_number, message):
    """
    Send a Signal message via the Signal REST API.

    Args:
        from_number (str): Sender's Signal number.
        to_number (str): Recipient's Signal number.
        message (str): Message body to send.
    """
    api_url = config.get('signal_rest_api_url')
    use_auth = config.get('signal_rest_api_use_auth', False)
    user = config.get('signal_rest_api_user')
    password = config.get('signal_rest_api_password')

    parsed_message = message.replace('\\n', '\n')

    payload = {
        'message': parsed_message,
        'number': from_number,
        'recipients': [to_number]
    }
    try:
        auth = (user, password) if use_auth else None
        response = requests.post(api_url, json=payload, auth=auth)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print('Error sending Signal message:', e)


def host_notification(args):
    """
    Construct a notification message for a host object.

    Args:
        args (argparse.Namespace): Parsed arguments.

    Returns:
        str: Formatted host notification message.
    """
    state = ''
    if args.notificationtype == 'ACKNOWLEDGEMENT':
        state = u'\U0001F515 '
        args.output = '\nAcknowledged by: %s\n%s' % (args.author, args.ackcomment)
    elif args.hoststate == 'UP':
        state = u'\U00002705 '
    elif args.hoststate == 'DOWN':
        state = u'\U0001F525 '
    elif args.hoststate == 'UNREACHABLE':
        state = u'\U00002753 '

    return '%s%s (%s): %s' % (
        state,
        args.hostname,
        args.hostaddress,
        args.output or '',
    )


def service_notification(args):
    """
    Construct a notification message for a service object.

    Args:
        args (argparse.Namespace): Parsed arguments.

    Returns:
        str: Formatted service notification message.
    """
    state = ''
    if args.notificationtype == 'ACKNOWLEDGEMENT':
        state = u'\U0001F515 '
        args.output = '\nAcknowledged by: %s\n%s' % (args.author, args.ackcomment)
    elif args.servicestate == 'OK':
        state = u'\U00002705 '
    elif args.servicestate == 'WARNING':
        state = u'\U000026A0 '
    elif args.servicestate == 'CRITICAL':
        state = u'\U0001F525 '
    elif args.servicestate == 'UNKNOWN':
        state = u'\U00002753 '

    return '%s%s/%s: %s' % (
        state,
        args.hostname,
        args.servicedesc,
        args.output or '',
    )


def main():
    """
    Process arguments and send Signal notifications based on Nagios input.

    Introduce a small random delay, parse arguments, format the message, and send the notification.
    """
    delay = random.uniform(0.1, 3.0)
    time.sleep(delay)
    # log_invocation(delay)
    args = parse_args()

    if args.object_type == 'host':
        message = host_notification(args)
    elif args.object_type == 'service':
        message = service_notification(args)
    else:
        print('Unknown object type:', args.object_type)
        return

    send_notification(args.from_number, args.contact, message)


if __name__ == '__main__':
    main()

