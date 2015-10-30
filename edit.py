#!/usr/bin/python

# Copyright (c) 2015 Ryan Skonnord
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Transforms index-edit.html into index.html"""

from __future__ import print_function

import re

with open('index-edit.html') as f:
    html = f.read()

html = re.sub(r'(<code.*?>)\s*(<pre.*?>)', r'\2\1', html)
html = re.sub(r'(</pre\s*>)\s*(</code\s*>)', r'\2\1', html)

def clean_code_text(code_text):
    lines = [line.rstrip() for line in code_text.split('\n')]
    def is_junk(line):
        return (not line) or line.startswith('#')
    while is_junk(lines[0]):
        lines = lines[1:]
    while is_junk(lines[-1]):
        lines = lines[:-1]
    return '\n'.join(lines)

def replace_codefile(match):
    open_tag = match.groups()[0]
    filename = match.groups()[1]
    with open(filename) as f:
        code_text = clean_code_text(f.read())
    return '<pre>{0}>{1}</code></pre>'.format(open_tag, code_text)
    
html = re.sub(r'(<code.*?)\s+data-file="(.*?)"\s*(/>|>\s*</code>)', replace_codefile, html)

with open('index.html', mode='w') as f:
    print(html, file=f)
