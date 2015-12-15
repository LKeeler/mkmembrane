#!/usr/bin/python
# -*- coding: utf-8 -*-

class Error(Exception):
    pass

class InputError(Error):
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

