# Copyright (c) 2021 ACSONE SA/NV

import odoo
from odoo.api import Environment


def odoo_env() -> Environment:
    #
    # /!\ With Odoo < 15 you need to wrap all this in 'with
    #     Environment.manage()' and apply this Odoo patch:
    #     https://github.com/odoo/odoo/pull/70398, to properly handle context
    #     locals in an async program.
    #
    # check_signaling() is to refresh the registry and cache when needed.
    registry = odoo.registry(odoo.tools.config["db_name"]).check_signaling()
    # manage_change() is to signal other instances when the registry or cache
    # needs refreshing.
    with registry.manage_changes():
        # The cursor context manager commits unless there is an exception.
        with registry.cursor() as cr:
            yield Environment(cr, odoo.SUPERUSER_ID, {})
