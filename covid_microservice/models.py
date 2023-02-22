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
from typing import Any, Dict, List, Literal, Mapping, Type, Union

from pydantic import BaseModel, Field

from .api.ancillary import make_sample_id

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


#


class Dto(BaseModel):
    """Base Dto Class"""

    def dictify(self, fields: Union[List[str], None]) -> Dict:
        """Returns a dictionary version of the object with only specified fields"""
        if fields is None:
            fields = self.__fields__
        return {k: getattr(self, k) for k in fields}


class PcrTest(Dto):
    """Simple DTO for the PCR tests"""

    #  DO: proper enumeration on status and test result fields
    patient_pseudonym: str
    submitter_email: str
    collection_date: str
    sample_id: str = ""
    access_token: str = ""
    status: str = ""
    test_result: str = ""
    test_date: str = ""

    class Config:
        """Config options for this class"""

        validate_assignment = True


class UpdatePcrTest(Dto):
    """Update DTO for PcrTest"""

    # DO: proper validation on the date fields
    # DO: proper enumeration on status and test result fields
    access_token: str
    status: str = ""
    test_result: str = ""
    test_date: str = ""


class MongoDao:
    """A dummy DAO Implementation specifically for MongoDB so errors shut up"""

    def __init__(self, dto_type: Type[Dto]):
        self.dto_type = dto_type
        self.db: Dict[Any, Any] = {}

    def _dto_to_document(self, dto):
        document = dto.dict()
        return document

    def _document_to_dto(self, document):
        document.pop("_id")
        return self.dto_type(**document)

    def find_one(self, filters: Mapping[str, Any]):
        """Find first item that matches criteria"""
        for obj in self.db.values():
            for fkey, fval in filters.items():
                if obj[fkey] != fval:
                    #  no match
                    break
            else:
                # all values matched, procede with find
                return self._document_to_dto(obj)
        return {}

    def insert_one(self, obj):
        """Insert one item"""
        document = self._dto_to_document(obj)
        _id = make_sample_id()
        self.db[_id] = document
        return _id

    def update_one(self, filters: Mapping[str, Any], replacement: Dto):
        """Update given item"""
        replacement_doc = self._dto_to_document(replacement)
        for key, obj in self.db.items():
            for fkey, fval in filters.items():
                if obj[fkey] != fval:
                    #  no match
                    break
            else:
                # all values matched, procede with replacement
                self.db[key] = replacement_doc
                break
        else:
            return {}
        return replacement

    def delete_one(self, filters: Mapping[str, Any]):
        """Delete an item"""
        for key, obj in self.db.items():
            for fkey, fval in filters.items():
                if obj[fkey] != fval:
                    #  no match
                    break
            else:
                # all values matched, procede with deletion
                self.db.pop(key)
                return True
        return False
