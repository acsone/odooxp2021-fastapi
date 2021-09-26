# Copyright (c) 2021 ACSONE SA/NV

def test_get_partners(test_client):
    response = test_client.get("/partners")
    assert response.ok
    assert len(response.json()) > 1
    assert response.json()[0]["name"]


def test_create_and_get_partner(test_client):
    response = test_client.post(
        "/partners",
        json={"name": "Toto Le Héro", "email": "toto@example.com"},
    )
    assert response.ok
    partner_id = response.json()["id"]
    response = test_client.get(f"/partners/{partner_id}")
    assert response.ok
    assert response.json() == {
        "id": partner_id,
        "name": "Toto Le Héro",
        "email": "toto@example.com",
        "is_company": False,
    }
