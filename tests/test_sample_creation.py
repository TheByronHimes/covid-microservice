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

"""Test module for testing the models and their validation settings"""
import pytest
from pydantic import EmailStr

from cm.core import models
from cm.core.utils import random_string

from .fixtures.utils import VALID_DATE_STRING, VALID_EMAIL, VALID_NAME, Parametrizer


@pytest.mark.parametrize(
    "patient_pseudonym",
    [
        (VALID_NAME),  # all okay
        pytest.param("Jonathan K", marks=pytest.mark.xfail),  # name too short
        pytest.param(random_string(64), marks=pytest.mark.xfail),  # name too long
    ],
)
def test_sample_creation_names(patient_pseudonym):
    """Test names parametrized for SampleCreation"""
    models.SampleCreation(
        patient_pseudonym=patient_pseudonym,
        submitter_email=EmailStr(VALID_EMAIL),
        collection_date=VALID_DATE_STRING,
    )


@pytest.mark.parametrize(
    "submitter_email", Parametrizer.make_email_string_test_params()
)
def test_sample_creation_email_addresses(submitter_email):
    """Verify that the email validation is working"""
    models.SampleCreation(
        patient_pseudonym=VALID_NAME,
        submitter_email=EmailStr(submitter_email),
        collection_date=VALID_DATE_STRING,
    )


@pytest.mark.parametrize(
    "collection_date",
    Parametrizer.make_date_string_test_params(),
)
def test_sample_creation_dates(collection_date):
    """Verify that the date string regex is working"""
    models.SampleCreation(
        patient_pseudonym=VALID_NAME,
        submitter_email=EmailStr(VALID_EMAIL),
        collection_date=collection_date,
    )
