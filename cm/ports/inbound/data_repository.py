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

"""Port for a data repository, which, again, has very little to do with the
repository design pattern."""
from abc import ABC, abstractmethod

from cm.core import models


class DataRepositoryPort(ABC):
    """Port for a data repository with Sample objects"""

    class SampleNotFoundError(RuntimeError):
        """Raised when no sample was found with the specified sample_id"""

        def __init__(self, *, sample_id: str):
            message = f"No Sample with the following ID exists: {sample_id}"
            super().__init__(message)

    class UnauthorizedRequestError(RuntimeError):
        """Raised when a request/action is unauthorized"""

        def __init__(self, *, sample_id: str):
            message = f"Unauthorized to access Sample ID {sample_id}"
            super().__init__(message)

    @abstractmethod
    async def retrieve_sample(
        self, *, sample_id: str, access_token: str
    ) -> models.Sample:
        """Retrieves and returns a sample with the specified sample_id.
        Raises:
            SampleNotFoundError: when unable to find a matching sample_id
            UnauthorizedRequestError: when access_token doesn't match what's expected"""
        ...

    @abstractmethod
    async def create_sample(
        self, *, sample_creation: models.SampleCreation
    ) -> models.SampleAuthDetails:
        """Takes the supplied SampleCreation object and uses it to create a Sample
        object along with a randomly generated access token and sample ID"""
        ...

    @abstractmethod
    async def update_sample(
        self, *, updates: models.SampleUpdate, access_token: str
    ) -> None:
        """Takes the supplied SampleUpdate object, finds the matching sample,
        and applies the updates
        Raises:
            SampleNotFoundError: when unable to find a matching sample_id
            UnauthorizedRequestError: when access_token doesn't match what's expected"""
        ...
