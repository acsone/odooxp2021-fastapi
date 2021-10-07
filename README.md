# FastAPI with Odoo backend demo

This repository accompanies Stéphane Bidoul's [Odoo Experience 2021 Talk](https://youtu.be/tFpezjMGdNc).

The first ~10 commits follow the talk structure and build the demo from the ground up.

To install, first create a python virtual environment, and install the dependencies in
it (including Odoo 15):

```console
$ python3 -m venv .venv
$ .venv/bin/python3 -m pip install requirements.txt
```

*Note*: this command will be slow as it will do a `git clone` of Odoo into
`.venv/src/odoo`. If you already have a local copy of the Odoo 15.0 source code, feel
free to update the `odoo` line in `requirements.txt` to make it point to your local copy
instead of the GitHub URL.

Then create an `odoo.cfg` configuration file with `db_name` set in the `[options]`
section:

```ini
[options]
db_name=odoo_fastapi_demo_15
```

Initialize a regular Odoo database with the contacts app installed:

```console
$ env ODOO_RC=odoo.cfg .venv/bin/odoo -o contacts --stop-after-init
```

You can then run the demo application server using:

```console
$ env ODOO_RC=odoo.cfg .venv/bin/python3 -m uvicorn odoo_fastapi_demo:app
```

And finally, you can browse the OpenAPI documentation at `http://127.0.0.1:8000/docs`,
and test the API endpoints using the `Try it out` buttons.

To run the tests, use:

```console
$ env ODOO_RC=odoo.cfg python -m pytest tests/ -v
```
