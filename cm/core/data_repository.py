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
"""This is called a repository but it has nothing to do with the Repository Pattern.
Basically, it houses all the domain logic."""
import secrets
import string

from cm.core import models
from cm.core.authorizer import AuthorizerInterface
from cm.ports.inbound.data_repository import DataRepositoryPort
from cm.ports.outbound.dao import ResourceNotFoundError, SampleDaoPort
from cm.ports.outbound.event_pub import EventPublisherPort


class DataRepository(DataRepositoryPort):
    """Data repository implementation for sample object interaction"""

    def __init__(
        self,
        *,
        sample_dao: SampleDaoPort,
        authorizer: AuthorizerInterface,
        event_publisher: EventPublisherPort
    ):
        """Initialize with the sample_dao object."""
        self._sample_dao = sample_dao
        self._authorizer = authorizer
        self._event_publisher = event_publisher

    def _random_string(self, num):
        """Produce a string containing num random numbers and letters"""
        chars = string.ascii_letters + string.digits
        return "".join([secrets.choice(chars) for _ in range(num)])

    async def retrieve_sample(
        self, *, sample_id: str, access_token: str
    ) -> models.Sample:
        try:
            sample = await self._sample_dao.get_by_id(sample_id)
        except ResourceNotFoundError as err:
            raise self.SampleNotFoundError(sample_id=sample_id) from err
        if not self._authorizer.check_token(
            token_plain=access_token, token_hashed=sample.access_token_hash
        ):
            raise self.UnauthorizedRequestError(sample_id=sample_id)
        return sample

    async def create_sample(
        self, *, sample_creation: models.SampleCreation
    ) -> models.SampleAuthDetails:
        access_token = self._authorizer.generate_token(length=16)
        access_token_hash = self._authorizer.hash_token(token=access_token)
        sample = models.Sample(
            **sample_creation.dict(),
            sample_id=self._random_string(10),
            access_token_hash=access_token_hash
        )
        await self._sample_dao.insert(sample)
        sample_auth_details = models.SampleAuthDetails(
            **sample.dict(), access_token=access_token
        )
        return sample_auth_details

    async def update_sample(
        self,
        *,
        updates: models.SampleUpdate,
        access_token: str = "",
        is_external: bool = True
    ) -> None:
        try:
            sample = await self._sample_dao.get_by_id(updates.sample_id)
        except ResourceNotFoundError as err:
            raise self.SampleNotFoundError(sample_id=updates.sample_id) from err

        if is_external:
            if not self._authorizer.check_token(
                token_plain=access_token, token_hashed=sample.access_token_hash
            ):
                raise self.UnauthorizedRequestError(sample_id=updates.sample_id)

        sample.status = updates.status
        sample.test_result = updates.test_result
        sample.test_date = updates.test_date
        await self._sample_dao.update(sample)

        sample_no_auth = models.SampleNoAuth(**sample.dict())
        await self._event_publisher.publish_sample_updated(
            sample_no_auth=sample_no_auth
        )
