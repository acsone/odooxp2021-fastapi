# Copyright (c) 2021 ACSONE SA/NV

import pytest
from fastapi.testclient import TestClient

import odoo
from odoo.api import Environment

from odoo_fastapi_demo import app, deps


@pytest.fixture(scope="session")
def registry():
    odoo.tools.config.parse_config([])
    return odoo.registry(odoo.tools.config["db_name"])


@pytest.fixture()
def env(registry):
    with registry.cursor() as cr:
        try:
            yield Environment(cr, odoo.SUPERUSER_ID, {})
        finally:
            cr.rollback()


@pytest.fixture()
def test_client(env):
    # Make sure the app uses the same Environment as the test
    # so data created in test is visible in app functions.
    def test_odoo_env():
        env.cr.flush()
        env.clear()
        return env

    app.dependency_overrides[deps.odoo_env] = test_odoo_env
    yield TestClient(app)
    app.dependency_overrides = {}
