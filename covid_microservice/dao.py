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
""" Holds DAO classes, including Dao Protocol class"""

from typing import Any, Dict, Mapping, Protocol, Type, runtime_checkable

from .models import Dto


@runtime_checkable
class Dao(Protocol):
    """Protocol/Port of a generic DAO"""

    def find_one(self, filters: Mapping[str, Any]) -> Dto:
        """Find one item"""

    def insert_one(self, obj: Dto) -> Any:
        """Insert one item"""

    def update_one(self, filters: Mapping[str, Any], replacement: Dto) -> Any:
        """Update one item"""

    def delete_one(self, filters: Mapping[str, Any]) -> Any:
        """Delete one item"""


class MongoDummyDao:
    """A temporary dummy DAO Implementation specifically for MongoDB"""

    def __init__(self, dto_type: Type[Dto], id_field: str):
        self.dto_type = dto_type
        self.db: Dict[Any, Any] = {}
        self.id_field = id_field

    def _dto_to_document(self, dto):
        document = dto.dict()
        return document

    def _document_to_dto(self, document):
        if "_id" in document:
            document.pop("_id")
        return self.dto_type(**document)

    def find_by_key(self, key: int):
        """Direct lookup by key"""
        return self._document_to_dto(self.db[key])

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
        _id = document[self.id_field]
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
