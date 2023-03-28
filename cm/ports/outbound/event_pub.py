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
Contains definition for the outbound port for event publishing
"""

from typing import Protocol

from cm.core import models


class EventPublisherPort(Protocol):
    """An interface for an adapter that publishes events related to this service"""

    async def publish_sample_updated(
        self, *, sample_no_auth: models.SampleNoAuth
    ) -> None:
        """Publish an event with the updated Sample info"""
        ...
