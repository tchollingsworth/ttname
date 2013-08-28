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

from nose.tools import assert_raises, assert_raises_regexp
import os
import random
import shutil
import sys
import tempfile

from ttname import TTNameTable
from ttname.cli import TTNameCLI, TTNameCLIError

_testfile = os.path.join(os.path.dirname(__file__), 'data/DejaVuSans.ttf')

def test_simple_read():
    TTNameCLI([_testfile])
    
def test_all_read():
    TTNameCLI(['-a', _testfile])
    
def test_single_read():
    TTNameCLI(['-n', 'name', _testfile])
    
def test_single_all_read():
    TTNameCLI(['-an', 'copyright', _testfile])
    
def test_stdin_read():
    stdin = sys.stdin
    sys.stdin = open(_testfile)
    
    TTNameCLI(['-'])
    
    sys.stdin.close()
    sys.stdin = stdin
    
def test_simple_write():
    tempfn = tempfile.mktemp(prefix='ttname-test-cli-simple-write-', suffix='.ttf')
    
    TTNameCLI(['--copyright=foo', _testfile, tempfn])
    
    tt = TTNameTable(tempfn)
    print tt.getName(0,1,0,0).string == 'foo'
    
    os.unlink(tempfn)
    
def test_stdout_write():
    stdout = sys.stdout
    sys.stdout = tempfile.NamedTemporaryFile(prefix='ttname-test-cli-stdout-write-', suffix='.ttf', delete=False)
    tempfn = sys.stdout.name
    
    TTNameCLI(['--license-url=http://example.com/', _testfile, '-'])
    
    sys.stdout.close()
    sys.stdout = stdout
    
    tt = TTNameTable(tempfn)
    assert tt.getName(14,1,0,0).string == 'http://example.com/'
    
    os.unlink(tempfn)
    
def test_overwrite_write():
    tempfn = tempfile.mktemp(prefix='ttname-test-cli-overwrite-write-', suffix='.ttf')
    shutil.copy2(_testfile, tempfn)
    
    TTNameCLI(['--vendor-url=http://example.com/', tempfn])
    
    tt = TTNameTable(tempfn)
    assert tt.getName(11,1,0,0).string == 'http://example.com/'
    
    os.unlink(tempfn)

def test_all_write():
    tempfn = tempfile.mktemp(prefix='ttname-test-cli-all-write-', suffix='.ttf')
    
    TTNameCLI(['--license=bar', '-a', _testfile, tempfn])
    
    tt = TTNameTable(tempfn)
    assert tt.getName(13,3,1,1033).string == 'bar'
    
    os.unlink(tempfn)
    
def test_numeric_write():
    tempfn = tempfile.mktemp(prefix='ttname-test-cli-numeric-write-', suffix='.ttf')
    
    TTNameCLI(['--name150=bat', _testfile, tempfn])
    
    tt = TTNameTable(tempfn)
    assert tt.getName(150,1,0,0).string == 'bat'
    
    os.unlink(tempfn)
    
def test_specific_write():
    tempfn = tempfile.mktemp(prefix='ttname-test-cli-specific-write-', suffix='.ttf')
    
    TTNameCLI(['--name75=baz', '--platform=3', '--encoding=1', '--lang=1033', _testfile, tempfn])
    
    tt = TTNameTable(tempfn)
    assert tt.getName(75,3,1,1033).string == 'baz'
    
    os.unlink(tempfn)
    
def test_short_platform_name_write():
    tempfn = tempfile.mktemp(prefix='ttname-test-cli-specific-write-', suffix='.ttf')
    
    TTNameCLI(['--name75=baz', '--platform=windows', '--encoding=1', '--lang=1033', _testfile, tempfn])
    
    tt = TTNameTable(tempfn)
    assert tt.getName(75,3,1,1033).string == 'baz'
    
    os.unlink(tempfn)
    
def test_multiple_write():
    tempfn = tempfile.mktemp(prefix='ttname-test-cli-multiple-write-', suffix='.ttf')
    
    TTNameCLI(['--copyright=herp', '--name75=derp', _testfile, tempfn])
    
    tt = TTNameTable(tempfn)
    assert tt.getName(0,1,0,0).string == 'herp'
    assert tt.getName(75,1,0,0).string == 'derp'
    
    os.unlink(tempfn)

def test_error_exits():
    stderr = sys.stderr
    sys.stderr = open(os.devnull, 'w')
    assert_raises(SystemExit, TTNameCLI, ['/this/file/does/not/exist'])
    sys.stderr = stderr

def test_error_nonexist():
    assert_raises_regexp(TTNameCLIError, 'No such file or directory',
                         TTNameCLI, ['/this/file/does/not/exist'], False)
    
def test_error_badfile():
    tempfh = tempfile.NamedTemporaryFile(prefix='ttname-test-cli-error-badfile-', suffix='.ttf', delete=False)
    tempfn = tempfh.name
    tempfh.write(os.urandom(1024*1024))
    tempfh.close()
    
    assert_raises_regexp(TTNameCLIError, 'Not a TrueType or OpenType font',
                         TTNameCLI, [tempfn], False)
    
    os.unlink(tempfn)

def test_error_bad_platform():
    assert_raises_regexp(TTNameCLIError, 'Invalid platform',
                         TTNameCLI, ['--platform=potato', _testfile], False)
    
def test_error_bad_name():
    assert_raises_regexp(TTNameCLIError, 'Invalid name',
                         TTNameCLI, ['--record=potato', _testfile], False)

def test_error_bad_outfile():
    assert_raises_regexp(TTNameCLIError, 'Unable to open output file',
        TTNameCLI, ['--designer=foo', _testfile, '/dev/readonly/nope'], False)
    
def test_error_overwrite():
    tempdir = tempfile.mkdtemp(prefix='ttname-test-error-overwrite-')
    tempfn = os.path.join(tempdir, 'DejaVuSans.ttf')
    shutil.copy2(_testfile, tempfn)
    os.chmod(tempdir, 0550)
    os.chmod(tempfn, 0660)
    
    assert_raises_regexp(TTNameCLIError, 'Unable to replace',
                         TTNameCLI, ['--designer-url=foo', tempfn], False)
    
    os.chmod(tempdir, 0770)
    os.chmod(tempfn, 0660)
    os.unlink(tempfn)
    os.rmdir(tempdir)
    