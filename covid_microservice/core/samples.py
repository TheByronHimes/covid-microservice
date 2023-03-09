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
from typing import Any

from .models import PcrTest


# 'Any' will be replaced with Dao or Type[Dao] again as soon as possible
def help_find_sample(access_token: str, dao: Any) -> PcrTest:
    """Find sample"""
    return dao.find_one(mapping={"access_token": access_token})


def help_update_sample(dto: PcrTest, dao: Any) -> None:
    """Update sample"""
    # result = dao.update(mapping = {"access_token": access_token}, new_data)
    dao.update(dto=dto)
