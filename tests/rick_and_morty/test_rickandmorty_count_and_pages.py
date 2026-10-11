import pytest


@pytest.mark.rickandmorty
@pytest.mark.regression
def test_validate_get_response_code(rick_and_morty_api):
    res = rick_and_morty_api.get("/character", params={"name": "rick", "status": "alive"})
    assert res.status_code == 200
    assert res.headers["Content-Type"].split(";")[0] == "application/json"
    json_data = res.json()
    assert json_data["info"]["count"] == 26
    assert json_data["info"]["pages"] == 2
