def test_home_route(app):
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Hello World!"}
