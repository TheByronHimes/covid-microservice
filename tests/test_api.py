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

from covid_microservice.api import router
from covid_microservice.models import PcrTest


def test_post_sample():
    """Test the /sample POST function"""
    pcr_test = PcrTest(
        patient_pseudonym="test test test",
        submitter_email="test@test.com",
        collection_date="2022-08-21T11:18",
    )

    obj = router.post_sample(pcr_test)
    assert isinstance(obj, dict)
    assert "sample_id" in obj
    assert "access_token" in obj
    assert len(obj.keys()) == 2
