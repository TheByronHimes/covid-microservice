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

"""Test dummy."""

from covid_microservice.models import MongoDao, PcrTest


def test_mongo():
    """tests MongoDao functions"""
    mdao = MongoDao(PcrTest)
    assert mdao.delete_one({"access_token": 23423423}) is False


def test_mongo_pcrtest():
    """Make sure the MongoDao works with PcrTest usage"""
    mdao = MongoDao(PcrTest)
    pcr_test = PcrTest(
        patient_pseudonym="test test test",
        submitter_email="test@test.com",
        collection_date="test date",
    )
    assert isinstance(mdao.insert_one(pcr_test), int) is True
    assert mdao.find_one(pcr_test.dictify()) == pcr_test
