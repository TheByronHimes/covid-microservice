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
#

import pytest
from pydantic import EmailStr

from cm.core import models

from .fixtures.utils import VALID_DATE_STRING, VALID_EMAIL, VALID_NAME, Parametrizer

# When testing inheritance, this can be used
prepared_sample_creation = models.SampleCreation(
    patient_pseudonym=VALID_NAME,
    submitter_email=EmailStr(VALID_EMAIL),
    collection_date=VALID_DATE_STRING,
)


def test_sample_full_creation_simple():
    """Simple SampleFullCreation instantiation, should work every time"""
    models.SampleFullCreation(**prepared_sample_creation.dict())


@pytest.mark.parametrize(
    "status",
    [
        ("pending"),
        ("completed"),
        ("failed"),
        pytest.param("super", marks=pytest.mark.xfail),
        pytest.param("", marks=pytest.mark.xfail),
    ],
)
def test_sample_full_creation(status):
    """Test matrix of status"""
    models.SampleFullCreation(
        **prepared_sample_creation.dict(),
        status=status,
    )


@pytest.mark.parametrize(
    "test_result",
    [
        ("inconclusive"),
        ("positive"),
        ("negative"),
        pytest.param("banana", marks=pytest.mark.xfail),
        pytest.param("", marks=pytest.mark.xfail),
    ],
)
def test_sample_full_creation_result(test_result):
    """Test values for test_result"""
    models.SampleFullCreation(
        **prepared_sample_creation.dict(),
        test_result=test_result,
    )


@pytest.mark.parametrize("test_date", Parametrizer.make_date_string_test_params())
def test_sample_full_creation_date(test_date):
    """Test what kinds of strings are allowed for the test_date field"""
    models.SampleFullCreation(**prepared_sample_creation.dict(), test_date=test_date)
