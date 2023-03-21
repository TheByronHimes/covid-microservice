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
"""A translator class for the inbound event consumer"""
from hexkit.custom_types import Ascii, JsonObject
from hexkit.protocols.eventsub import EventSubscriberProtocol
from pydantic import BaseSettings, Field

from cm.ports.inbound.notifier import NotifierPort


class EventSubTranslatorConfig(BaseSettings):
    """Config for consuming sample-update events"""

    sample_updated_event_topic: str = Field(
        ...,
        description="Name of the topic to publish events that inform about new file "
        + "uploads.",
        example="file_uploads",
    )
    sample_updated_event_type: str = Field(
        ...,
        description="The type to use for event that inform about new file uploads.",
        example="file_upload_received",
    )


class EventSubTranslator(EventSubscriberProtocol):
    """A translator for the EventSubscriberProtocol"""

    def __init__(self, config: EventSubTranslatorConfig, notifier: NotifierPort):
        """Initialize with config anb notifier dep"""

        self.topics_of_interest = [config.sample_updated_event_topic]
        self.types_of_interest = [config.sample_updated_event_type]

        self._notifier = notifier
        self._config = config

    async def _consume_validated(
        self, *, payload: JsonObject, type_: Ascii, topic: Ascii
    ) -> None:
        """Receive and process event"""
        raise NotImplementedError
