# Copyright (c) 2021 ACSONE SA/NV

from typing import Optional, List

from fastapi import FastAPI, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from pydantic import BaseModel

import odoo
from odoo.api import Environment
from odoo.models import Model
from odoo.exceptions import AccessError, MissingError

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


@app.get("/partners", response_model=List[Partner])
def partners(is_company: Optional[bool] = None, env: Environment = Depends(odoo_env)):
    domain = []
    if is_company is not None:
        domain.append(("is_company", "=", is_company))
    partners = env["res.partner"].search(domain)
    return [Partner.from_res_partner(p) for p in partners]



@app.get("/partners/{partner_id}", response_model=Partner)
def get_partner(partner_id: int, env: Environment = Depends(odoo_env)):
    try:
        partner = env["res.partner"].browse(partner_id)
        return Partner.from_res_partner(partner)
    except MissingError:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    except AccessError:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN)


@app.post("/partners", response_model=Partner, status_code=HTTP_201_CREATED)
def create_partner(partner: Partner, env: Environment = Depends(odoo_env)):
    partner = env["res.partner"].create(
        {
            "name": partner.name,
            "email": partner.email,
            "is_company": partner.is_company,
        }
    )
    return Partner.from_res_partner(partner)
