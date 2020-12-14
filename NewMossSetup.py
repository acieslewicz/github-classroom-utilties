#!/usr/bin/env python3

import argparse
import os
import shutil
import time

def parse_roster(roster_path):
    with open(roster_path) as f:
        names = f.read().splitlines()
    return names

def clone_assignments(names, classroom, assignment, tag):
    for name in names:
        print(name)
        clone_cmd = f"git clone --branch {tag} git@github.com:{classroom}/{assignment}-{name}"
        os.system(clone_cmd)
    # Clone Starter as well
    clone_cmd = f"git clone git@github.com:{classroom}/{assignment}-starter"
    os.system(clone_cmd)
    time.sleep(5)

def parse_repositories(names, destination_path):
    for root, _, files in os.walk(os.getcwd()):
        for file in files :
            if str(file).endswith(('.c', '.h')):
                for name in names:
                    if name in root :
                        shutil.copy(os.path.join(root, file), os.path.join(destination_path, "Moss-Directory", name))

def main():
    parser = argparse.ArgumentParser(
        description='Setup Github classroom project for MOSS.'
    )
    parser.add_argument(
        '-c', '--classroom',
        type=str, required=True,
        help='Name of Github Classrrom Organization as it appears in the url.'
    )
    parser.add_argument(
        '-a', '--assignment',
        type=str, required=True,
        help='Assignment name as it would appear in the url.'
    )
    parser.add_argument(
        '-t', '--tag',
        type=str, required=True,
        help='Project submission tag.'
    )
    parser.add_argument(
        '-r', '--rosterPath',
        type=str, required=True,
        help='Location of the classroom roster.'
    )
    parser.add_argument(
        '-d', '--destinationPath',
        type=str, required=True,
        help='Location of the MOSS prep output.'
    )
    parser.add_argument(
        '-m', '--setupMoss',
        type=bool, required=False, default=False,
        help='Location of the MOSS prep output.'
    )
    options = parser.parse_args()
    destination_path = os.path.abspath(options.destinationPath)
    names = parse_roster(options.rosterPath)

    # Clone Project Repositories
    os.chdir(destination_path)
    os.mkdir("GitHub-Repos")
    os.chdir("GitHub-Repos")
    clone_assignments(names, options.classroom, options.assignment, options.tag)

    # Setup Directory structure for MOSS
    if options.setupMoss:
        os.chdir(destination_path)
        os.mkdir("Moss-Directory")
        os.chdir("Moss-Directory")
        for name in names:
            os.mkdir(name)

        # Go through every cloned repository and copy over ".c" and ".h" files
        os.chdir(destination_path)
        os.chdir("GitHub-Repos")
        parse_repositories(names, destination_path)

if __name__ == "__main__":
    main()