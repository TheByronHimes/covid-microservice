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

"""Interface for an authorizer class, which can generate, hash, and validate tokens."""

import secrets
import string
from abc import ABC, abstractmethod

import bcrypt


class AuthorizerInterface(ABC):
    """Describes an object that can perform basic authorization-related tasks"""

    @abstractmethod
    def generate_token(self, *, length: int) -> str:
        """Produce a string containing "length" random numbers and letters"""

    @abstractmethod
    def hash_token(self, *, token: str) -> bytes:
        """Returns a hashed token for storage in the database"""

    @abstractmethod
    def check_token(self, *, token_plain: str, token_hashed: bytes) -> bool:
        """Compares a plaintext and hashed token to see if they are equivalent"""


class Authorizer(AuthorizerInterface):
    """Implementation of an AuthorizerPort"""

    def generate_token(self, *, length: int) -> str:
        """Produce a string containing "length" random numbers and letters"""
        chars = string.ascii_letters + string.digits
        return "".join([secrets.choice(chars) for _ in range(length)])

    def hash_token(self, *, token: str) -> bytes:
        token_bytes = bytes(token, encoding="utf-8")
        return bcrypt.hashpw(token_bytes, bcrypt.gensalt())

    def check_token(self, *, token_plain: str, token_hashed: bytes) -> bool:
        token_plain_bytes = bytes(token_plain, encoding="utf-8")
        return bcrypt.checkpw(token_plain_bytes, token_hashed)
