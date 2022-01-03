#!/usr/bin/env python3
import libcalamares
import subprocess

def run():
    """
    Installing the base system
    """

    root_mount_point = libcalamares.globalstorage.value("rootMountPoint")

    subprocess.run(['sudo' 'pacstrap', root_mount_point, 'base', 'linux'])
