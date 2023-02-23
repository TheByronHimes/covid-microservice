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

"""Test module for functionality common to DAOs (at this time all Mongo based)"""

import pytest

from covid_microservice.dao import Dao, MongoDummyDao
from covid_microservice.models import PcrTest

# parametrize with MongoDummyDao and MongoDao (which doesn't exist yet)
pytestmark = pytest.mark.parametrize("concrete_class", [MongoDummyDao])
ID_FIELD = "sample_id"


def test_mongodao_implements_dao_protocol(concrete_class):
    """Verify that the DAOs adhere to the protocol"""
    mdao = concrete_class(PcrTest, ID_FIELD)
    assert isinstance(mdao, Dao)


# Test common functions of concrete DAO implementations
def test_dao_delete(concrete_class):
    """Test deletion of nonexistent data"""
    mdao = concrete_class(PcrTest, ID_FIELD)
    assert mdao.delete_one({"access_token": 23423423}) is False


def test_mongo_pcrtest(concrete_class):
    """Make sure the Dao works with PcrTest usage"""
    mdao = concrete_class(PcrTest, ID_FIELD)
    pcr_test = PcrTest(
        patient_pseudonym="test test test",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
    )
    assert isinstance(mdao.insert_one(pcr_test), int)
    assert mdao.find_one(pcr_test.dictify()) == pcr_test
