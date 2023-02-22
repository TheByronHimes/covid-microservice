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

from covid_microservice.api.ancillary import make_sample_id
from covid_microservice.models import PcrTest


def test_with_all_valid_input():
    """Uses valid input to add an object"""
    return PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
        access_token="1234567812345678",
    )


@pytest.mark.xfail
def test_with_too_long_name():
    """test pcrtest patient pseudonym max length"""
    return PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="sadfasdfasdfasdasdfkjalsdkjflaks\
            djlfkasdlkfasldkfjalksdjfsdfdfdd",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
        access_token="2234567812345678",
    )


@pytest.mark.xfail
def test_with_too_short_name():
    """Test pcrtest patient pseudonym min length"""
    return PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="0123456789",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
        access_token="3234567812345678",
    )


@pytest.mark.xfail
def test_with_invalid_email_format():
    """test pcrtest email format"""
    return PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="testtest.com",
        collection_date="2022-08-21T11:18",
        access_token="43234567812345678",
    )


@pytest.mark.xfail
def test_with_bad_status():
    """Test pcrtest status enums"""
    return PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
        status="invalid",
        access_token="53234567812345678",
    )


@pytest.mark.xfail
def test_with_too_long_email():
    """Test pcrtest email char limit"""
    return PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="testtesttesttesttesttesttesttesttesttesttesttest\
        testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttest\
        testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttest\
        testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttest\
        testtesttest@test.com",
        collection_date="2022-08-21T11:18",
        access_token="63234567812345678",
    )


@pytest.mark.xfail
def test_with_too_long_token():
    """Test pcrtest access_token max length"""
    return PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
        access_token="a1b2c3d4e5f6g7h8i9",
    )


@pytest.mark.xfail
def test_with_invalid_token():
    """Test pcrtest access_token valid chars"""
    return PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
        access_token="a1b2c3d4e5f6g7h$",
    )


@pytest.mark.xfail
def test_with_date_no_t():
    """Test pcrtest collection_date formatting"""
    return PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21 11:18",
        access_token="73234567812345678",
    )


@pytest.mark.xfail
def test_with_date_short_year():
    """Test pcrtest year formatting in collection_date"""
    return PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="22-08-21T11:18",
        access_token="83234567812345678",
    )


@pytest.mark.xfail
def test_with_date_with_milliseconds():
    """Test pcrtest collection date with milliseconds (not allowed)"""
    return PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18.357",
        access_token="93234567812345678",
    )
