# Lab 5 — Static Code Analysis: Issue Documentation

Line numbers refer to the original `flight_reservation_system.py`.

| Issue | Type | Original line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Shell command execution (`os.system`) | High — Security (Bandit B605) | 63 | Executed a shell command using a filename in a command string. | Removed shell execution and printed a status message instead. |
| Weak MD5 hash | High — Security (Bandit B324) | 52 | MD5 is not appropriate when a cryptographic hash is required. | Replaced MD5 with SHA-256. |
| Unsafe `eval()` | Medium — Security (Bandit B307) | 47 | Could execute arbitrary Python expressions. | Removed expression evaluation and calculate the surcharge directly. |
| Mutable default argument | Bug / Code quality (Pylint W0102) | 15 | The default list could be shared across calls. | Changed the default to `None` and create a fresh list for each call. |
| Broad exception handler | Reliability / Security (Bandit B110; Flake8 E722) | 27–32 | A bare `except` and `pass` hid errors. | Removed the exception handler and validate the flight number first. |
| Hardcoded secret | Security (Bandit B105) | 75 | A token was stored in source and printed. | Read `AIRLINE_API_SECRET` from the environment and never print its value. |
| Insecure PIN generation | Security (Bandit B311) | 56 | `random.randint` is not suitable for security-sensitive PINs. | Used `secrets.randbelow`. |
| Unused imports/variables | Code quality (Pylint / Flake8) | Multiple | Unused names made the code harder to maintain. | Removed unused imports and variables. |
| Naming and documentation | Code quality (Pylint) | Multiple | Function names did not follow `snake_case`; docstrings were missing. | Renamed functions and added docstrings. |
| Line length / formatting / final newline | Style (Flake8 / Pylint) | Multiple | Some lines exceeded style limits and the file lacked a final newline. | Wrapped long lines and ensured standard formatting and a final newline. |
| File handling | Code quality (Pylint) | 60–62 | File was opened without a context manager or explicit encoding. | Used `Path.open()` with UTF-8 encoding and a context manager. |
| Flight validation and summary | Correctness | Multiple | Availability and cancellation logic did not consistently account for seat counts or unknown flights. | Added flight existence and seat-count checks. |

## Verification

Run the tools against the final program and compare the results with the original reports. Only report a finding as resolved if the after-report confirms it.
