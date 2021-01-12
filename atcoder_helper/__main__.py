#!/usr/bin/env python

import argparse
import logging

import argcomplete
import pkg_resources

import atcoder_helper.command.gen

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

version = pkg_resources.get_distribution("atcoder-helper").version


def get_sub_commands():
    return [v for v in vars(atcoder_helper.command) if not v.startswith("_")]


def get_sub_command_module(sub_command):
    return getattr(atcoder_helper.command, sub_command)


def main() -> None:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    logging.basicConfig(
        handlers=[stream_handler], format="%(name)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--version", action="version", version=f"%(prog)s {version}")

    subparsers = parser.add_subparsers(dest="command")
    for sub_command in get_sub_commands():
        sub_command_module = get_sub_command_module(sub_command)
        sub_command_module.add_arguments(subparsers.add_parser(sub_command))

    argcomplete.autocomplete(parser, exclude=["-h", "--help", "--version"])

    args = parser.parse_args()

    sub_command_module = get_sub_command_module(args.command)
    sub_command_module.main(args)


if __name__ == "__main__":
    main()
