#!/usr/bin/env python3

import os
from shutil import copyfile

home_dir = os.getenv('HOME')  # only works on Linux
desktop_dir = os.path.join(home_dir, 'Desktop')
chrome_based_browsers = ['brave', 'chrome', 'chromium', 'vivaldi']


def get_wm_class(desktop_file_contents):
    wm_class = next(filter(lambda s: 'StartupWMClass' in s, desktop_file_contents))\
    .split('=')[-1].replace('\n', '')
    return wm_class


def make_new_exec_line(desktop_file_contents, wm_class):
    el = next(filter(lambda s: 'Exec=' in s, desktop_file_contents))
    exec_line = el.replace('\n', '')
    xdo_append = f' && xdotool search --sync --classname {wm_class} set_window --class {wm_class}\n'
    return exec_line + xdo_append, desktop_file_contents.index(el)


def check_if_xdotool_written(desktop_file_contents):
    return any(filter(lambda s: 'xdotool' in s, desktop_file_contents))


for f in os.listdir(desktop_dir):

    if not any([(browser in f) for browser in chrome_based_browsers]):
        continue

    desktop_file = os.path.join(desktop_dir, f)
    desktop_file_contents = open(desktop_file, 'r').readlines()

    if check_if_xdotool_written(desktop_file_contents):
        print('skipping because xdotool is already written to', desktop_file)
        continue

    wm_class = get_wm_class(desktop_file_contents)
    new_exec_line, idx = make_new_exec_line(desktop_file_contents, wm_class)

    desktop_file_contents[idx] = new_exec_line
    with open(desktop_file, 'w') as nf:
        nf.writelines(desktop_file_contents)

    print('written new xdotool line')
