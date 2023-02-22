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
Desc: Module that handles the main API functionality.
Contents:
    - help_find_sample()
    - help_update_sample()
    - get_sample()
    - post_sample()
    - update_sample()
"""

from fastapi import APIRouter

from ..models import MongoDao, PcrTest, UpdatePcrTest
from .ancillary import make_access_token, make_sample_id

# Create connection to DB
mdao = MongoDao(PcrTest)


# Helper functions that might get moved or replaced by something else.
def help_find_sample(access_token: str) -> PcrTest:
    """Find sample"""
    return mdao.find_one({"access_token": access_token})


def help_update_sample(access_token: str, new_data: PcrTest) -> PcrTest:
    """Update sample"""
    result = mdao.update_one({"access_token": access_token}, new_data)
    return result


# Establish routes
sample_router = APIRouter()


@sample_router.get("/sample/{access_token}", status_code=200)
def get_sample(access_token: str):
    """
    Search for a test sample matching the access token.
    Handle GET req:
        1. Return test sample information if found
    """
    access_token = access_token.strip()
    sample = help_find_sample(access_token)
    data_to_return = sample.dictify(
        [
            "patient_pseudonym",
            "submitter_email",
            "collection_date",
            "status",
            "test_result",
            "test_date",
        ]
    )
    return data_to_return


@sample_router.post("/sample", status_code=201)
def post_sample(data: PcrTest):
    """
    Upload a new sample.
    Handle POST req:
        1. Insert new data
        2. Return sample_id and access_token
    """
    data.access_token = make_access_token()
    data.sample_id = make_sample_id()
    record_id = mdao.insert_one(data)
    sample = mdao.find_by_key(record_id)
    data_to_return = sample.dictify(["sample_id", "access_token"])

    return data_to_return


@sample_router.patch("/sample", status_code=201)
def update_sample(data: UpdatePcrTest):
    """
    Update a test sample with results.
    Handle PATCH req:
        1. Find sample with matching access_token
        2. Update sample
        3. Return updated sample
    """
    sample = help_find_sample(data.access_token)
    sample.status = data.status
    sample.test_result = data.test_result
    sample.test_date = data.test_date

    result = help_update_sample(data.access_token, sample)

    return result.dictify()
