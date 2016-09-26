# -*- coding:utf-8 -*-
#
# Copyright 2014 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging

from bandit.core import utils

logger = logging.getLogger(__name__)


def checks(*args):
    '''Decorator function to set checks to be run.'''
    def wrapper(func):
        if not hasattr(func, "_checks"):
            func._checks = []
        func._checks.extend(utils.check_ast_node(a) for a in args)

        logger.debug('checks() decorator executed')
        logger.debug('  func._checks: %s', func._checks)
        return func
    return wrapper


def takes_config(*args):
    '''Test function takes config

    Use of this delegate before a test function indicates that it should be
    passed data from the config file. Passing a name parameter allows
    aliasing tests and thus sharing config options.
    '''
    name = ""

    def _takes_config(func):
        if not hasattr(func, "_takes_config"):
            func._takes_config = name
        return func

    if len(args) == 1 and callable(args[0]):
        name = args[0].__name__
        return _takes_config(args[0])
    else:
        name = args[0]
        return _takes_config


def test_id(id_val):
    '''Test function identifier

    Use this decorator before a test function indicates its simple ID
    '''
    def _has_id(func):
        if not hasattr(func, "_test_id"):
            func._test_id = id_val
        return func
    return _has_id


def accepts_baseline(*args):
    """Decorator to indicate formatter accepts baseline results

    Use of this decorator before a formatter indicates that it is able to deal
    with baseline results.  Specifically this means it has a way to display
    candidate results and know when it should do so.
    """
    def wrapper(func):
        if not hasattr(func, '_accepts_baseline'):
            func._accepts_baseline = True

        logger.debug('accepts_baseline() decorator executed on %s',
                     func.__name__)

        return func
    return wrapper(args[0])
