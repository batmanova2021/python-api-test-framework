import pytest

pytestmark = pytest.mark.jsonplaceholdertest


@pytest.mark.smoke
def test_validate_response_code(jsonplaceholder_api):
    response = jsonplaceholder_api.get("/posts")
    assert response.status_code == 200
    assert response.headers["Content-Type"].split(";")[0] == "application/json"


@pytest.mark.regression
def test_validate_userid_and_id(jsonplaceholder_api, validate_schema):
    response = jsonplaceholder_api.get("/posts")
    assert response.status_code == 200
    assert response.headers["Content-Type"].split(";")[0] == "application/json"
    data = response.json()
    validate_schema(data, "posts_list_schema.json")
    assert data[0]["userId"] == 1
    assert data[0]["id"] == 1
