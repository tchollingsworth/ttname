# This file is part of ttname.
#
# Copyright 2013 T.C. Hollingsworth <tchollingsworth@gmail.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution. 
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os

from ttname import TTNameTable, info

_testfile = os.path.join(os.path.dirname(__file__), 'data/DejaVuSans.ttf')

def test_sanity():
    assert info.names[0].startswith('copyright notice')
    assert info.names_short['copyright'] == 0
    assert info.platforms[0].startswith('Unicode')
    assert info.encodings[0][0].startswith('Unicode 1.0')
    assert info.langs[1][0].startswith('English')

def test_unknowns():
    assert info.names[100].startswith('Reserved')
    assert info.names[300].startswith('Font-specific')
    assert info.platforms[100].startswith('Unknown')
    assert info.encodings[0][100].startswith('Unknown')
    assert info.langs[1][100].startswith('Unknown')
    
def test_fromfile():
    tt = TTNameTable(_testfile)
    rec = tt.getName(1,1,0,0)
  
    assert info.name(rec).startswith('font family name')
    assert info.platform(rec).startswith('Macintosh')
    assert info.encoding(rec).startswith('Roman')
    assert info.lang(rec).startswith('English')
    
def test_cli_helpers():
    tt = TTNameTable(_testfile)
    rec = tt.getName(1,1,0,0)
    
    assert info.trip(rec) == 'Macintosh (#1)/Roman (#0)/English (#0)'
    assert info.quad(rec) == 'Macintosh (#1)/Roman (#0)/English (#0) font family name (#1)'