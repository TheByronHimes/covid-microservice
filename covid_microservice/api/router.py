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
"""

from fastapi import APIRouter

from ..core.samples import help_find_sample, help_update_sample
from ..core.utils import make_access_token, make_sample_id
from ..dao import MongoDummyDao
from ..models import NewSampleSubmission, PcrTest, UpdatePcrTest

# Set up a DAO
mdao = MongoDummyDao(PcrTest, "sample_id")

# This APIRouter instance will be referenced/included by 'app' in main.py
sample_router = APIRouter()


# GET /sample
@sample_router.get(
    "/sample/{access_token}", status_code=200, summary="Retrieve a existing sample"
)
def get_sample(access_token: str):
    """
    Search for a test sample matching the access token.
    Handle GET req:
        1. Return test sample information if found
    """
    access_token = access_token.strip()
    sample = help_find_sample(access_token, mdao)
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


# POST /sample
@sample_router.post("/sample", status_code=201, summary="Upload a new sample")
def post_sample(data: NewSampleSubmission):
    """
    Upload a new sample.
    Handle POST req:
        1. Insert new data
        2. Return sample_id and access_token
    """
    pcrtest = PcrTest(
        patient_pseudonym=data.patient_pseudonym,
        submitter_email=data.submitter_email,
        collection_date=data.collection_date,
        sample_id=make_sample_id(),
        access_token=make_access_token(),
    )

    record_id = mdao.insert_one(pcrtest)
    sample = mdao.find_by_key(record_id)
    data_to_return = sample.dictify(["sample_id", "access_token"])
    #
    return data_to_return


# PATCH /sample
@sample_router.patch(
    "/sample", status_code=204, summary="Update an existing sample's test results"
)
def update_sample(data: UpdatePcrTest):
    """
    Update a test sample with results.
    Handle PATCH req:
        1. Find sample with matching access_token
        2. Update sample
        3. Return success code (no body)
    """
    sample = help_find_sample(data.access_token, mdao)
    if isinstance(sample, PcrTest):
        sample.status = data.status
        sample.test_result = data.test_result
        sample.test_date = data.test_date
        help_update_sample(data.access_token, sample, mdao)
        return 204
    return 422
