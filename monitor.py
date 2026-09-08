#!/usr/bin/env python3

import re
import datetime
import os, glob
import sys
import settings
import subprocess as sp
import numpy as np

os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))

with open(settings.log_path) as infile:
    logging = infile.read()

date_regex = r'[A-Z][a-z]{2} [A-Z][a-z]{2} [0-9, ]* [0-9]{2}:[0-9]{2}:[0-9]{2} [A-Z]{3} [0-9]{4}'
matches = re.findall(date_regex, logging)
if not matches:
    exit(1)

logs = np.array(logging.strip().split('\n'))
date_mask = np.vectorize(lambda x: x in matches)(logs)

ignore_regex = [
    r'I\d{4} \d{2}:\d{2}:\d{2}.\d{6} \d{7} fork_posix.cc:\d*\] Other threads are currently calling into gRPC, skipping fork\(\) handlers',
    r'I\d{4} \d{2}:\d{2}:\d{2}.\d{6} \d{7} ev_poll_posix.cc:\d*\] FD from fork parent still in poll list: fd\(\d*, generation: \d*\)'
]

ignore_mask = np.zeros(len(logs), dtype=bool)
for regex in ignore_regex:
    ignore_matches = re.findall(regex, logging.strip())
    ignore_mask |= np.vectorize(lambda x: x in ignore_matches)(logs)

day_of_week = np.array([x.split(' ')[0] for x in logs[date_mask]])

np.where((day_of_week == day_of_week[-1])[::-1])

# if len(matches) != len():
#     emails = ' '.join([f"'{email}'" for email in settings.logging_emails])
#     sp.run(f'"{settings.create_event_path}" "{settings.error_message}" 0 {emails}', shell=True)

