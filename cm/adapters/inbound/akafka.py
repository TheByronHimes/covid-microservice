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

"""Contains the inbound kafka translator"""
from hexkit.custom_types import Ascii, JsonObject
from hexkit.protocols.eventsub import EventSubscriberProtocol
from pydantic import BaseSettings, Field

from cm.core import models
from cm.ports.inbound.data_repository import DataRepositoryPort


class EventSubTranslatorConfig(BaseSettings):
    """Config for the event subscriber"""

    update_sample_event_topic: str = Field(
        ...,
        description="Name of the event topic that tracks sample events",
        example="sample_events",
    )
    update_sample_event_type: str = Field(
        ...,
        description="The type label for events containing update-op data for samples",
        example="update_sample",
    )


class EventSubTranslator(EventSubscriberProtocol):
    """A translator that can consume Sample Update events"""

    def __init__(
        self, *, config: EventSubTranslatorConfig, data_repository: DataRepositoryPort
    ):
        self._config = config
        self._data_repository = data_repository

        self.topics_of_interest = [
            config.update_sample_event_topic,
        ]
        self.types_of_interest = [
            config.update_sample_event_type,
        ]

    async def _update_sample(self, *, sample_updates: models.SampleUpdate):
        """Sends updates to data repository to be applied. Because it is an internal
        (service to service) call, we bypass the authorization."""
        await self._data_repository.update_sample(
            updates=sample_updates, is_external=False
        )

    async def _consume_validated(  # pylint: disable=unused-argument
        self, *, payload: JsonObject, type_: Ascii, topic: Ascii
    ) -> None:
        """Consumes an event"""
        if type_ == self._config.update_sample_event_type:
            sample_updates = models.SampleUpdate(**payload)
            await self._update_sample(sample_updates=sample_updates)
        else:
            raise RuntimeError(f"Received unexpected event type: {type_}")
