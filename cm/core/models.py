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

from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class SampleStatus(str, Enum):
    """Enumeration for Sample status values"""

    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class SampleTestResult(str, Enum):
    """Enumeration for Sample test_result values"""

    INCONCLUSIVE = "inconclusive"
    POSITIVE = "positive"
    NEGATIVE = "negative"


class SampleCreation(BaseModel):
    """Pydantic model to perform validation on new submission data.
    This is separate from the Sample model to prevent someone from submitting
    their own access token.
    """

    patient_pseudonym: str = Field(..., min_length=11, max_length=63)
    submitter_email: EmailStr
    collection_date: str = Field(..., regex=r"^\d{4}(-\d{2}){2}T\d{2}:\d{2}[zZ]?$")


class SampleFullCreation(SampleCreation):
    """This appends the test data fields: status, test_result, and test_date"""

    status: SampleStatus = SampleStatus.PENDING
    test_result: SampleTestResult = SampleTestResult.INCONCLUSIVE
    test_date: str = Field(default="", regex=r"^(\d{4}(-\d{2}){2}T\d{2}:\d{2}[zZ]?)?$")

    class Config:
        """Fields not required, so force validation on assignment"""

        validate_assignment = True


class Sample(SampleFullCreation):
    """SampleFullCreation plus a hashed access token for authorizing access, and an ID"""

    sample_id: str
    access_token_hash: bytes


class SampleAuthDetails(Sample):
    """Sample objects containing the plaintext access_token"""

    access_token: str = Field(default=..., regex=r"^[a-zA-Z0-9]*$")


class SampleUpdate(BaseModel):
    """Update class for Sample"""

    sample_id: str = ""
    status: SampleStatus
    test_result: SampleTestResult
    # the regex is slightly different: The date is considered mandatory here
    test_date: str = Field(..., regex=r"\d{4}(-\d{2}){2}T\d{2}:\d{2}[zZ]?")
