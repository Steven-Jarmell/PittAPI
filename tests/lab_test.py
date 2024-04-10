"""
The Pitt API, to access workable data of the University of Pittsburgh
Copyright (C) 2015 Ritwik Gupta

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import unittest
import responses

from pittapi import lab
from tests.mocks.lab_mocks import mock_all_ids_data


class LabTest(unittest.TestCase):
    @responses.activate
    def test_get_all_lab_ids(self):
        responses.add(
            responses.GET,
            lab.PITT_BASE_URL + "avail.json",
            json=mock_all_ids_data,
            status=200,
        )
        
        results = lab._fetch_all_lab_ids()
        self.assertIsInstance(results, list)

        EXPECTED_LIST = [
            "bba4a8796295ff6a8df116524b40e178",
            "98a4759fc02ca3655d56cd58abed4e90",
            "8adaaeb974aa38b2283c73532c095ca7",
            "6fd5a4e0dd0a32e3ccb441e25a1a2d78",
            "25d1bfa80cafb622994b7d06c63011f2",
            "04853e8d1453c90a910a0b803529a3a0",
        ]
        self.assertListEqual(results, EXPECTED_LIST, "List of Lab Ids did not match")
