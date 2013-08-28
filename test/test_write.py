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
import pprint
import random
import tempfile

from ttname import TTNameTable
from util import get_fontconfig_data

_testfile = os.path.join(os.path.dirname(__file__), 'data/DejaVuSans.ttf')

def test_write_existing_fields():
    tempfh = tempfile.NamedTemporaryFile(prefix='ttname-test-write-existing-', suffix='.ttf', delete=False)
    tempfn = tempfh.name
    
    t = TTNameTable(_testfile)
    
    for platID in (1, 3):
        #windows is funky of course
        platEncID = 1 if platID == 3 else 0
        langID = 1033 if platID == 3 else 0
        
        for nameID in (1, 3, 4, 16):        
            t.getName(nameID, platID, platEncID, langID).string = 'Potato Sans'
        
        t.getName(6, platID, platEncID, langID).string = 'PotatoSans'
    
        
    t.save(tempfh)
    tempfh.close()
    
    new_t = TTNameTable(tempfn)

    for i in (1, 3, 4, 16):
        assert new_t.getName(i, 1, 0, 0).string == 'Potato Sans'

    fc = get_fontconfig_data(tempfn)

    assert fc['family'] == 'Potato Sans'
    assert fc['style'] == 'Book'
    assert fc['fullname'] == 'Potato Sans'
    assert fc['postscriptname'] == 'PotatoSans'

    os.unlink(tempfn)

def test_write_new_fields():
    tempfh = tempfile.NamedTemporaryFile(prefix='ttname-test-write-new-', suffix='.ttf', delete=False)
    tempfn = tempfh.name

    t = TTNameTable(_testfile)

    newfields = (7, 9, 10, 12, 150)

    for platID in (1, 3):
        #windows is funky of course
        platEncID = 1 if platID == 3 else 0
        langID = 1033 if platID == 3 else 0
        
        for i in newfields:
            t.getName(i, platID, platEncID, langID, True).string = 'Cake'
        
    t.save(tempfh)
    tempfh.close()
    
    new_t = TTNameTable(tempfn)
    
    for i in newfields:
        assert new_t.getName(i, 1, 0, 0).string == 'Cake'
        
    os.unlink(tempfn)
    