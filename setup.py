#!/usr/bin/python

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

from setuptools import setup
from distutils.errors import DistutilsError
from setuptools.command import sdist, install
import os
import subprocess

# EVIL MONKEYPATCH HACKS

#always rebuild the man page during sdist
_orig_sdist_run = sdist.sdist.run

def _new_sdist_run(self):
    try:
        subprocess.call(['pandoc', '-s', '-w', 'man', 'ttname.1.md', '-o', 'ttname.1'])
    except OSError:
        raise DistutilsError('unable to find pandoc comamnd to build man page')
    except subprocess.CalledProcessError:
        raise DistutilsError('pandoc exited with an error')
    
    _orig_sdist_run(self)
    
sdist.sdist.run = _new_sdist_run

# setuptools/distutils doesn't know how to install man pages?  REALLY??
_orig_install_run = install.install.run

def _new_install_run(self):
    _orig_install_run(self)
    
    if os.name == 'posix':
        manpath = os.path.join(self.root, self.install_data, 'share', 'man', 'man1')
        self.mkpath(manpath)
        self.copy_file('ttname.1', manpath)
        
install.install.run = _new_install_run

# and now the normal stuff...

setup(
    name='ttname',
    version='1',
    description='CLI font metadata editor',
    license='BSD',
    author='T.C. Hollingsworth',
    author_email='tchollingsworth@gmail.com',
    url='https://github.com/tchollingsworth/ttname',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Text Processing :: Fonts',
    ],
    
    packages=['ttname'],
    setup_requires=['nose'],
    test_suite='nose.collector',
    include_package_data=True,
    entry_points = {
        'console_scripts': [
            'ttname = ttname.cli:TTNameCLI'
        ]
    }
)

    