#! /usr/bin/env python3
############################################################################
# The MIT License
#
# Copyright (c) 2022 NETWAYS GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
############################################################################
# Author: Andre Paskowski
# GitHub: https://github.com/APaskowski

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from xml.etree import ElementTree as ET
import sys
import argparse
import os

# State output
states = ["OK", "WARNING", "CRITICAL", "UNKNOWN"]


def main():
    # Parse hostname
    scriptname = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(prog=scriptname)
    parser.add_argument(
        "-H", "--host", type=str, required=True,
        help="Nano sensor hostname (Premise)"
    )
    args = parser.parse_args()

    url = f"http://{args.host}/status.xml"
    state = 3

    try:
        handler = urlopen(url)
        # Convert UTF-8 to ISO here, device deliver 8859-1 encodings
        content = handler.read().decode(encoding="iso-8859-1")
        root = ET.fromstring(content)
        data = {}
        for child in root:
            try:
                data[child.tag] = float(child.text)
            except ValueError:
                data[child.tag] = child.text
        # Convert alarm attribute value explicitly to boolean
        data["on"] = bool(data["on"])
        # Output temperature and Alarm state (true/false)
        if data["on"] is True:
            state = 2
        elif data["on"] is False:
            state = 0

        # Output of temp and alarm.
        # The "°C" is a html entity to make it readable in icinga
        print(
            f"check_nano: {states[state]} temp={data['temp1']}&deg;C," +
            f" alarm={data['on']}|'temp'={data['temp1']}"
        )
        sys.exit(state)

    except (HTTPError, URLError) as err:
        print(f"{states[3]}: error={err}")
        sys.exit(3)


if __name__ == "__main__":
    main()
