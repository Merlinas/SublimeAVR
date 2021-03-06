"""
AVR-GCC output parser
Copyright (c) 2013 Kim Blomqvist, kblomqvist.github.io

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import os, subprocess

def devices(location = ""):
	p = subprocess.Popen(
		[os.path.join(location, "avr-as"), "-mlist-devices"],
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE
	)
	out, err = p.communicate()

	if err: # in case -mlist-devices is not supported by avr-as
		dump = err
		cut = -9
	else:
		dump = out
		cut = -1

	devices = []
	for line in dump.decode().split(os.linesep)[1:]:
		devices.extend(line.strip().split(" "))
	return devices[:cut]
