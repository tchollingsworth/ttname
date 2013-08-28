% TTNAME(1)
% 
% August 25, 2013

# NAME

**ttname** - CLI font metadata editor

# SYNOPSIS

**ttname** *[options]* *input_file* [*output_file*]

# DESCRIPTION

ttname provides a simple CLI interface to edit the **name** table in TrueType or
OpenType fonts, which contains metadata regarding the font.  It uses the the
same library underlying the venerable **ttx(1)** utility to do it's work.

# OPTIONS

## UNIVERSAL OPTIONS

These options are valid regardless of whether you are using **ttname** to read 
or  write to font files.

*input_file*
:   The path to a OpenType of TrueType file

-a, \--all
:   Operate on all platform/encoding/language combinations.  By default, ttname
    will only operate on the first combination found.  You probably want to use
    this option when writing.
    
-p, \--platform
:   Specifies the OpenType platform ID number to operate on.  You can provide
    the numeric ID or use one of the following short names:
    
    -------------   ------------------
    **unicode**     for platform ID #0
    **iso**         for platform ID #1
    **macintosh**   for platform ID #2
    **windows**     for platform ID #3
    **custom**      for platform ID #4
    -------------   ------------------
    
-e, \--encoding
:   Specifies the OpenType platform encoding ID number to operate on.

-l, \--lang
:   Specifies the OpenType language encoding ID number to operate on.

## READ OPTIONS

The following option is only valid when you are using *ttname* to read the
metadata from 

-n *{nameID}*, \--record=*{nameID}*
:   Specifies the OpenType name ID number to return on the standard output.  In
    addition to using the numeric form, you can also pass one of the short names
    listed below in *WRITE OPTIONS*.
    
## WRITE OPTIONS

These options are only valid when *ttname* is used to write new metadata to
font files.

\--name*{nameID}*=*{DATA}\*
:   Updates the OpenType name ID number *{nameID}* with the provided *{DATA}*.  
    If the record does not exist, it will be created.  If *-a* is provided on
    the command line, the same name ID will be updated for all 
    platform/encoding/language combinations that exist in the file.  Otherwise,
    the specified or default platform/encoding/language are used.
    
In addition to using the numeric form as above, *ttname* also supports textual
options for the well known name ID numbers, which range from 0-.  Using any of the following is
equivalent to passing the numeric form as above.

\--copyright
:   Updates name id **#0**, which contains the **copyright notice**.

\--family
:   Updates name id **#1**, which contains the **font family name**.

\--subfamily
:   Updates name id **#2**, which contains the **font subfamily name**.

\--id
:   Updates name id **#3**, which contains a **unique font identifier**.

\--name
:   Updates name id **#4**, which contains the **full font name**.

\--version
:   Updates name id **#5**, which contains a **version string**.

\--ps-name
:   Updates name id **#6**, which contains the **PostScript name**.

\--trademark
:   Updates name id **#7**, which contains **trademark information**.

\--mfg-name
:   Updates name id **#8**, which contains the **manufacturer name**.

\--designer
:   Updates name id **#9**, which contains the **designer name**.

\--desc
:   Updates name id **#10**, which contains a **description of the font**.

\--vendor-url
:   Updates name id **#11**, which contains the **URL of the font vendor**.

\--designer-url
:   Updates name id **#12**, which contains the **URL of the font designer**.

\--license
:   Updates name id **#13**, which contains a **license description**.

\--license-url
:   Updates name id **#14**, which contains the **license info URL**.

\--pref-family
:   Updates name id **#16**, which contains the **preferred family**.

\--pref-subfamily
:   Updates name id **#17**, which contains the **preferred subfamily**.

\--compat-full
:   Updates name id **#18**, which contains a **compatible full name**.  Used only
    by the Macintosh platform (platform ID #1).

\--sample
:   Updates name id **#19**, which contains **sample text**.

\--ps-cid-findfont-name
:   Updates name id **#20**, which contains the **PostScript CID findfont name**.

\--wws-family
:   Updates name id **#21**, which contains the **WWS family name**.

\--wws-subfamily
:   Updates name id **#22**, which contains the **WWS subfamily name**.

# EXAMPLES

Display the name records from the first platform/encoding/language combination
present in the font file:

    ttname font.ttf

Display all name records in the font file:

    ttname -a font.ttf

Display only the first copyright record in the font file:

    ttname --record=copyright font.ttf
    
or use the number, if you don't know the name:

    ttname -n0 font.ttf
    
Change the font designer's URL:

    ttname --designer-url='http://www.example.com/' font.ttf
    
Again, you can use the number, which is useful for weird names:

    ttname --name12='http://www.example.com/' font.ttf
    
# SEE ALSO

* **ttx(1)**
* **fc-query(1)**
* Microsoft's documentation of the name table

    <https://www.microsoft.com/typography/otspec/name.htm>

* Apple's documentation of the name table

    <https://developer.apple.com/fonts/TTRefMan/RM06/Chap6name.html>
    
* ISO/IEC 14496-22:2009
    
# BUGS

In the likely event that you encounter a bug, you can report it at:

    <https://github.com/tchollingsworth/ttname/issues>
    
or contact the author listed below.
    
# AUTHOR

T.C.\ Hollingsworth\
<tchollingsworth@gmail.com>

# COPYRIGHT

ttname is distributed under the simplified 2-clause BSD license.

Copyright 2013 T.C.\ Hollingsworth\  <tchollingsworth@gmail.com>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
