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


from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from hexkit.protocols.dao import ResourceNotFoundError

from ..core.utils import make_access_token, make_sample_id
from ..dao import get_mongodb_pcrtest_dao
from ..models import NewSampleResponse, NewSampleSubmission, PcrTest, UpdatePcrTest

# This APIRouter instance will be referenced/included by 'app' in main.py
sample_router = APIRouter()


# GET /sample
@sample_router.get(
    "/sample/{access_token}", status_code=200, summary="Retrieve a existing sample"
)
async def get_sample(access_token: str, mdao=Depends(get_mongodb_pcrtest_dao)):
    """
    Search for a test sample matching the access token.
    Handle GET req:
        1. Return test sample information if found
    """
    try:
        sample = await mdao.get_by_id(access_token.strip())
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
    except ResourceNotFoundError:
        return {}


# POST /sample
@sample_router.post(
    "/sample",
    summary="Upload a new sample",
    status_code=201,
)
async def post_sample(data: NewSampleSubmission, mdao=Depends(get_mongodb_pcrtest_dao)):
    """
    Upload a new sample.
    Handle POST req:
        1. Insert new data
        2. Return sample_id and access_token
    """
    sample_id = make_sample_id()
    access_token = make_access_token()
    pcrtest = PcrTest(
        patient_pseudonym=data.patient_pseudonym,
        submitter_email=data.submitter_email,
        collection_date=data.collection_date,
        sample_id=sample_id,
        access_token=access_token,
    )

    await mdao.insert(pcrtest)
    result = await mdao.get_by_id(access_token)
    sample_response = NewSampleResponse(
        access_token=result.access_token, sample_id=result.sample_id
    )

    return sample_response


# PATCH /sample
@sample_router.patch(
    "/sample", status_code=204, summary="Update an existing sample's test results"
)
async def update_sample(data: UpdatePcrTest, mdao=Depends(get_mongodb_pcrtest_dao)):
    """
    Update a test sample with results.
    Handle PATCH req:
        1. Find sample with matching access_token
        2. Update sample
        3. Return success code (no body)
    """
    try:
        sample = await mdao.get_by_id(data.access_token)
        sample.status = data.status
        sample.test_result = data.test_result
        sample.test_date = data.test_date
        await mdao.update(sample)
        return 204
    except ResourceNotFoundError as exc:
        raise HTTPException(
            status_code=404, detail="Specified resource was not found."
        ) from exc
