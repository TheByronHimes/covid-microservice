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


class EventSubTranslatorConfig(BaseSettings):
    """Config for the event subscriber"""

    sample_updated_event_topic: str = Field(
        ...,
        description="Name of the event topic used to track sample update events",
        example="sample_updates",
    )
    sample_updated_event_type: str = Field(
        ...,
        description="The type to use for event that inform about sample updates.",
        example="sample_updated",
    )


class EventSubTranslator(EventSubscriberProtocol):
    """A translator that can consume Sample Update events"""

    def __init__(self, *, config: EventSubTranslatorConfig):
        self._config = config

        self.topics_of_interest = [config.sample_updated_event_topic]
        self.types_of_interest = [config.sample_updated_event_type]

    async def _consume_validated(  # pylint: disable=unused-argument
        self, *, payload: JsonObject, type_: Ascii, topic: Ascii
    ) -> None:
        """Consumes an event"""
        if type_ != self._config.sample_updated_event_type:
            raise RuntimeError(f"Received unexpected event type: {type_}")

        if topic != self._config.sample_updated_event_topic:
            raise RuntimeError(f"Received unexpected topic: {topic}")
