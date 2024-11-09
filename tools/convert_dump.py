#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import argparse
import os
import shutil
from os import path

ALTERNATE_PARTITION_PATH_MAP = {
    'product': 'system/product',
    'system_ext': 'system/system_ext',
    'vendor': 'system/vendor',
    'odm': 'vendor/odm',
}


def move_sar_system_paths(dump_dir: str):
    # For System-as-Root, move system/ to system_root/ and system/system/
    # to system/
    system_dir = path.join(dump_dir, 'system')
    system_system_dir = path.join(system_dir, 'system')
    if path.isdir(system_system_dir):
        system_root_dir = path.join(dump_dir, 'system_root')
        system_root_system_dir = path.join(system_root_dir, 'system')

        shutil.move(system_dir, system_root_dir)
        shutil.move(system_root_system_dir, dump_dir)


def move_alternate_partition_paths(dump_dir: str):
    # Make sure that even for devices that don't have separate partitions
    # for vendor, odm, etc., the partition directories are copied into the root
    # dump directory to simplify file copying
    for (
        partition,
        alternate_partition_path,
    ) in ALTERNATE_PARTITION_PATH_MAP.items():
        partition_path = path.join(dump_dir, partition)
        if path.isdir(partition_path):
            continue

        partition_path = path.join(dump_dir, alternate_partition_path)
        if not path.isdir(partition_path):
            continue

        shutil.move(partition_path, dump_dir)


parser = argparse.ArgumentParser(
    description='Convert extract dump from bash extract_utils'
    'to python extract_utils structure',
)

parser.add_argument(
    'dump_dir',
    help='dump directory',
    nargs='*',
)


def convert_dump(dump_dir: str):
    dump_output_dir = path.join(dump_dir, 'output')

    if path.isdir(dump_output_dir):
        for file in os.scandir(dump_output_dir):
            shutil.move(file.path, dump_dir)

        shutil.rmtree(dump_output_dir)

    move_sar_system_paths(dump_dir)
    move_alternate_partition_paths(dump_dir)


def convert_dumps(dump_dirs: str):
    for dump_dir in dump_dirs:
        convert_dump(dump_dir)


if __name__ == '__main__':
    parser_args = parser.parse_args()

    convert_dumps(parser_args.dump_dir)
