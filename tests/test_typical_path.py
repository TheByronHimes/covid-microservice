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
from hexkit.providers.akafka.testutils import kafka_fixture  # noqa
from hexkit.providers.mongodb.testutils import mongodb_fixture  # noqa

from cm.core import models
from tests.fixtures.joint import JointFixture, joint_fixture  # noqa


@pytest.mark.asyncio
async def test_full_journey(joint_fixture: JointFixture):  # noqa
    """The path:
    1. Upload sample
        - check response
    2. Update sample
        - check updates are applied
        - check response
        - check errors (update nonexistent sample)
    3. Query sample
        - check results
        - check errors (query non-existent sample)
    """

    sample = {
        "patient_pseudonym": "Stephen Nehigh",
        "submitter_email": "byro93@live.com",
        "collection_date": "2023-02-02T11:37",
    }
    response_from_post = await joint_fixture.rest_client.post(
        url="/samples",
        json=sample,
    )

    body = response_from_post.json()

    # verify the contents of the response
    for field_name in [
        "patient_pseudonym",
        "submitter_email",
        "collection_date",
        "status",
        "test_result",
        "test_date",
        "access_token",
        "sample_id",
    ]:
        assert field_name in body

    access_token = body["access_token"]
    sample_id = body["sample_id"]

    sample_update = {
        "sample_id": sample_id,
        "status": models.SampleStatus.COMPLETED,
        "test_result": models.SampleTestResult.NEGATIVE,
        "test_date": "2023-02-03T11:45",
    }

    headers = {"Authorization": "Bearer " + access_token}

    response_from_patch = await joint_fixture.rest_client.patch(
        url="/samples", json=sample_update, headers=headers
    )

    assert response_from_patch.status_code == 204

    response_from_get = await joint_fixture.rest_client.get(
        url=f"/samples/{sample_id}", headers=headers
    )

    assert response_from_get.status_code == 200

    body_from_get = response_from_get.json()
    assert body_from_get["sample_id"] == sample_id
    assert body_from_get["submitter_email"] == "byro93@live.com"
    assert body_from_get["collection_date"] == "2023-02-02T11:37"
    assert body_from_get["status"] == models.SampleStatus.COMPLETED
    assert body_from_get["test_result"] == models.SampleTestResult.NEGATIVE
    assert body_from_get["test_date"] == "2023-02-03T11:45"
