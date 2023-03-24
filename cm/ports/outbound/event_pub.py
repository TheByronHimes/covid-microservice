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
"""
Borrowed from upload-controller-service, slight tweaks.
"""

from typing import Protocol


class EventPublisherPort(Protocol):
    """An interface for an adapter that publishes events related to this service"""

    async def publish_sample_updated(
        self, *, submitter_email: str, sample_id: str
    ) -> None:
        """Publish event saying that the given sample was updated"""
        ...
