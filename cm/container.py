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
"""Dependency-Injection container"""
from hexkit.inject import ContainerBase, get_configurator, get_constructor
from hexkit.providers.akafka.provider import KafkaEventPublisher
from hexkit.providers.mongodb import MongoDbDaoFactory

from cm.adapters.outbound.akafka import EventPubTranslator
from cm.adapters.outbound.dao import SampleDaoConstructor
from cm.config import Config
from cm.core.authorizer import Authorizer
from cm.core.data_repository import DataRepository


class Container(ContainerBase):
    """Dependency-Injection Container"""

    config = get_configurator(Config)

    # outbound providers
    dao_factory = get_constructor(MongoDbDaoFactory, config=config)
    kafka_event_publisher = get_constructor(KafkaEventPublisher, config=config)

    # outbound translators
    sample_dao = get_constructor(SampleDaoConstructor, dao_factory=dao_factory)
    event_publisher = get_constructor(
        EventPubTranslator, config=config, provider=kafka_event_publisher
    )

    # domain/core components:
    data_repository = get_constructor(
        DataRepository,
        sample_dao=sample_dao,
        authorizer=Authorizer(),
        event_publisher=event_publisher,
    )
