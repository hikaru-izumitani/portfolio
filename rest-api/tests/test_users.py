def test_empty_collection_returns_404(app):
    response = app.test_client().get("/users")
    assert response.status_code == 404
    assert response.json["error"] == "User not found"


def test_create_and_list_users(app):
    client = app.test_client()
    first = client.post("/users", json={"name": "Ada", "email": "ada@example.com"})
    second = client.post("/users", json={"name": "Grace", "email": "grace@example.com"})

    assert first.status_code == 200
    assert first.json["name"] == "Ada"
    assert first.json["email"] == "ada@example.com"
    assert first.json["message"] == "User created successfully."
    assert first.json["id"]

    listed = client.get("/users")
    assert listed.status_code == 200
    names = [user["name"] for user in listed.json]
    assert names == ["Ada", "Grace"] or set(names) == {"Ada", "Grace"}
    assert first.json["id"] != second.json["id"]


def test_duplicate_email_returns_400(app):
    client = app.test_client()
    payload = {"name": "Ada", "email": "ada@example.com"}
    assert client.post("/users", json=payload).status_code == 200
    duplicate = client.post("/users", json=payload)
    assert duplicate.status_code == 400
    assert duplicate.json["error"] == "the email is already in use"


def test_invalid_or_missing_create_fields(app):
    client = app.test_client()
    missing_email = client.post("/users", json={"name": "Ada"})
    missing_name = client.post("/users", json={"email": "ada@example.com"})
    empty_email = client.post("/users", json={"name": "Ada", "email": ""})
    numeric_email = client.post("/users", json={"name": "Ada", "email": 12345678})
    bad_email = client.post("/users", json={"name": "Ada", "email": "adaexample.com"})

    assert missing_email.status_code == 400
    assert missing_email.json["error"] == "email is required"
    assert missing_name.status_code == 400
    assert missing_name.json["error"] == "name is required"
    assert empty_email.status_code == 400
    assert empty_email.json["error"] == "Invalid email format"
    assert numeric_email.status_code == 400
    assert bad_email.status_code == 400
    assert bad_email.json["error"] == "Invalid email format"


def test_get_user_by_id(app):
    client = app.test_client()
    created = client.post("/users", json={"name": "Ada", "email": "ada@example.com"})
    user_id = created.json["id"]

    found = client.get(f"/users/{user_id}")
    assert found.status_code == 200
    assert found.json["id"] == user_id
    assert found.json["name"] == "Ada"
    assert found.json["email"] == "ada@example.com"

    missing = client.get("/users/missing")
    assert missing.status_code == 404
    assert missing.json["error"] == "User not found"


def test_patch_user(app):
    client = app.test_client()
    created = client.post("/users", json={"name": "Ada", "email": "ada@example.com"})
    user_id = created.json["id"]

    renamed = client.patch(f"/users/{user_id}", json={"name": "Ada Lovelace"})
    assert renamed.status_code == 200
    assert renamed.json["name"] == "Ada Lovelace"
    assert renamed.json["email"] == "ada@example.com"
    assert renamed.json["message"] == "User updated successfully."

    remailed = client.patch(f"/users/{user_id}", json={"email": "lovelace@example.com"})
    assert remailed.status_code == 200
    assert remailed.json["email"] == "lovelace@example.com"

    missing = client.patch("/users/missing", json={"name": "Grace"})
    assert missing.status_code == 404
    empty = client.patch(f"/users/{user_id}", json={})
    assert empty.status_code == 400
    assert empty.json["error"] == "No valid fields to update. You need name or email to update"
    invalid = client.patch(f"/users/{user_id}", json={"email": "not-an-email"})
    assert invalid.status_code == 400
    assert invalid.json["error"] == "Invalid email format"


def test_patch_and_put_reject_duplicate_email(app):
    client = app.test_client()
    client.post("/users", json={"name": "Ada", "email": "ada@example.com"})
    other = client.post("/users", json={"name": "Grace", "email": "grace@example.com"})
    user_id = other.json["id"]

    patched = client.patch(f"/users/{user_id}", json={"email": "ada@example.com"})
    assert patched.status_code == 400
    assert patched.json["error"] == "the email is already in use"

    replaced = client.put(f"/users/{user_id}", json={"name": "Grace", "email": "ada@example.com"})
    assert replaced.status_code == 400
    assert replaced.json["error"] == "the email is already in use"


def test_put_replaces_both_fields(app):
    client = app.test_client()
    created = client.post("/users", json={"name": "Ada", "email": "ada@example.com"})
    user_id = created.json["id"]

    replaced = client.put(f"/users/{user_id}", json={"name": "Grace", "email": "grace@example.com"})
    assert replaced.status_code == 200
    assert replaced.json["name"] == "Grace"
    assert replaced.json["email"] == "grace@example.com"
    assert replaced.json["message"] == "User updated successfully."

    name_only = client.put(f"/users/{user_id}", json={"name": "Grace"})
    email_only = client.put(f"/users/{user_id}", json={"email": "grace@example.com"})
    empty = client.put(f"/users/{user_id}", json={})
    invalid = client.put(f"/users/{user_id}", json={"name": "Grace", "email": "not-an-email"})
    missing = client.put("/users/missing", json={"name": "Grace", "email": "grace@example.com"})

    assert name_only.status_code == 400
    assert name_only.json["error"] == "You need email to update."
    assert email_only.status_code == 400
    assert email_only.json["error"] == "You need name to update."
    assert empty.status_code == 400
    assert empty.json["error"] == "No valid fields to update. You need name and email."
    assert invalid.status_code == 400
    assert invalid.json["error"] == "Invalid email format"
    assert missing.status_code == 404
    assert missing.json["error"] == "User not found"


def test_delete_user(app):
    client = app.test_client()
    created = client.post("/users", json={"name": "Ada", "email": "ada@example.com"})
    user_id = created.json["id"]

    deleted = client.delete(f"/users/{user_id}")
    assert deleted.status_code == 200
    assert deleted.json["message"] == "User deleted successfully."
    assert client.get(f"/users/{user_id}").status_code == 404

    missing = client.delete("/users/missing")
    assert missing.status_code == 404
    assert missing.json["error"] == "User not found"
