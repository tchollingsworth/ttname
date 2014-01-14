"""
Provides a simple CLI interface for editing the "name" table of TrueType and
OpenType fonts, which contains metadata regarding the font.
"""

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

from fontTools.ttLib import TTLibError
import argparse
import collections
import os
import sys
import tempfile

from table import TTNameTable
import info

class TTNameCLI(object):
    def __init__(self, argv=sys.argv[1:], swallow_exceptions=True):
        try:
            self.parse_cmdline(argv)
        
            self.open()
        
            if self.newnames:
                self.write()
            else:
                self.read()
                
        except TTNameCLIError as e:
            #normally we'll just output an error and quit
            if swallow_exceptions:
                sys.stderr.write(e.message)
                sys.stderr.write('\n')
                sys.exit(1)
            #but sometimes we re-raise the error so the tests can see it more easily
            else:
                raise

    def parse_cmdline(self, argv):
        p = argparse.ArgumentParser(description=__doc__)
        
        #which files to operate on
        p.add_argument('infile', metavar='INFILE',
                       help='input file (use "-" for stdin)')
        p.add_argument('outfile', nargs='?', metavar='OUTFILE',
                       help='output file (use "-" for stdout)')

        #operate on all platform/encoding/language combinations simultaneously instead 
        #of a specific one
        p.add_argument('-a', '--all', action='store_true',
                    help='operate on all platform/encoding/language combinations '
                    'simultaneously')

        #which platform to operate on
        p.add_argument('-p', '--platform', default=None,
                            help='name or number specifiying the platform ID to '
                            'operate on (defaults to first in table)')

        #which platform specific encoding to operate on
        p.add_argument('-e', '--encoding', type=int, default=None,
                            help='the platform specific encoding ID to operate '
                            'on (defaults to first in table)')

        #which language ID to operate on
        p.add_argument('-l', '--lang', type=int, default=None,
                            help='which language ID to operate on (defaults to '
                            'first in table)')

        #for outputting, which name id to output
        p.add_argument('-n', '--record',
                    help='output a specific name instead of the whole list')
        
        #add numeric options for each permissible name id
        for i in xrange(0, 23768):
            p.add_argument('--name{0}'.format(i), 
                        default=argparse.SUPPRESS, help=argparse.SUPPRESS)

        #add stringed options for each permissible name id
        for name, number in info.names_short.iteritems():
            p.add_argument('--{0}'.format(name), dest='name{0}'.format(number),
                metavar='DATA', default=argparse.SUPPRESS, help=info.names[number])

        #phew
        self.args = p.parse_args(args=argv)

        #convert the ugly argparse list of name values to a nice dict
        self.newnames = {}
        for i in xrange(0, 23768):
            if 'name{0}'.format(i) in self.args:
                self.newnames[i] = self.args.__dict__['name{0}'.format(i)]
                        
    def open(self):
        #open the font
        try:
            if self.args.infile == '-':
                self.table = TTNameTable(sys.stdin)
            else:
                self.table = TTNameTable(self.args.infile)
        except IOError as e:
            raise TTNameCLIError('Unable to open input file "{0}": {1}'.format(
                self.args.infile, e.strerror))
        except TTLibError as e:
            raise TTNameCLIError('Unable to open font: {0}'.format(e.message))
        
        #resolve the platform/encoding/lang
        first = next(self.table.names)
        
        if self.args.platform is None:
            self.platform = first.platformID
        else:
            if self.args.platform.lower() in info.platforms_short:
                self.platform = info.platforms_short[self.args.platform.lower()]
            else:
                try:
                    self.platform = int(self.args.platform)
                except ValueError:
                    raise TTNameCLIError('Invalid platform: {0}\n'.format(self.args.platform))
        
        if self.args.encoding is None:
            self.encoding = first.platEncID
        else:
            self.encoding = self.args.encoding
        
        if self.args.lang is None:
            self.lang = first.langID
        else:
            self.lang = self.args.lang
    
    #FIXME: the output is fugly.  ideas for how to do it better are welcome
    def read(self):
        #outputting a single name
        if self.args.record is not None:
            if self.args.record in info.names_short:
                nameID = info.names_short[self.args.record]
            else:
                try:
                    nameID = int(self.args.record)
                except ValueError:
                    raise TTNameCLIError('Invalid name: {0}\n'.format(self.args.record))
            
            if self.args.all:
                names = self.table.getNameFromAll(nameID)
                for n in names:
                    print u'{0}: {1}'.format(info.trip(n), n.string)
                    
            else:
                print self.table.getName(nameID, self.platform, 
                                   self.encoding, self.lang)
                
        #outputting the whole table
        else:
            if self.args.all:
                for sd, names in self.table.getNamesBySection().iteritems():
                    print info.trip(names[0])
                    print '=' * len(info.trip(names[0]))
                    
                    for n in names:
                        print u'{0}: {1}'.format(info.name(n), n.string)
                            
                    print
            
            else:
                names = self.table.getSection(self.platform, self.encoding,
                                              self.lang)
                
                for n in names:
                    print u'{0}: {1}'.format(info.name(n), n.string)

    def write(self):
        if self.args.outfile is not None:
            if self.args.outfile == '-':
                outfile = sys.stdout
            else:
                try:
                    outfile = open(self.args.outfile, 'w')
                except IOError as e:
                    raise TTNameCLIError('Unable to open output file '
                        '"{0}": {1}'.format(self.args.infile, e.strerror))
                    
        else:
            try:
                outfile = tempfile.NamedTemporaryFile(dir=os.path.dirname(self.args.infile),
                        prefix=os.path.basename(self.args.infile), suffix='.ttname-tmp', delete=False)
                tempfn = outfile.name
            except OSError as e:
                raise TTNameCLIError('Unable to replace file')
        
        if self.args.all:
            for name, value in self.newnames.iteritems():
                for rec in self.table.getNameFromAll(name):
                    rec.string = value
        else:
            
            for name, value in self.newnames.iteritems():
                entry = self.table.getName(name, self.platform, self.encoding,
                                        self.lang, True)
                entry.string = value
                print entry.string
            
        self.table.save(outfile)
        outfile.close()
    
        if self.args.outfile is None:
            os.unlink(self.args.infile)
            os.rename(tempfn, self.args.infile)

class TTNameCLIError(Exception):
    pass
