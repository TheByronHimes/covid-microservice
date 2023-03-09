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
from hexkit.providers.mongodb.provider import MongoDbDaoNaturalId

from ..core.models import NewSampleResponse, NewSampleSubmission, PcrTest, UpdatePcrTest
from ..core.utils import make_access_token, make_sample_id
from .deps import get_mongodb_pcrtest_dao

MSG_NOT_FOUND = "Specified resource was not found."

# This APIRouter instance will be referenced/included by 'app' in main.py
sample_router = APIRouter()


# GET /sample
@sample_router.get(
    "/sample/{access_token}",
    status_code=200,
    summary="Retrieve a existing sample",
    response_model=dict,
)
async def get_sample(
    access_token: str, mdao: MongoDbDaoNaturalId = Depends(get_mongodb_pcrtest_dao)
) -> dict:
    """
    Retrieve information for a test sample matching the access token.

    Args:
        access_token (str): The access token for the sample.
        mdao: A MongoDB DAO object for accessing the database.

    Returns:
        dict: A dictionary containing the sample information.

    Raises:
        HTTPException: If the specified resource was not found.
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
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=MSG_NOT_FOUND) from exc


# POST /sample
@sample_router.post(
    "/sample",
    summary="Upload a new sample",
    status_code=201,
    response_model=NewSampleResponse,
)
async def post_sample(
    data: NewSampleSubmission,
    mdao: MongoDbDaoNaturalId = Depends(get_mongodb_pcrtest_dao),
) -> NewSampleResponse:
    """
    Upload a new sample.

    Args:
        data (NewSampleSubmission): The data for the new sample.
        mdao: A MongoDB DAO object for accessing the database.

    Returns:
        NewSampleResponse: The access token and sample ID for the new sample.
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
    "/sample",
    status_code=204,
    summary="Update an existing sample's test results",
    response_model=None,
)
async def update_sample(
    data: UpdatePcrTest, mdao: MongoDbDaoNaturalId = Depends(get_mongodb_pcrtest_dao)
):
    """
    Update a test sample with new test results.

    Args:
        data (UpdatePcrTest): A data object containing the updated test results,
        including status, test_result, and test_date.
        mdao: A MongoDB DAO object for accessing the database.

    Returns:
        None. Returns a 204 No Content status code if the update was successful.

    Raises:
        HTTPException: If the test sample with the matching access_token cannot be
        found, raises a 404 Not Found error.
    """
    try:
        sample = await mdao.get_by_id(data.access_token)
        sample.status = data.status
        sample.test_result = data.test_result
        sample.test_date = data.test_date
        await mdao.update(sample)
        return 204
    except ResourceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=MSG_NOT_FOUND) from exc
