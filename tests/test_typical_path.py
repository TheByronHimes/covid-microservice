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
"""Tests the typical path(s) of user interaction, following an upload-update-query
sequence of events."""
import json

import pytest
from ghga_service_chassis_lib.utils import DateTimeUTC
from hexkit.providers.akafka.testutils import ExpectedEvent, kafka_fixture  # noqa: F401
from hexkit.providers.mongodb.testutils import mongodb_fixture  # noqa: F401

from cm.core import models
from tests.fixtures.joint import JointFixture, joint_fixture  # noqa: F401


@pytest.mark.parametrize(
    ("parms"),
    [
        {
            "patient_pseudonym": "Stephen Nehigh",
            "submitter_email": "test@test.com",
            "collection_date": "2023-02-02T11:37-07:00",
            "status": models.SampleStatus.COMPLETED,
            "test_result": models.SampleTestResult.NEGATIVE,
            "test_date": "2023-02-03T11:01-07:00",
        }
    ],
)
@pytest.mark.asyncio
async def test_full_journey(joint_fixture: JointFixture, parms):  # noqa: F811
    """The path:
    1. Upload sample
        - check response
    2. Update sample
        - check updates are applied
        - check response
        - check that event was published
    3. Query sample
        - check results
        - check errors (query non-existent sample)
    """
    # submit new sample
    sample = {
        "patient_pseudonym": parms["patient_pseudonym"],
        "submitter_email": parms["submitter_email"],
        "collection_date": parms["collection_date"],
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
        "access_token_hash",
        "sample_id",
    ]:
        assert field_name in body

    access_token = body["access_token"]
    sample_id = body["sample_id"]

    # perform update
    sample_update = {
        "sample_id": sample_id,
        "status": parms["status"],
        "test_result": parms["test_result"],
        "test_date": parms["test_date"],
    }

    headers = {"Authorization": "Bearer " + access_token}

    expected_payload = json.loads(models.SampleNoAuth(**sample, **sample_update).json())

    expected_events = [
        ExpectedEvent(
            payload=expected_payload,
            type_=joint_fixture.config.sample_updated_event_type,
            key=sample_id,
        )
    ]

    # verify that updating a sample leads to the publishing of an event
    async with joint_fixture.kafka.expect_events(
        events=expected_events, in_topic=joint_fixture.config.sample_updated_event_topic
    ):
        await joint_fixture.rest_client.patch(
            url="/samples", json=sample_update, headers=headers
        )

    # consume event produced just now
    event_subscriber = await joint_fixture.container.kafka_event_subscriber()
    await event_subscriber.run(forever=False)

    # Try to retrieve updated sample, verify results
    response_from_get = await joint_fixture.rest_client.get(
        url=f"/samples/{sample_id}", headers=headers
    )

    assert response_from_get.status_code == 200

    body_from_get = response_from_get.json()
    assert body_from_get["sample_id"] == sample_id
    assert body_from_get["submitter_email"] == parms["submitter_email"]
    assert DateTimeUTC.fromisoformat(
        body_from_get["collection_date"]
    ) == DateTimeUTC.fromisoformat(parms["collection_date"])
    assert body_from_get["status"] == parms["status"]
    assert body_from_get["test_result"] == parms["test_result"]
    assert DateTimeUTC.fromisoformat(
        body_from_get["test_date"]
    ) == DateTimeUTC.fromisoformat(parms["test_date"])

    # Update sample via published event
    update_event = {
        "sample_id": sample_id,
        "status": models.SampleStatus.COMPLETED,
        "test_result": models.SampleTestResult.POSITIVE,
        "test_date": "2023-02-03T14:15-07:00",
    }

    await joint_fixture.kafka.publish_event(
        payload=update_event,
        type_=joint_fixture.config.update_sample_event_type,
        topic=joint_fixture.config.update_sample_event_topic,
        key=sample_id,
    )

    # consume update_sample event, which should trigger the update
    await event_subscriber.run(forever=False)

    # Verify that the update was applied, and only check the fields we updated
    response_from_get2 = await joint_fixture.rest_client.get(
        url=f"/samples/{sample_id}", headers=headers
    )
    body_from_get = response_from_get2.json()
    assert body_from_get["sample_id"] == sample_id
    assert body_from_get["status"] == update_event["status"]
    assert body_from_get["test_result"] == update_event["test_result"]
    assert DateTimeUTC.fromisoformat(
        body_from_get["test_date"]
    ) == DateTimeUTC.fromisoformat(update_event["test_date"])
