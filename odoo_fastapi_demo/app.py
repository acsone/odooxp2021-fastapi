# Copyright (c) 2021 ACSONE SA/NV

from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from pydantic import BaseModel

import odoo
from odoo.api import Environment
from odoo.models import Model

from .deps import odoo_env

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

    @classmethod
    def from_res_partner(cls, p: Model) -> "Partner":
        return Partner(id=p.id, name=p.name, email=p.email, is_company=p.is_company)


tom = Partner(id=1, name="Tom", email="tom@wb.com")


@app.get("/partners", response_model=List[Partner])
def partners(env: Environment = Depends(odoo_env)):
    partners = env["res.partner"].search([])
    return [Partner.from_res_partner(p) for p in partners]



@app.get("/partners/{partner_id}", response_model=Partner)
def get_partner(partner_id: int):
    if partner_id == 1:
        return tom
    raise HTTPException(status_code=HTTP_404_NOT_FOUND)


@app.post("/partners", response_model=Partner, status_code=HTTP_201_CREATED)
def create_partner(partner: Partner):
    return partner
