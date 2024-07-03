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
import pytest

from pittapi import lab
import tests.mocks.lab_mocks as lab_mocks


def create_test_url(lab_name: str) -> str:
    return lab.PITT_BASE_URL + lab.AVAIL_LAB_ID_MAP[lab_name] + "/status.json?noredir=1"


class LabTest(unittest.TestCase):
    @responses.activate
    def test_get_status_bellefield(self):
        responses.add(
            responses.GET,
            create_test_url("BELLEFIELD"),
            json=lab_mocks.mocked_bellefield_data,
        )

        results = lab.get_one_lab_data("BELLEFIELD")

        self.assertIsInstance(results, lab.Lab)

        self.assertEqual(results.name, "Bellefield 314")
        self.assertEqual(results.status, False)
        self.assertEqual(results.available_computers, 29)
        self.assertEqual(results.off_computers, 1)
        self.assertEqual(results.in_use_computers, 0)
        self.assertEqual(results.out_of_service_computers, 0)
        self.assertEqual(results.total_computers, 30)

    @responses.activate
    def test_get_status_lawrence(self):
        responses.add(
            responses.GET,
            create_test_url("LAWRENCE"),
            json=lab_mocks.mocked_lawrence_data,
        )

        results = lab.get_one_lab_data("LAWRENCE")

        self.assertIsInstance(results, lab.Lab)

        self.assertEqual(results.name, "David Lawrence 230")
        self.assertEqual(results.status, False)
        self.assertEqual(results.available_computers, 25)
        self.assertEqual(results.off_computers, 10)
        self.assertEqual(results.in_use_computers, 5)
        self.assertEqual(results.out_of_service_computers, 0)
        self.assertEqual(results.total_computers, 40)

    @responses.activate
    def test_get_status_sutherland(self):
        responses.add(
            responses.GET,
            create_test_url("SUTH"),
            json=lab_mocks.mocked_sutherland_data,
        )

        results = lab.get_one_lab_data("SUTH")

        self.assertIsInstance(results, lab.Lab)

        self.assertEqual(results.name, "Sutherland 120")
        self.assertEqual(results.status, False)
        self.assertEqual(results.available_computers, 11)
        self.assertEqual(results.off_computers, 1)
        self.assertEqual(results.in_use_computers, 0)
        self.assertEqual(results.out_of_service_computers, 0)
        self.assertEqual(results.total_computers, 12)

    @responses.activate
    def test_get_status_cathg27(self):
        responses.add(
            responses.GET,
            create_test_url("CATH_G27"),
            json=lab_mocks.mocked_cathy_g27_data,
        )

        results = lab.get_one_lab_data("CATH_G27")

        self.assertIsInstance(results, lab.Lab)

        self.assertEqual(results.name, "Cathedral G27")
        self.assertEqual(results.status, False)
        self.assertEqual(results.available_computers, 16)
        self.assertEqual(results.off_computers, 3)
        self.assertEqual(results.in_use_computers, 11)
        self.assertEqual(results.out_of_service_computers, 0)
        self.assertEqual(results.total_computers, 30)

    @responses.activate
    def test_get_status_cathg62(self):
        responses.add(
            responses.GET,
            create_test_url("CATH_G62"),
            json=lab_mocks.mocked_cathy_g62_data,
        )

        results = lab.get_one_lab_data("CATH_G62")

        self.assertIsInstance(results, lab.Lab)

        self.assertEqual(results.name, "Cathedral G62")
        self.assertEqual(results.status, False)
        self.assertEqual(results.available_computers, 26)
        self.assertEqual(results.off_computers, 5)
        self.assertEqual(results.in_use_computers, 0)
        self.assertEqual(results.out_of_service_computers, 0)
        self.assertEqual(results.total_computers, 31)

    @responses.activate
    def test_get_status_benedum(self):
        responses.add(
            responses.GET,
            create_test_url("BENEDUM"),
            json=lab_mocks.mocked_benedum_data,
        )

        results = lab.get_one_lab_data("BENEDUM")

        self.assertIsInstance(results, lab.Lab)

        self.assertEqual(results.name, "Benedum B06")
        self.assertEqual(results.status, False)
        self.assertEqual(results.available_computers, 28)
        self.assertEqual(results.off_computers, 7)
        self.assertEqual(results.in_use_computers, 4)
        self.assertEqual(results.out_of_service_computers, 0)
        self.assertEqual(results.total_computers, 39)

    @responses.activate
    def test_get_all_lab_data(self):
        responses.add(
            responses.GET,
            create_test_url("BELLEFIELD"),
            json=lab_mocks.mocked_bellefield_data,
        )
        responses.add(
            responses.GET,
            create_test_url("LAWRENCE"),
            json=lab_mocks.mocked_lawrence_data,
        )
        responses.add(
            responses.GET,
            create_test_url("SUTH"),
            json=lab_mocks.mocked_sutherland_data,
        )
        responses.add(
            responses.GET,
            create_test_url("CATH_G27"),
            json=lab_mocks.mocked_cathy_g27_data,
        )
        responses.add(
            responses.GET,
            create_test_url("CATH_G62"),
            json=lab_mocks.mocked_cathy_g62_data,
        )
        responses.add(
            responses.GET,
            create_test_url("BENEDUM"),
            json=lab_mocks.mocked_benedum_data,
        )

        results = lab.get_all_labs_data()

        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 6)

        for item in results:
            self.assertIsInstance(item, lab.Lab)

    def test_invalid_lab_name(self):
        with pytest.raises(
            ValueError,
            match="Invalid lab name: INVALID. Valid options: BELLEFIELD, LAWRENCE, SUTH, CATH_G27, CATH_G62, BENEDUM",
        ):
            lab.get_one_lab_data("INVALID")

    @responses.activate
    def test_handle_invalid_lab_id(self):
        responses.add(
            responses.GET,
            create_test_url("CATH_G27"),
            body="Resource not found",
            status=404,
        )

        with pytest.raises(
            lab.LabAPIError,
            match="The Lab ID was invalid. Please open a GitHub issue so we can resolve this.",
        ):
            lab.get_one_lab_data("CATH_G27")

    @responses.activate
    def test_handle_unexpected_fetch_err(self):
        responses.add(
            responses.GET,
            create_test_url("CATH_G27"),
            body="Unauthorized",
            status=401,
        )

        with pytest.raises(
            lab.LabAPIError,
            match="An unexpected error occurred while fetching lab data: Unauthorized",
        ):
            lab.get_one_lab_data("CATH_G27")
