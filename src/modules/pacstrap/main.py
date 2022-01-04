#!/usr/bin/env python3
import libcalamares
import subprocess
import re

def run():
    """
    Installing the base system
    """

    root_mount_point = libcalamares.globalstorage.value("rootMountPoint")

    total_packages = -1
    downloaded_packages = 0
    installed_packages = 0
    
    process = subprocess.Popen(['sudo', 'pacstrap', root_mount_point, 'base', 'linux'], stdout=subprocess.PIPE)
    for line in iter(process.stdout.readline, b''):
        
        if line.startswith(b'Packages ('):
            total_packages = int(re.findall('\((\d+)\)', str(line))[0])
        if b'downloading' in line and total_packages != -1:
            downloaded_packages += 1
        if b'installing' in line and total_packages != -1:
            installed_packages += 1

        if total_packages != -1:
            libcalamares.job.setprogress((downloaded_packages/2 + installed_packages/2) / total_packages)
