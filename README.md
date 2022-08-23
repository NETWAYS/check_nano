## check_nano.py
***
Framework to build icinga checks against "Inveo Nano Temperature Sensore"

## Checks
The check command will ouput the temperature based on your "Inveo Nano Sensore" The alarm parameters are set in the administration panel of your sensor. The Plugin will query your sensors xml page to get all the information it needs. 

Example output:
```
check_nano: OK temp=31.2°C, alarm=False
```
Monitoring states:
- OK = alarm is off 
- CRITICAL = alarm is on
- UNKOWN = sensor is not reachable

## Arguments

```
usage: check_nano.py [-h] -H HOST

options:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Nano sensor hostname (Premise)

```

## Manual syntax examples

```
python3 check_nano.py -H <your_host>

python3 check_nano.py --Host <your_host>
```

## License
***

The MIT License

Copyright 2022 NETWAYS GmbH

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
