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

"""Defines dataclasses for holding business-logic data"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Literal, Union

from pydantic import BaseModel, EmailStr, Field

SupportedLanguages = Literal["Greek", "Croatian", "French", "German"]


class MessageBase(BaseModel):
    """A message base container"""

    message: str = Field(..., description="The message content.")
    created_at: datetime = Field(
        ..., description="The date/time when the message was created"
    )


class GreetingBase(BaseModel):
    """A container for basic metadata on a greeting phrase/expression"""

    language: SupportedLanguages = Field(..., description="The language.")
    isinformal: bool = Field(
        ..., description="Is the expression used in informal contexts?"
    )


class GreetingExpression(GreetingBase):
    """A container for describing a greeting expression"""

    expression: str = Field(..., description="The actual greeting expression")


class Greeting(GreetingBase, MessageBase):
    """A container storing a greeting for a specfic person incl. metadata"""

    pass  # pylint: disable=unnecessary-pass


## *********************************************************
## *********************************************************
## *********************************************************


class Dto(BaseModel):
    """Base Dto Class"""

    def dictify(self, fields: Union[List[str], None] = None) -> Dict:
        """Returns a dictionary version of the object with only specified fields"""
        if fields is None:
            fields = list(self.__fields__.keys())
        return {k: getattr(self, k) for k in fields}


class StatusEnum(str, Enum):
    """Enumeration for PcrTest status values"""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class TestResultEnum(str, Enum):
    """Enumeration for PcrTest test_result values"""

    UNSET = ""
    POSITIVE = "positive"
    NEGATIVE = "negative"


class NewSampleSubmission(BaseModel):
    """Pydantic model to perform validation on new submission data.
    This is separate from the PcrTest to prevent someone from submitting
    their own access token.
    """

    patient_pseudonym: str = Field(..., min_length=11, max_length=63)
    submitter_email: EmailStr
    collection_date: str = Field(..., regex=r"^\d{4}(-\d{2}){2}T\d{2}:\d{2}[zZ]?$")


class PcrTest(Dto):
    """Simple DTO for the PCR tests"""

    patient_pseudonym: str = Field(..., min_length=11, max_length=63)
    submitter_email: EmailStr
    collection_date: str = Field(..., regex=r"^\d{4}(-\d{2}){2}T\d{2}:\d{2}[zZ]?$")
    sample_id: int = 0
    access_token: str = Field(default="", regex=r"^[a-zA-Z0-9]*$")
    status: StatusEnum = StatusEnum.PENDING
    test_result: TestResultEnum = TestResultEnum.UNSET
    test_date: str = Field(default="", regex=r"(^\d{4}(-\d{2}){2}T\d{2}:\d{2}[zZ]?$)?")

    class Config:
        """Config options for this class"""

        validate_assignment = True


class UpdatePcrTest(Dto):
    """Update DTO for PcrTest"""

    access_token: str = Field(..., regex=r"^[a-zA-Z0-9]*$")
    status: StatusEnum
    test_result: TestResultEnum
    # the regex is slightly different: The date is considered mandatory here
    test_date: str = Field(..., regex=r"\d{4}(-\d{2}){2}T\d{2}:\d{2}[zZ]?")
