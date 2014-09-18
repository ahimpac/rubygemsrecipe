#!/usr/bin/env python

import re
import os.path
import logging
import subprocess


def sh(cmd):
    retcode = subprocess.call(cmd, shell=True)
    assert retcode == 0

def shr(cmd):
    return subprocess.check_output(cmd, shell=True)


def clean():
    logging.info('Cleaning environment...')
    paths = (
        '.installed.cfg',
        'bin',
        'bootstrap.py',
        'develop-eggs',
        'include',
        'lib',
        'local',
        'parts',
    )
    for path in paths:
        if os.path.exists(path):
            sh('rm -r %s' % path)


def main():
    logging.basicConfig(
        format='%(message)s',
        level=logging.INFO
    )
    clean()
    sh('wget http://downloads.buildout.org/2/bootstrap.py')
    sh('virtualenv --no-site-packages .')
    sh('bin/pip install --upgrade setuptools')
    sh('bin/python bootstrap.py')
    sh('bin/buildout')
    assert re.match(
        r'^Sass \d+(\.\d+){2} \([a-zA-Z ]+\)$',
        shr('bin/sass --version').strip()
    )



if __name__ == '__main__':
    main()
