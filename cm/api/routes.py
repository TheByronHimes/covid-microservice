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
Desc:
Module that handles the main API functionality. This breaks from THA somewhat, in
that this module is neither a port, a translator, or an adaptor, nor is it core logic.
The business/domain logic is housed in the data_repository.py module in cm.core
in order to minimize the deviation from THA. This way, the API doesn't know anything
about the implementation of the business logic, only the contract that it itself is a
part of: You supply ABC, I return XYZ. The how and why of exchanging ABC for XYZ is a
mystery from the perspective of the API. The only difference between what the outside
world sees and what the API sees is that the API sees the data repository, which deals
in whole objects. The API will take the result of a call to the data repository and
return either the whole result or a subset of the result. An example is in get_sample,
where the data repository returns a complete Sample object, but the API returns
everything except for the access_token and sample_id fields. The data repository doesn't
care about what the API wants or needs, and the API doesn't care about what the data
repository does at night.

So if you look at the path operation functions, you will notice that all the real logic
is being done by the data_repository object, which is injected by the
Dependency Injection (DI) Container (just called "container"). That container, from
container.py, is responsible for configuration and provision of objects like the
data_repository and DAO.
"""

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from cm.container import Container
from cm.core import models
from cm.ports.inbound.data_repository import DataRepositoryPort

MSG_NOT_FOUND = "Specified resource was not found."
MSG_UNAUTHORIZED = "Unauthorized access requested"

# This APIRouter instance will be referenced/included by 'app' in main.py
sample_router = APIRouter()

# To instruct FastAPI how to authenticate requests that need it
bearer_scheme = HTTPBearer()


# GET /sample
@sample_router.get(
    "/samples/{sample_id}",
    status_code=200,
    summary="Retrieve a existing sample",
    response_model=dict,
)
@inject
async def get_sample(
    sample_id: str,
    data_repository: DataRepositoryPort = Depends(Provide[Container.data_repository]),
    authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> models.Sample:
    """
    Retrieve information for a test sample matching the access token.
    """

    access_token = authorization.credentials

    try:
        sample = await data_repository.retrieve_sample(
            sample_id=sample_id, access_token=access_token
        )

    except DataRepositoryPort.SampleNotFoundError as err:
        raise HTTPException(status_code=404, detail=MSG_NOT_FOUND) from err
    except DataRepositoryPort.UnauthorizedRequestError as err:
        raise HTTPException(status_code=403, detail=MSG_UNAUTHORIZED) from err
    return sample


# POST /sample
@sample_router.post(
    "/samples",
    summary="Upload a new sample",
    status_code=201,
    response_model=models.SampleAuthDetails,
)
@inject
async def samples_post(
    data: models.SampleCreation,
    data_repository: DataRepositoryPort = Depends(Provide[Container.data_repository]),
) -> models.SampleAuthDetails:
    """Posts a new sample to the database"""
    return await data_repository.create_sample(sample_creation=data)


# PATCH /sample
@sample_router.patch(
    "/samples",
    status_code=204,
    summary="Update an existing sample's test results",
    response_model=None,
)
@inject
async def update_sample(
    updates: models.SampleUpdate,
    data_repository: DataRepositoryPort = Depends(Provide[Container.data_repository]),
    authorization: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    """Updates an existing sample"""
    access_token = authorization.credentials

    try:
        await data_repository.update_sample(updates=updates, access_token=access_token)
    except DataRepositoryPort.SampleNotFoundError as err:
        raise HTTPException(status_code=404, detail=MSG_NOT_FOUND) from err
    except DataRepositoryPort.UnauthorizedRequestError as err:
        raise HTTPException(status_code=403, detail=MSG_UNAUTHORIZED) from err
