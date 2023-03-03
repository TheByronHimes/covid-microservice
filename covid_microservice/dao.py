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
""" Holds DAO classes, including Dao Protocol class"""


from hexkit.providers.mongodb.provider import MongoDbConfig, MongoDbDaoFactory

from .models import PcrTest


class SamplesDaoFactoryConfig(MongoDbConfig):
    """Contains config for DAO Factory"""

    collection_name = "samples"


async def get_mongodb_pcrtest_dao():
    """Return usable DAO"""
    config = SamplesDaoFactoryConfig(
        db_connection_str="mongodb://mongodb:27017", db_name="covid_db"
    )
    factory = MongoDbDaoFactory(config=config)
    return await factory.get_dao(
        name="samples", dto_model=PcrTest, id_field="access_token"
    )
