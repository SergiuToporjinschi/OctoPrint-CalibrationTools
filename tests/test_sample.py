# -*- coding: utf-8 -*-
import logging
import unittest
from distutils.log import debug
from unittest.mock import patch

from octoprint_CalibrationTools import EStepsApi

# import mock


class test_sample(unittest.TestCase):
    def fakeDebug(self):
        pass

    def test_somethingPassing(self):
        x = EStepsApi.API()
        x._logger = logging
        with patch('EStepsApi.API._printer') as m_printer:
            inst = m_printer.return_value
            inst._printer.return_value = "test"
            x.apiGateWay("eSteps_load","")
        # self.assertEqual(, True)

