#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

DEBUG = True


class Error(Exception):
    pass


class InputError(Error):

    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg


def error(*objs):
    print('ERROR:', *objs, file=sys.stderr)


def debug(*objs):
    global DEBUG
    if DEBUG:
        print('DEBUG:', *objs, file=sys.stdout)
