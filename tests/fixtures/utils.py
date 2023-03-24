# Copyright 2021 - 2023 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
# for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Includes a Parametrizer class which can provide date and email
string parameters for testing"""


from pathlib import Path

import pytest

BASE_DIR = Path(__file__).parent.resolve()

VALID_EMAIL = "test@test.com"
VALID_DATE_STRING = "2023-01-15T11:18"
VALID_NAME = "Jonathan K."


class Parametrizer:
    """Hosts static methods to assist in test creation."""

    @staticmethod
    def make_date_string_test_params() -> list:
        """Returns a list of valid and invalid pytest test parameters"""
        params = [
            (VALID_DATE_STRING),  # all okay
            ("2023-01-15T11:18Z"),  # okay, Z accepted
            ("2023-01-15T11:18z"),  # okay, little z accepted too
            pytest.param(
                "2023-01-15T11:18.4", marks=pytest.mark.xfail
            ),  # invalid, nothing sub-minute
            pytest.param("22-01-15T11:18", marks=pytest.mark.xfail),  # invalid year
            pytest.param(
                "2023-1-15T11:18", marks=pytest.mark.xfail
            ),  # invalid month format
            pytest.param(
                "2023-01-5T11:18", marks=pytest.mark.xfail
            ),  # invalid day format
            pytest.param("2023-01-0511:18", marks=pytest.mark.xfail),  # no T
            pytest.param("2023-01-15t11:18", marks=pytest.mark.xfail),  # little t bad
        ]

        return params

    @staticmethod
    def make_email_string_test_params() -> list:
        """Returns a list of valid and invalid pytest test parameters for emails"""
        passes = [
            (VALID_EMAIL),  # all okay
        ]

        fail_cases = [
            "test.com",
            "test@test@test.com",
            "testtesttesttesttesttesttesttesttesttesttesttest\
            testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttest\
            testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttest\
            testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttest\
            testtesttest@test.com",
        ]

        fails = [pytest.param(fail, marks=pytest.mark.xfail) for fail in fail_cases]

        return passes + fails
