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
"""Kafka-based event publishing adapters and the exceptions they may throw."""

from hexkit.protocols.eventpub import EventPublisherProtocol
from pydantic import BaseSettings, Field

from cm.ports.outbound.event_pub import EventPublisherPort


class EventPubTranslatorConfig(BaseSettings):
    """Config for publishing events for sample updates"""

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


class EventPubTranslator(EventPublisherPort):
    """A translator for event-publishing functionality"""

    def __init__(
        self, *, config: EventPubTranslatorConfig, provider: EventPublisherProtocol
    ) -> None:
        """Assign config and event-publishing provider"""
        self._config = config
        self._provider = provider

    async def publish_sample_updated(
        self, *, submitter_email: str, sample_id: str
    ) -> None:
        """Publish an event saying that a sample was updated, include submitter
        email and sample id"""
        event_payload = {"submitter_email": submitter_email, "sample_id": sample_id}
        await self._provider.publish(
            payload=event_payload,
            type_=self._config.sample_updated_event_type,
            topic=self._config.sample_updated_event_topic,
            key=str(sample_id) + submitter_email,
        )
