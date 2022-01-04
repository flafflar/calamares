#!/usr/bin/env python3
import libcalamares
import re

total_packages = -1
downloaded_packages = 0
installed_packages = 0

def output_handler(line):
    global total_packages, downloaded_packages, installed_packages
    if line.startswith('Packages ('):
        total_packages = int(re.findall('\((\d+)\)', line)[0])
    if 'downloading' in line and total_packages != -1:
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

    packages = libcalamares.job.configuration.get("packages")

    print(packages)

    try:
        libcalamares.utils.host_env_process_output(['pacstrap', root_mount_point] + packages, output_handler)
    except:
        pass
