import datetime
import re
import os
import sys
import glob


# Written for Python 2.7
# This script can be used to send a metric which tells how many days have passed
# since the last repair to Prometheus

# Can safely be added to cron 

# The lines below allows the script to scan for the last log file created

path = '<your_log_file_directory>'
log_file=glob.glob(path + '*.log')
if not log_file:
 sys.exit()
 
latest_log = max(log_file, key=os.path.getctime)

def get_time_since_last_repair():
    # Open the Cassandra log file
    with open(latest_log, "r") as f:
        # Read the log file into a list of lines
        lines = f.readlines()
    # Reverse the list of lines so we can search through it in reverse chronological order
    lines.reverse()
    # Initialize variable to store the timestamp of the last repair completion message
    last_repair_timestamp = None
    # Search through the log file for the last repair completion message
    for line in lines:
        match = re.search(r'(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d{3}', line)
        if match and "Repair command" and "finished" in line:
            last_repair_timestamp = match.group("date")
            break
    if last_repair_timestamp is not None:
        # Parse the timestamp as a datetime object
        last_repair_time = datetime.datetime.strptime(last_repair_timestamp, "%Y-%m-%d %H:%M:%S")
        # Get the current time
        current_time = datetime.datetime.now()
        # Calculate the time difference between the current time and the time of the last repair
        time_since_last_repair = current_time - last_repair_time
        time_since_last_repair = round(time_since_last_repair.total_seconds()/86400)
        # Print the time since the last repair in timestamp format
        print("days_since_last_repair {}".format(time_since_last_repair))
    else:
        print("N/A")

# Create the prom file
with open("<path_and_name_of_the_prom_file>", "w") as f:
    sys.stdout = f
    get_time_since_last_repair()