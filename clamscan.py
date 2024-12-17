""" 
This script runs a clamscan on the specified directory and logs the output to a file.

The script is configured to exclude certain directories from the scan, as defined in the `excluded_directories` list.

"""

import subprocess
import datetime
from os import environ

from ..constants import clamscan_exlcuded_directories # Remove this line

# Define the directory to scan and the log file
SCAN_DIR = environ.get('DATA_DIR')
LOG_FILE = "/var/log/clamscan.log"

excluded_directories: list[str] = [
    # Add any additional directories to exclude from the scan here
    # e.x 
    # '/root', '/etc', '/home'
    ] + clamscan_exlcuded_directories # <--- Remove this line

excluded_directories_cli = ['--exclude-dir=' + x for x in excluded_directories]

# Run clamscan and save the output to the log file
def run_clamscan():
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"Scan started at {datetime.datetime.now()}")
        result = subprocess.run(["clamscan", "-r", SCAN_DIR, '--infected'] + excluded_directories_cli, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        log_file.write(result.stdout.decode())
        log_file.write(result.stderr.decode())
        log_file.write(f"Scan finished at {datetime.datetime.now()}\n")
    ...
if __name__ == "__main__":
    run_clamscan()