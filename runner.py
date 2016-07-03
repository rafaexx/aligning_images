#!/usr/bin/env python
# coding: utf-8

import argparse
import pystache
import subprocess

from os import listdir
from os.path import isfile, join


def folder_to_occurs(folder="tifs", pattern=".tif"):
    """
    Get a list of occurs inside a folder based on the pattern
    """
    file_list = []
    for filename in listdir(folder):
        if isfile(join(folder, filename)):
            sufix_to_ignore = len(pattern) * -1
            file_list.append(filename[0:sufix_to_ignore])

    return list(set(file_list))


def create_descriptors(occurs):
    """
    Generate a new descriptor file
    """
    #images_folder = "/home/rafael/Desktop/rafael_ubuntu/tifs/"
    images_folder = "/home/roger/workspacepy/aligning_images/tifs"
    for filename in occurs:
        with open('templates/descriptor.txt', 'rb') as descriptor:
            content = pystache.render(descriptor.read(), {'filename': filename,
                                                          'folder': images_folder})
            file = open("descriptors/{0}.txt".format(filename), "w")
            file.write(content)
            file.close()


def execute_command(occurs):
    """
    Execute a command for each occurs
    """
    output_folder = "/home/roger/workspacepy/aligning_images/outputs"
    descriptor_folder = "/home/roger/workspacepy/aligning_images/descriptors"
    for filename in occurs:
        cmd = "PTmender -o {0}/{1} {2}/{3}.txt".format(
            output_folder,
            filename,
            descriptor_folder,
            filename)
        #print "  -->", cmd
        subprocess.Popen(cmd, shell=True, executable='/bin/bash')

parser = argparse.ArgumentParser(description='Script runner')
parser.add_argument('--folder', help='Folder for locating files. I.e: tifs/')
parser.add_argument('--pattern', help='Pattern to ignore. I.e: _?.tif')

args = parser.parse_args()

if args.folder:
    occurs = folder_to_occurs(args.folder, args.pattern)
    create_descriptors(occurs)
    execute_command(occurs)
