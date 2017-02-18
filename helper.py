#!/usr/bin/env python
# vur: a void user repository.
# Licensed under the MIT License.
# Define the name and version
name = "A Void User Repository Helper"
version = "0.3"
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
server = config.get('main', 'server', fallback="https://github.com/jcjordyn130/vur-templates/raw/master")
storagedir = config.get('main', 'storagedir', fallback=os.environ['HOME'] + "/.cache/vur/")
sudocommand = config.get('main', 'sudocommand', fallback="sudo")

# Parse the command line arguments
parser = argparse.ArgumentParser(description='A helper script for the void user repository.')
parser.add_argument('-f','--first-time', help='First time setup and init.', dest='firsttime', action='store_true', required=False)
parser.add_argument('-s','--bootstrap', help='Bootstraps xbps-src.', dest='bootstrap', action='store_true', required=False)
parser.add_argument('-u','--update', help='Updates xbps-src.', dest='update', action='store_true', required=False)
parser.add_argument('-v','--version', help='Prints the version.', dest='version_boolean', action='store_true', required=False)
parser.add_argument('-i','--install', help='Package to build and install', required=False)
parser.add_argument('-b','--build', help='Package to build (no auto install)', required=False)
args = parser.parse_args()

# Define functions
def install(str):
	print("Installing package: %s" % str)
	subprocess.call([sudocommand, "xbps-install", "--repository=" + storagedir + "/hostdir/binpkgs", str])

def build(str):
	print("Building package: %s" % str)
	if not os.path.exists(storagedir + "/srcpkgs/" + str):
		os.makedirs(storagedir + "/srcpkgs/" + str)
		urllib.urlretrieve(server + "/" + str + "/" + "template", storagedir + "/srcpkgs/" + str + "/template")
	subprocess.call([storagedir + "/xbps-src", "pkg", str])

def update():
	print ("Updating xbps-src...")
	subprocess.call(["git", "pull"])
	subprocess.call([storagedir + "/xbps-src", "bootstrap-update"])

def bootstrap():
	print ("Bootstrapping xbps-src...")
	subprocess.call([storagedir + "/xbps-src", "binary-bootstrap"])

# Do things if certain paramaters are passed.
if args.firsttime:
	# If the storagedir doesn't exist, create it.
	if not os.path.exists(storagedir):
	        print ("Making the storage directory (%s)..." % storagedir)
		os.makedirs(storagedir)
	print ("Fetching the void-packages repo...")
	# Clone the git repo here.
	subprocess.call(["git", "clone", "https://github.com/voidlinux/void-packages.git", storagedir])
	# Lets bootstrap!
        bootstrap()

if args.bootstrap:	
	bootstrap()

if args.update:
	update()

if args.version_boolean:
	print (name + " " + version)
	exit(0)

if args.build:
	build(args.build)

if args.install:
	install(args.install)
