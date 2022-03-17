
def test_read_home(client):
    response = client.get("api/v1/")
    assert response.status_code == 200