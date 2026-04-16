"""Tests for auth and operations endpoint helpers."""


def test_login_uses_auth_endpoint(mock_client, mock_response):
    mock_client.session.post.return_value = mock_response({"access_token": "abc"})

    result = mock_client.login("u@example.com", "secret")

    assert result["access_token"] == "abc"
    call = mock_client.session.post.call_args
    assert call.args[0].endswith("auth/login")


def test_change_password_uses_auth_endpoint(mock_client, mock_response):
    mock_client.session.post.return_value = mock_response({"status": "ok"})

    result = mock_client.change_password("old", "new")

    assert result["status"] == "ok"
    call = mock_client.session.post.call_args
    assert call.args[0].endswith("auth/change-password")


def test_upload_image_endpoint(mock_client, mock_response):
    mock_client.session.post.return_value = mock_response({"url": "https://cdn/image.png"})

    result = mock_client.upload_image({"file": "base64"})

    assert result["url"].endswith("image.png")
    call = mock_client.session.post.call_args
    assert call.args[0].endswith("upload/image")
