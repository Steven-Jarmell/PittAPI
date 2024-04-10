"""
The Pitt API, to access workable data of the University of Pittsburgh
Copyright (C) 2015 Ritwik Gupta

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

from typing import List, NamedTuple
import requests

# Need to make unverified requests to Pitt endpoint
import urllib3
urllib3.disable_warnings()

PITT_BASE_URL = "https://pitt-keyserve-prod.univ.pitt.edu/maps/std/"

class Lab(NamedTuple):
    name: str
    status: str
    available_computers: int
    total_computers: int

def _fetch_all_lab_ids() -> List[str]:
    """Fetches the id for all labs."""
    res = requests.get(PITT_BASE_URL + 'avail.json', verify=False).json()
    labs_info = res["results"]["maps"]

    lab_ids = []
    for lab in labs_info:
        lab_ids.append(lab["ident"])

    return lab_ids

def _fetch_lab_data(id: str) -> List[str]:
    """Fetches text of status/machines of a single labs."""
    pass

def _fetch_all_lab_data() -> List[str]:
    """Fetches text of status/machines of all labs."""
    pass

def get_one_lab_status() -> List[Lab]:
    """Returns a dictionary with status and amount of OS machines for one lab."""
    pass

def get_all_labs_status() -> List[Lab]:
    """Returns a dictionary with status and amount of OS machines for all labs."""
    pass
