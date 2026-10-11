import pytest


@pytest.mark.rickandmorty
@pytest.mark.smoke
def test_validate_get_response_code(rick_and_morty_api):
    response = rick_and_morty_api.get("/character")
    assert response.status_code == 200
