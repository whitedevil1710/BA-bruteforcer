# Brute-Force Script

This is a Python script that performs HTTP basic authentication brute-force attacks against a target URL using a list of usernames and passwords.

## Usage

1. Clone the repository:

```bash
git clone https://github.com/whitedevil1710/BA-bruteforcer.git
cd BA-bruteforcer
```

2. Install the required dependencies (termcolor and requests):

```bash
pip install termcolor requests
```
3. Run the script:

```bash
python main.py
```
### Commands

- seturl: Set the target URL for the brute-force attack.
- setuname: Set the list of usernames. Provide either a filename containing usernames (one per line) or list them directly as arguments.
- setpass: Set the list of passwords. Provide either a filename containing passwords (one per line) or list them directly as arguments.
- run: Run the brute-force attack using the provided target URL, username list, and password list.
- history: Display the command history with line numbers.
- clear_history: Clear the command history.

### Disclaimer

Use this script responsibly and only on systems you have explicit permission to test. Unauthorized brute-force attacks are illegal and unethical. The script is provided for educational and ethical purposes only.
