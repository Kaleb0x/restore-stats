#!/bin/python
import shutil
import sys
import os


def restore_stat(from_backup, to_original, type):
    try:
        if len(sys.argv) == 4 and os.path.getmtime(to_original) > sys.argv[3]:
            return

        shutil.copystat(from_backup, to_original)

    except FileNotFoundError:
        with open("error.log", "a") as f:
            print(f"Not found in original : {from_backup}")
            f.write(f"{type}:{from_backup}\n")
            return


if __name__ == "__main__":
    original = os.path.abspath(sys.argv[1])
    backup = os.path.abspath(sys.argv[2])

    print(f"Copying file stats from {backup} to {original}")

    for root, dirs, files in os.walk(backup):
        relative_root = os.path.relpath(root, backup)

        for file in files:
            backup_file = os.path.join(backup, relative_root, file)
            original_file = os.path.join(original, relative_root, file)

            print(f"f:{backup_file} -> {original_file}")
            restore_stat(backup_file, original_file, "f")

        for dir in dirs:
            backup_dir = os.path.join(backup, relative_root, dir)
            original_dir = os.path.join(original, relative_root, dir)

            print(f"d:{backup_dir} -> {original_dir}")
            restore_stat(backup_dir, original_dir, "d")
