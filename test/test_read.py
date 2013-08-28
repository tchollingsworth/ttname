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
import random

from ttname import TTNameTable
from util import get_fontconfig_data

_testfile = os.path.join(os.path.dirname(__file__), 'data/DejaVuSans.ttf')

def test_matches_reality():
    t = TTNameTable(_testfile)
    
    assert t.getName(0,1,0,0).string.startswith('Copyright (c) 2003 by Bitstream, Inc.')
    assert t.getName(1,1,0,0).string == 'DejaVu Sans'
    assert t.getName(2,1,0,0).string == 'Book'
    assert t.getName(3,1,0,0).string == 'DejaVu Sans'
    assert t.getName(4,1,0,0).string == 'DejaVu Sans'
    assert t.getName(5,1,0,0).string == 'Version 2.33'
    assert t.getName(6,1,0,0).string == 'DejaVuSans'
    assert t.getName(7,1,0,0) is None
    assert t.getName(8,1,0,0).string == 'DejaVu fonts team'
    assert t.getName(9,1,0,0) is None
    assert t.getName(10,1,0,0) is None
    assert t.getName(11,1,0,0).string == 'http://dejavu.sourceforge.net'
    assert t.getName(12,1,0,0) is None
    assert t.getName(13,1,0,0).string.startswith('Fonts are (c) Bitstream (see below).')
    assert t.getName(14,1,0,0).string == 'http://dejavu.sourceforge.net/wiki/index.php/License'
    assert t.getName(15,1,0,0) is None
    assert t.getName(16,1,0,0).string == 'DejaVu Sans'
    assert t.getName(17,1,0,0).string == 'Book'
    assert t.getName(18,1,0,0) is None
    assert t.getName(19,1,0,0) is None
    assert t.getName(20,1,0,0) is None
    
    
def test_matches_fontconfig():
    t = TTNameTable(_testfile)
    fc = get_fontconfig_data(_testfile)
    
    assert t.getName(1,1,0,0).string == fc['family']
    assert t.getName(2,1,0,0).string == fc['style']
    assert t.getName(4,1,0,0).string == fc['fullname']
    assert t.getName(6,1,0,0).string == fc['postscriptname']
    

def test_get_section():
    t = TTNameTable(_testfile)
    
    for record in t.getSection(1,0,0):
        assert record.platformID == 1
        assert record.platEncID == 0
        assert record.langID == 0
    
def test_get_name_from_all():
    t = TTNameTable(_testfile)
    n = list(t.getNameFromAll(1))[0]
    assert n.string == 'DejaVu Sans'

def test_get_names_by_sect():
    t = TTNameTable(_testfile)
    
    for sectinfo, sect in t.getNamesBySection().iteritems():
        assert sectinfo.platformID == sect[random.randrange(0, len(sect))].platformID
        assert sectinfo.platEncID == sect[random.randrange(0, len(sect))].platEncID
        assert sectinfo.langID == sect[random.randrange(0, len(sect))].langID
