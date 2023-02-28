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

import asyncio

import pytest

from covid_microservice.api import router
from covid_microservice.models import NewSampleSubmission, UpdatePcrTest


@pytest.fixture(scope="session")
def event_loop():
    """Override pytest-asyncio EL fixture so we can do multiple async tests"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_post_sample_nominal():
    """Test the /sample POST function"""
    data = NewSampleSubmission(
        patient_pseudonym="test test test",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
    )

    obj = await router.post_sample(data)
    assert isinstance(obj, dict)
    assert "sample_id" in obj
    assert "access_token" in obj
    assert len(obj.keys()) == 2


@pytest.mark.asyncio()
async def test_update_sample_nominal():
    """Test that the update function works when it should"""
    data = NewSampleSubmission(
        patient_pseudonym="Franklin York",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:11",
    )
    result = await router.post_sample(data)
    access_token = result["access_token"]

    updates = UpdatePcrTest(
        access_token=access_token,
        status="completed",
        test_result="positive",
        test_date="2022-08-23T08:37",
    )
    response = await router.update_sample(updates)
    assert response == 204


@pytest.mark.asyncio
async def test_update_non_existent_sample():
    """Receive 422 code upon updating non-existent sample (bad access token)"""
    updates = UpdatePcrTest(
        access_token="doesnotexist",
        status="completed",
        test_result="positive",
        test_date="2022-08-23T08:37",
    )
    response = await router.update_sample(updates)
    assert response == 422


@pytest.mark.asyncio
async def test_get_nonexistent_sample():
    """Test what happens when a user searches with a bad access token"""
    data = await router.get_sample(access_token="doesnotexist")
    assert data == {}


@pytest.mark.asyncio
async def test_get_existing_sample():
    """Make sure nominal retrieval works"""
    data = NewSampleSubmission(
        patient_pseudonym="Franklin York 2",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:11",
    )
    result = await router.post_sample(data)
    access_token = result["access_token"]

    response = await router.get_sample(access_token=access_token)
    assert isinstance(response, dict)
    assert response["patient_pseudonym"] == "Franklin York 2"
