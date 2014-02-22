#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
import sys

from ddp.client import DdpClient


def main(argv=None):
    if argv is None:
        argv = sys.argv
    args = build_argument_parser().parse_args(args=argv[1:])

    client = None
    try:
        client = DdpClient(args.ddp_server)
        client.connect()
        run_command(client, args)
    finally:
        if client is not None:
            try:
                client.disconnect()
            except:
                # Nothing we can do.
                pass
    return 0


def build_argument_parser():
    parser = ArgumentParser()
    parser.add_argument('ddp_server')
    subparsers = parser.add_subparsers(dest='command')
    addsms = subparsers.add_parser('addsms')
    addsms.add_argument('number')
    addsms.add_argument('message')
    reset = subparsers.add_parser('reset')
    reset.add_argument('num_words', type=int)
    return parser


def run_command(client, args):
    commands = {
        'addsms': addsms,
        'reset': reset,
    }
    command = commands[args.command]
    reply = command(client, args)
    print_reply(reply)


def addsms(client, args):
    return client.method('addSms', [args.number, args.message])


def reset(client, args):
    return client.method('reset', [args.num_words])


def print_reply(reply):
    items = reply.items()
    items.sort()

    key_width = max(len(item[0]) for item in items)

    parts = []
    for key, value in items:
        part = '{0:{1}}: {2}'.format(key, key_width, value)
        parts.append(part)

    reply_string = '\n'.join(parts)
    print(reply_string)


def max_len(iterable):
    return max(len(item) for item in iterable)


if __name__ == '__main__':
    try:
        return_code = main()
    except KeyboardInterrupt:
        return_code = 1
    exit(return_code)

