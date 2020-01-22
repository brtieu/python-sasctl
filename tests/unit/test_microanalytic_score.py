#!/usr/bin/env python
# encoding: utf-8
#
# Copyright © 2019, SAS Institute Inc., Cary, NC, USA.  All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import pytest
from six.moves import mock

from sasctl.services import microanalytic_score as mas

from sasctl import current_session
from sasctl.core import RestObj

with mock.patch('sasctl.core.requests.Session.request'):
    current_session('example.com', 'username', 'password')


def test_create_python_module():
    with mock.patch('sasctl.services.microanalytic_score.post') as post:
        with pytest.raises(ValueError):
            mas.create_module()     # Source code is required

    with mock.patch('sasctl.services.microanalytic_score.post') as post:
        source = '\n'.join(("def testMethod(var1, var2):",
                            "    'Output: out1, out2'",
                            "    out1 = var1 + 5",
                            "    out2 = var2.upper()",
                            "    return out1, out2"))
        mas.create_module(source=source)

        assert post.call_count == 1
        json = post.call_args[1].get('json', {})
        assert 'text/x-python' == json['type']
        assert 'public' == json['scope']


def test_delete_module(caplog):
    import logging
    caplog.set_level(logging.INFO, 'sasctl._services.service')

    # Delete should succeed even if object couldn't be found on server
    with mock.patch('sasctl._services.microanalytic_score.MicroAnalyticScore'
                    '.get') as get:
        get.return_value = None

        assert mas.delete_module('spam') is None
        assert any("Object 'spam' not found" in r.msg for r in caplog.records)


def test_define_steps():

    # Mock module to be returned
    module = RestObj(name='unittestmodule',
                     id='unittestmodule',
                     stepIds=['step1', 'step2'])

    # Mock module step with no inputs
    step1 = RestObj(id='post')

    # Mock module step with multiple inputs
    step2 = RestObj({
        "id": "score",
        "inputs": [
            {
                "name": "age",
                "type": "decimal",
                "dim": 0,
                "size": 0
            },
            {
                "name": "b",
                "type": "decimal",
                "dim": 0,
                "size": 0
            },
            {
                "name": "chas",
                "type": "decimal",
                "dim": 0,
                "size": 0
            },
            {
                "name": "crim",
                "type": "decimal",
                "dim": 0,
                "size": 0
            },
            {
                "name": "dis",
                "type": "decimal",
                "dim": 0,
                "size": 0
            },
            {
                "name": "indus",
                "type": "decimal",
                "dim": 0,
                "size": 0
            },
            {
                "name": "lstat",
                "type": "decimal",
                "dim": 0,
                "size": 0
            },
            {
                "name": "nox",
                "type": "decimal",
                "dim": 0,
                "size": 0
            },
            {
                "name": "ptratio",
                "type": "decimal",
                "dim": 0,
                "size": 0
            },
            {
                "name": "rad",
                "type": "decimal",
                "dim": 0,
                "size": 0
            },
            {
                "name": "rm",
                "type": "decimal",
                "dim": 0,
                "size": 0
            },
            {
                "name": "tax",
                "type": "decimal",
                "dim": 0,
                "size": 0
            },
            {
                "name": "zn",
                "type": "decimal",
                "dim": 0,
                "size": 0
            }
        ],
        "outputs": [
            {
                "name": "em_prediction",
                "type": "decimal",
                "dim": 0,
                "size": 0
            },
            {
                "name": "p_price",
                "type": "decimal",
                "dim": 0,
                "size": 0
            },
            {
                "name": "_warn_",
                "type": "string",
                "dim": 0,
                "size": 4
            }
        ]
    })

    with mock.patch('sasctl._services.microanalytic_score.MicroAnalyticScore.get_module') as get_module:
        with mock.patch('sasctl._services.microanalytic_score.MicroAnalyticScore''.get_module_step') as get_step:
            get_module.return_value = module
            get_step.side_effect = [step1, step2]
            result = mas.define_steps(None)

    for step in get_step.side_effect:
        assert hasattr(result, step.id)
