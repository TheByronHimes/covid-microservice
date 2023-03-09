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
import pytest_asyncio
from fastapi.testclient import TestClient
from hexkit.providers.mongodb.testutils import (  # noqa: F401; pylint: disable=unused-import
    mongodb_fixture,
)

from covid_microservice.api.deps import get_mongodb_pcrtest_dao
from covid_microservice.api.main import app
from covid_microservice.core.models import PcrTest

SAMPLE_URL = "/sample"


@pytest_asyncio.fixture(name="client_with_db")
async def fixture_client_with_db(
    mongodb_fixture,  # noqa: F811; pylint: disable=redefined-outer-name
):
    """Yield a TestClient with a test db. This replaces the DAO dependency in
    the Router instance with the test DAO produced here"""
    dao = await mongodb_fixture.dao_factory.get_dao(
        name="samples",
        dto_model=PcrTest,
        id_field="access_token",
    )
    app.dependency_overrides[get_mongodb_pcrtest_dao] = lambda: dao
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_post_sample_nominal(client_with_db):
    """Test the /sample POST function"""
    nss = {
        "patient_pseudonym": "test test test",
        "submitter_email": "test@test.com",
        "collection_date": "2022-08-21T11:18",
    }

    response = client_with_db.post(SAMPLE_URL, json=nss).json()
    assert isinstance(response, dict)
    assert "sample_id" in response
    assert "access_token" in response
    assert len(response.keys()) == 2


@pytest.mark.asyncio
async def test_update_sample_nominal(client_with_db):
    """Test that the update function works when it should"""
    nss = {
        "patient_pseudonym": "Franklin York",
        "submitter_email": "test@test.com",
        "collection_date": "2022-08-21T11:11",
    }

    with client_with_db:
        post_response = client_with_db.post(SAMPLE_URL, json=nss).json()
        access_token = post_response["access_token"]

        updates = {
            "access_token": access_token,
            "status": "completed",
            "test_result": "positive",
            "test_date": "2022-08-23T08:37",
        }
        patch_response = client_with_db.patch(SAMPLE_URL, json=updates)
        assert patch_response.status_code == 204


@pytest.mark.asyncio
async def test_update_non_existent_sample(client_with_db):
    """Receive 4xx code upon updating non-existent sample (bad access token)"""
    updates = {
        "access_token": "doesnotexist",
        "status": "completed",
        "test_result": "positive",
        "test_date": "2022-08-23T08:37",
    }

    client_with_db = TestClient(app)

    response = client_with_db.patch(SAMPLE_URL, json=updates)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_nonexistent_sample(client_with_db):
    """Test what happens when a user searches with a bad access token"""

    data = client_with_db.get(SAMPLE_URL + "eqfeqefew44")
    assert data.json() == {"detail": "Not Found"}


@pytest.mark.asyncio
async def test_get_existing_sample(client_with_db):
    """Make sure nominal retrieval works"""
    nss = {
        "patient_pseudonym": "Franklin York 2",
        "submitter_email": "test@test.com",
        "collection_date": "2022-08-21T11:11",
    }
    with client_with_db:
        result = client_with_db.post(SAMPLE_URL, json=nss).json()
        access_token = result["access_token"]

        response = client_with_db.get(SAMPLE_URL + "/" + access_token).json()
        assert isinstance(response, dict)
        assert response["patient_pseudonym"] == "Franklin York 2"
