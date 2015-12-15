#!/usr/bin/python
# -*- coding: utf-8 -*-

def getExtension(file):
    parts = file.split(".")
    return parts.pop()

def getFilename(file):
    parts = file.split(".")
    parts.pop()
    filename = parts[0]
    for part in parts[1:]:
        filename = filename+"."+part
    return filename
