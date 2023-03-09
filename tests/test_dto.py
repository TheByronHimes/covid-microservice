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

"""Test module for testing DTOs"""
import pytest

from covid_microservice.core.models import Dto, NewSampleSubmission, PcrTest
from covid_microservice.core.utils import make_sample_id


def test_pcrtest_is_dto():
    """Make sure PcrTest is detected as a subclass of Dto"""
    pcrtest = PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
        access_token="1234567812345678",
    )
    assert issubclass(PcrTest, Dto)
    assert isinstance(pcrtest, Dto)


def test_pcrtest_with_all_valid_input():
    """Uses valid input to add an object"""
    pcrtest = PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
        access_token="1234567812345678",
    )
    assert isinstance(pcrtest, PcrTest)


@pytest.mark.xfail
def test_pcrtest_with_too_long_name():
    """test pcrtest patient pseudonym max length"""
    PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="sadfasdfasdfasdasdfkjalsdkjflaks\
            djlfkasdlkfasldkfjalksdjfsdfdfdd",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
        access_token="2234567812345678",
    )


@pytest.mark.xfail
def test_pcrtest_with_too_short_name():
    """Test pcrtest patient pseudonym min length"""
    PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="0123456789",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
        access_token="3234567812345678",
    )


@pytest.mark.xfail
def test_pcrtest_with_invalid_email_format():
    """test pcrtest email format"""
    PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="testtest.com",
        collection_date="2022-08-21T11:18",
        access_token="43234567812345678",
    )


@pytest.mark.xfail
def test_pcrtest_with_bad_status():
    """Test pcrtest status enums"""
    PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
        status="invalid",
        access_token="53234567812345678",
    )


@pytest.mark.xfail
def test_pcrtest_with_bad_test_result():
    """Test pcrtest test_result enums"""
    PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
        status="completed",
        test_result="invalid",
        access_token="53234567812345678",
    )


@pytest.mark.xfail
def test_pcrtest_with_too_long_email():
    """Test pcrtest email char limit"""
    PcrTest(
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
def test_pcrtest_with_invalid_token():
    """Test pcrtest access_token valid chars"""
    PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
        access_token="a1b2c3d4e5f6g7h$",
    )


@pytest.mark.xfail
def test_pcrtest_with_date_no_t():
    """Test pcrtest collection_date formatting"""
    PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21 11:18",
        access_token="73234567812345678",
    )


@pytest.mark.xfail
def test_pcrtest_with_date_short_year():
    """Test pcrtest year formatting in collection_date"""
    PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="22-08-21T11:18",
        access_token="83234567812345678",
    )


@pytest.mark.xfail
def test_pcrtest_with_date_with_milliseconds():
    """Test pcrtest collection date with milliseconds (not allowed)"""
    PcrTest(
        sample_id=make_sample_id(),
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18.357",
        access_token="93234567812345678",
    )


###########
# New Sample Submission Tests
###########


def test_nss_with_all_valid_input():
    """Uses valid input to add an object"""
    nss = NewSampleSubmission(
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
    )
    assert isinstance(nss, NewSampleSubmission)


@pytest.mark.xfail
def test_nss_with_too_long_name():
    """test pcrtest patient pseudonym max length"""
    NewSampleSubmission(
        patient_pseudonym="sadfasdfasdfasdasdfkjalsdkjflaks\
            djlfkasdlkfasldkfjalksdjfsdfdfdd",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
    )


@pytest.mark.xfail
def test_nss_with_too_short_name():
    """Test pcrtest patient pseudonym min length"""
    NewSampleSubmission(
        patient_pseudonym="0123456789",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
    )


@pytest.mark.xfail
def test_nss_with_invalid_email_format():
    """test pcrtest email format"""
    NewSampleSubmission(
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="testtest.com",
        collection_date="2022-08-21T11:18",
    )


@pytest.mark.xfail
def test_nss_with_date_no_t():
    """Test pcrtest collection_date formatting"""
    NewSampleSubmission(
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21 11:18",
    )


@pytest.mark.xfail
def test_nss_with_date_short_year():
    """Test pcrtest year formatting in collection_date"""
    NewSampleSubmission(
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="22-08-21T11:18",
    )


@pytest.mark.xfail
def test_nss_with_date_with_milliseconds():
    """Test pcrtest collection date with milliseconds (not allowed)"""
    NewSampleSubmission(
        patient_pseudonym="Alfredo Barnelli",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18.357",
    )
