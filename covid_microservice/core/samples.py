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
#
"""Helper functions related to covid test sample data
that might get moved or replaced by something else."""
from ..dao import Dao
from ..models import PcrTest


def help_find_sample(access_token: str, dao: Dao) -> PcrTest:
    """Find sample"""
    return dao.find_one({"access_token": access_token})


def help_update_sample(access_token: str, new_data: PcrTest, dao: Dao) -> PcrTest:
    """Update sample"""
    result = dao.update_one({"access_token": access_token}, new_data)
    return result
