# Invalidated LIKE BINARY Bruteforce

Python helper for the **HTB Machine** challenge.

This script automates two parts of the challenge:

* Session bypass using an empty JSON login request.
* Optional admin password extraction using a `LIKE BINARY` condition.

> This project is intended only for CTFs, labs, and authorized security practice environments.

---

## Features

* Clean command-line usage.
* Supports base URL input.
* Extracts the user flag when only the target URL is provided.
* Extracts the admin password only when the admin email is provided.
* Minimal output for cleaner writeups and terminal screenshots.

---

## Requirements

* Python 3
* requests

Install dependencies:

```
pip install requests
```

---

## Usage

### Get flag

```
python3 bruteforce.py -u "http://domain"
```

Expected output:

```
[+] User flag: <user_flag>
```

---

### Extract the user password

```
python3 bruteforce.py -u "http://domain" -e "user@domain"
```

Expected output:

```
[+] User password: <user_password>
```

---

## Parameters

| Parameter       | Description                              |
| --------------- | ---------------------------------------- |
| `-u`, `--url`   | Base URL of the target machine           |
| `-e`, `--email` | User email used for password extraction |

---

## How It Works

When only the target URL is provided, the script sends an empty JSON request to the login endpoint in order to obtain a valid session cookie. Then, it visits the profile page and extracts the displayed user flag.

When an admin email is provided, the script performs character-by-character extraction using a vulnerable parameter similar to:

```
password LIKE BINARY '<prefix>%'
```

Because `LIKE BINARY` is case-sensitive, the script can determine the correct password by testing one character at a time.

---

## Project Structure

```
invalidated-like-binary-bruteforce/
├── bruteforce.py
└── README.md
```

---

## Disclaimer

This tool was created for educational purposes and CTF challenge solving only. Do not use it against systems without explicit authorization.
