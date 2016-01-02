#!/usr/bin/env python
#  vim:ts=4:sts=4:sw=4:et
#
#  Author: Hari Sekhon
#  Date: 2015-12-22 23:25:25 +0000 (Tue, 22 Dec 2015)
#
#  https://github.com/harisekhon/pytools
#
#  License: see accompanying Hari Sekhon LICENSE file
#
#  If you're using my code you're welcome to connect with me on LinkedIn and optionally send me feedback to help improve or steer this or other code I publish
#
#  http://www.linkedin.com/in/harisekhon
#

"""

XML Validator Tool

Validates each file passed as an argument

Directories are recursed, checking all files ending in a .xml suffix.

Works like a standard unix filter program - if no files are passed as arguments or '-' is passed then reads from standard input

"""

# Forked from validate_yaml.py

from __future__ import print_function

__author__  = 'Hari Sekhon'
__version__ = '0.4'

import os
import re
import sys
import traceback
sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])) + '/pylib')
try:
    from harisekhon.utils import *
    from harisekhon import CLI
except ImportError, e:
    print('module import failed: %s' % e, file=sys.stderr)
    sys.exit(4)


class XmlValidatorTool(CLI):

    RE_XML_SUFFIX = re.compile('.*\.xml', re.I)

    def check_xml(self, content):
        if isXml(content):
            print(self.valid_xml_msg)
        else:
            # TODO: change this to use a getter
            if self.options.verbose > 2:
                try:
                    ET.fromstring(content)
                # Python 2.7 throws xml.etree.ElementTree.ParseError, but Python 2.6 throws xml.parsers.expat.ExpatError
                except Exception, e:
                    print(e)
            die(self.invalid_xml_msg)

    def run(self):
        if not self.args:
            self.args.append('-')
        for arg in self.args:
            if arg == '-':
                continue
            if not os.path.exists(arg):
                print("'%s' not found" % arg)
                sys.exit(ERRORS['WARNING'])
            if os.path.isfile(arg):
                vlog_option('file', arg)
            elif os.path.isdir(arg):
                vlog_option('directory', arg)
            else:
                die("path '%s' could not be determined as either a file or directory" % arg)
        for arg in self.args:
            self.check_path(arg)

    def check_path(self, path):
        if path == '-' or os.path.isfile(path):
            self.check_file(path)
        elif os.path.isdir(path):
            for item in os.listdir(path):
                subpath = os.path.join(path, item)
                if os.path.isdir(subpath):
                    self.check_path(subpath)
                if not self.RE_XML_SUFFIX.match(item):
                    continue
                self.check_file(subpath)
        else:
            die("failed to determine if path '%s' is file or directory" % path)

    def check_file(self, filename):
        if filename == '-':
            filename = '<STDIN>'
        self.valid_xml_msg   = '%s => XML OK'      % filename
        self.invalid_xml_msg = '%s => XML INVALID' % filename
        if filename == '<STDIN>':
            self.check_xml(sys.stdin.read())
        else:
            with open(filename) as self.f:
                self.check_xml(self.f.read())


if __name__ == '__main__':
    XmlValidatorTool().main()