#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Rodolphe Quiédeville <rodolphe@quiedeville.org>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Read the next song from database and print the filename on STDOUT
"""
from song import Song
from utils import trigger

def main():
    """
    Main function
    """
    nbt = Song()
    fname = nbt.next()
    trigger(fname, "/tmp/python_unix_sockets_example")
    return fname

if __name__ == "__main__":
    print main()
