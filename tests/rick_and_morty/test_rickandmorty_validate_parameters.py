import pytest


@pytest.mark.rickandmorty
@pytest.mark.regression
def test_parameters_query_request(rick_and_morty_api):
    name = "Rick"
    status = "Alive"
    res = rick_and_morty_api.get("/character", params={"name": name, "status": status})
    assert res.status_code == 200
    assert res.headers["Content-Type"].split(";")[0] == "application/json"
    json_data = res.json()
    assert json_data["results"][0]["name"] == "Rick Sanchez"
    assert json_data["results"][0]["id"] == 1
    assert json_data["results"][0]["species"] == "Human"
    assert json_data["results"][0]["status"] == "Alive"
    assert json_data["info"]["pages"] == 2
