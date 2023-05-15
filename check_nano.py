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
from urllib.parse import urljoin
from urllib.error import HTTPError, URLError
from xml.etree import ElementTree as ET
import ssl
import sys
import argparse


__version__ = "1.0.0"

# State output
states = ["OK", "WARNING", "CRITICAL", "UNKNOWN"]

def commandline(args):
    parser = argparse.ArgumentParser(prog="check_nano")

    parser.add_argument('-V', '--version', action='version', version='check_nano' + __version__)

    parser.add_argument(
        "-H", "--host", type=str, required=True,
        help="Nano sensor hostname (Premise)"
    )
    parser.add_argument('-T', '--timeout', help='Seconds before connection times out (default 10)',
                        default=10,
                        type=int)
    parser.add_argument('--insecure',
                        dest='insecure',
                        action='store_true',
                        default=False,
                        help='Allow insecure SSL connections (default False)')
    parser.add_argument('--protocol',
                        choices=["http", "https"],
                        default='https',
                        help='HTTP protocol, use one of http or https (default https)')

    return parser.parse_args(args)


def get_data(url, timeout, insecure):
    """
    Requests the data via HTTP. Basically a wrapper around urllib.

    Expected Repsonse:
    <response>
    <out>00000000</out>
    <on>00000000</on>
    <in>00000000</in>
    <counter1>0</counter1>
    <temp1>34.3</temp1>
    <mac>00:00:00:00:00:00</mac>
    </response>
    """

    # Default context for connection
    ctx = ssl.create_default_context()
    if insecure is True:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

    response = urlopen(url=url, timeout=timeout, context=ctx) # pylint: disable=consider-using-with

    if response.getcode() >= 400:
        raise RuntimeError("Could not get response")

    # Convert UTF-8 to ISO here, device deliver 8859-1 encodings
    return response.read().decode(encoding="iso-8859-1")

def main(args):
    url = urljoin(f"{args.protocol}://{args.host}", "status.xml")
    state = 3

    try:
        resp = get_data(url=url,
                        timeout=args.timeout,
                        insecure=args.insecure) # pylint: disable=consider-using-with
    except (HTTPError, URLError) as err:
        print(f"check_nano {states[3]}: Could not connect to sensor", err)
        return 3

    try:
        root = ET.fromstring(resp)
    except ET.ParseError as err:
        print(f"check_nano {states[3]}: Could not parse response", err)
        return 3

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

    return state


if __name__ == '__main__': # pragma: no cover
    try:
        ARGS = commandline(sys.argv[1:])
        sys.exit(main(ARGS))
    except SystemExit:
        # Re-throw the exception
        raise sys.exc_info()[1].with_traceback(sys.exc_info()[2]) # pylint: disable=raise-missing-from
    except:
        print("UNKNOWN - Error: %s" % (str(sys.exc_info()[1])))
        sys.exit(3)
