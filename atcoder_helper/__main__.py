#!/usr/bin/env python

import argparse
import logging

import atcoder_helper.command.gen

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main() -> None:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    logging.basicConfig(
        handlers=[stream_handler],
        format="%(name)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    choices = [v for v in vars(atcoder_helper.command) if not v.startswith("_")]

    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=str, choices=choices, help="command")
    ns, args = parser.parse_known_args()

    sub_main = getattr(atcoder_helper.command, ns.command).main
    sub_main(args)


if __name__ == "__main__":
    main()
