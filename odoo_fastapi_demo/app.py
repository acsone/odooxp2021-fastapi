# Copyright (c) 2021 ACSONE SA/NV

from typing import Optional, List

from fastapi import FastAPI, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from pydantic import BaseModel

import odoo


app = FastAPI(title="FastAPI with Odoo Demo")


@app.on_event("startup")
def initialize_odoo() -> None:
    # Read Odoo config from $ODOO_RC.
    odoo.tools.config.parse_config([])



class Partner(BaseModel):
    id: Optional[int]
    name: str
    email: Optional[str]
    is_company: bool = False


tom = Partner(id=1, name="Tom", email="tom@wb.com")


@app.get("/partners", response_model=List[Partner])
def partners():
    return [
        tom,
        Partner(id=2, name="Jerry", email="jerry@wb.com"),
        dict(id=3, name="Warner Bros", email="info@wb.com", is_company=True),
    ]


@app.get("/partners/{partner_id}", response_model=Partner)
def get_partner(partner_id: int):
    if partner_id == 1:
        return tom
    raise HTTPException(status_code=HTTP_404_NOT_FOUND)


@app.post("/partners", response_model=Partner, status_code=HTTP_201_CREATED)
def create_partner(partner: Partner):
    return partner
