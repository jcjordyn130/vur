#!/usr/bin/env python
# vur: a void user repository.
# Licensed under the MIT License.
# Define the name and version
name = "a vur helper"
version = "0.1"
# Imports
import os
import sys
import configparser
import argparse
import subprocess
import urllib

# Setup the configuration file
configfile = os.environ['HOME'] + "/.vurhelper.conf" # Change where the config file is here
config = configparser.ConfigParser(interpolation=None)
config.read(configfile)

# Start getting the config values
server = config.get('main', 'server', fallback="https://server.jordynsblog.tk/void-templates")
storagedir = config.get('main', 'storagedir', fallback=os.environ['HOME'] + "/.cache/vur/")

# Go into the storage dir
os.chdir(storagedir)

# Parse the command line arguments
parser = argparse.ArgumentParser(description='A helper script for the void user repository.')
parser.add_argument('-f','--first-time', help='First time setup and init.', dest='firsttime', action='store_true', required=False)
parser.add_argument('-b','--bootstrap', help='Bootstraps xbps-src.', dest='bootstrap', action='store_true', required=False)
parser.add_argument('-u','--update', help='Updates xbps-src.', dest='update', action='store_true', required=False)
parser.add_argument('-v','--version', help='Prints the version.', dest='version_boolean', action='store_true', required=False)
parser.add_argument('-i','--install', help='Package to install', required=False)
args = parser.parse_args()

if args.firsttime:
	# If the storagedir doesn't exist, create it.
	if not os.path.exists(storagedir):
	        print ("Making the storage directory (%s)..." % storagedir)
		os.makedirs(storagedir)
	print ("Fetching the void-packages repo...")
	# Lets use gitpython later. (git clone)
	subprocess.call(["git", "clone", "https://github.com/voidlinux/void-packages.git", storagedir])
        print ("Bootstrapping xbps-src...")
        subprocess.call([storagedir + "/xbps-src", "binary-bootstrap"])

if args.bootstrap:	
	print ("Bootstrapping xbps-src...")
	subprocess.call([storagedir + "/xbps-src", "binary-bootstrap"])

if args.update:
	print ("Updating xbps-src...")
	os.chdir(storagedir)
	subprocess.call(["git", "pull"])
	subprocess.call([storagedir + "/xbps-src", "bootstrap-update"])

if args.version_boolean:
	print (name + " " + version)
	exit(0)

if args.install:
	if not os.path.exists(storagedir + "/srcpkgs/" + args.install):
		os.makedirs(storagedir + "/srcpkgs/" + args.install)
		urllib.urlretrieve(server + "/" + args.install + "/" + "template", storagedir + "/srcpkgs/" + args.install + "/template")
	subprocess.call([storagedir + "/xbps-src", "pkg", args.install])
