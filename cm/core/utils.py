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


""" Ancillary functions, topic agnostic """

import secrets
import string


def random_string(num: int) -> str:
    """Produce a string containing num random numbers and letters"""
    chars = string.ascii_letters + string.digits
    return "".join([secrets.choice(chars) for _ in range(num)])


def make_access_token() -> str:
    """Method to return an access token string"""
    return random_string(16)
