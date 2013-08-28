"""
objects representing the font metadata "name" table and its Records
"""

# Once upon a time, this file used the TTFont API to all the editing.  And it
# works great for reading, but when you call save() all you get is garbage out.
# Rather than try and figure out what the hell is wrong with that, we just do
# the XML serialization dance, since that code path seems to have been well used
# for at least a decade.

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

from StringIO import StringIO
from fontTools.ttLib import TTFont
import fontTools.ttLib.xmlImport
import collections
import tempfile
import sys
import os

#use lxml for a speed boost if we have it
try:
    import lxml.etree as etree
except ImportError: #pragma: no cover
    import xml.etree.ElementTree as etree

# EVIL MONKEYPATCH HACKS

# everything in TTFont takes a file object but the XML reader.  fml.
def _parse(self):
    if hasattr(self.fileName, 'read'):
        self.parseFile(self.fileName)
    #this never gets used, it's just to be exceedingly correct
    else:   #pragma: no cover
        self.parseFile(open(fileName))

fontTools.ttLib.xmlImport.ExpatParser.parse = _parse

class StrungIO(StringIO):
    "A special StringIO that ignores ttx's foolish close operations"
    def close(self):
        self.seek(0)
    
    def free(self):
        StringIO.close(self)

# and now the normal stuff...

SectionData = collections.namedtuple('SectionData', ['platformID', 'platEncID', 'langID'])

class TTNameRecord(object):
    "An object representing a name record that mimics those returned by TTFont"
    #...so I don't have to rewrite cli.py  ;-)
    def __init__(self, *args):
        if len(args) == 1:
            self._elem = args[0]
        elif len(args) == 5:
            parent, nameID, platformID, platEncID, langID = args
            self._elem = elem = etree.SubElement(parent, 'namerecord')
    
            self.nameID = nameID
            self.platformID = platformID
            self.platEncID = platEncID
            self.langID = langID
        else:
            raise TypeError('either 1 or 5 arguments expected')
        
    def __getattr__(self, name):
        if name == 'langID':
            return int(self._elem.get(name), 16)
        elif name in self._elem.keys():
            return int(self._elem.get(name))
        elif name == 'string':
            return self._elem.text.strip()
        else:
            raise AttributeError
    
    def __setattr__(self, name, value):
        if name == '_elem': #chicken, meet egg
            object.__setattr__(self, name, value)
        elif name == 'langID':
            self._elem.set(name, hex(value))
        elif name in ['nameID', 'platformID', 'platEncID']:
            self._elem.set(name, str(value))
        elif name == 'string':
            self._elem.text = value
        else:
            object.__setattr__(self, name, value)

class TTNameTable(object):
    'The "name" table of an OpenType font, containing metadata regarding the font'
    def __init__(self, fileish):
        self._infile = fileish
        self._xml = StrungIO()
    
        #grrrrrrrr
        stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        tt = TTFont(fileish)
        tt.saveXML(self._xml, tables=['name'], progress=False)
        sys.stdout = stdout
        
        self._xml.seek(0)
        self._tree = etree.parse(self._xml)
        self._name = self._tree.getroot().find('name')
    
    def __del__(self):
        self._xml.free()
    
    # yet more compat fun
    @property
    def names(self):
        for elem in self._name:
            yield TTNameRecord(elem)
    
    def save(self, fileish):
        new_xml = StrungIO()
        self._tree.write(new_xml)
        new_xml.seek(0)
        
        stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        self._font = TTFont(self._infile)
        self._font.importXML(new_xml, progress=False)
        self._font.save(fileish)
        sys.stdout = stdout
        
        new_xml.free()
    
    # I hate camelcased function names, but that's what TTFont uses :-(
    def getName(self, nameID, platformID, platEncID, langID, write=False):
        for n in self.names:
            if n.nameID == nameID and n.platformID == platformID and \
                        n.platEncID == platEncID and n.langID == langID:
                return n
        
        if write:
            new = TTNameRecord(self._name, nameID, platformID, platEncID, langID)
            return new
        else:
            return None
        
    def getSection(self, platformID, platEncID, langID):
        for n in self.names:
            if platformID == n.platformID and platEncID == n.platEncID and langID == n.langID:
                yield n
    
    def getNameFromAll(self, nameID):
        for n in self.names:
            if nameID == n.nameID:
                yield n
    
    def getNamesBySection(self):
        """returns a mapping of names keyed by section information"""
        result = {}
        
        for n in self.names:
            sd = SectionData(n.platformID, n.platEncID, n.langID)
            
            if sd not in result.iterkeys():
                result[sd] = []
                
            result[sd].append(n)
            
        return result
    