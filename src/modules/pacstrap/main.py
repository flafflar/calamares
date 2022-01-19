#!/usr/bin/env python3
import libcalamares
import subprocess
import re

total_packages = -1
downloaded_packages = 0
installed_packages = 0

output = ""

def output_handler(line):
    global total_packages, downloaded_packages, installed_packages
    global output

    output += line + '\n'
    libcalamares.utils.debug(line)

    if line.startswith('Packages ('):
        total_packages = int(re.findall('\((\d+)\)', line)[0])

    # Catch percentages in the output
    percentages = re.findall('\d+%', line)
    if len(percentages) > 0 and total_packages != -1:
        downloaded_packages = int(downloaded_packages) + float(percentages[0][:-1]) / 100.0
    elif 'downloading' in line and total_packages != -1:
        downloaded_packages += 1

    if 'installing' in line and total_packages != -1:
        installed_packages += 1

    if total_packages != -1:
        libcalamares.job.setprogress((downloaded_packages/2 + installed_packages/2) / total_packages)

def run():
    """
    Installing the base system
    """

    root_mount_point = libcalamares.globalstorage.value("rootMountPoint")

    if root_mount_point == None or root_mount_point == "":
        return "Error", "Root not mounted"

    packages = libcalamares.job.configuration.get("packages")
    libcalamares.utils.debug('Packages to install: ' + ','.join(packages))

    try:
        libcalamares.utils.host_env_process_output(['stdbuf', '-oL', 'pacstrap', root_mount_point] + packages, output_handler)
    except subprocess.CalledProcessError as e:
        return f"Error: pacstrap exited with exit code {e.returncode}", f"Command output:\n{output}"
