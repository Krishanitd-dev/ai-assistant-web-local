import os
import pytest
from fastapi.testclient import TestClient
os.environ["DATABASE"] = "test_conversation.db"
from app.main import app
from app.database import create_table


client = TestClient(app, follow_redirects=False)


def test_registration_success():
    response = client.post(
        "/register",
        data={
            "email": "testuser2@example.com",
            "password": "Password123",
            "confirm_password": "Password123"
        }
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/"


def test_duplicate_email_rejected():
    client.post(
        "/register",
        data={
            "email": "duplicate1@example.com",
            "password": "Password123",
            "confirm_password": "Password123"}
    )


    response = client.post(
        "/register",
        data={
            "email": "duplicate1@example.com",
            "password": "Password123",
            "confirm_password": "Password123"}
    )

    assert response.status_code == 200
    assert "Email already registered." in response.text


def test_login_correct_password():
    client.post(
        "/register",
        data={
            "email": "loginuser2@example.com",
            "password": "Password123",
            "confirm_password": "Password123"}
    )


    response = client.post(
        "/login",
        data={"email": "loginuser2@example.com", "password": "Password123"}
    )

    assert response.status_code == 303
    assert response.headers["location"] == "/ask"


def test_login_incorrect_password():
    client.post("/register",
        data={
            "email": "wrongpassword2@example.com",
            "password": "Password123",
            "confirm_password": "Password123"}
    )

    response = client.post("/login",
        data={
            "email": "wrongpassword2@example.com",
            "password": "WrongPassword123"}
    )

    assert response.status_code == 200
    assert "Invalid email or password." in response.text

def test_user_access():

    client.post(
        "/register",
        data={
            "email": "usera1@example.com",
            "password": "Password123",
            "confirm_password": "Password123"
        }
    )

    login_response = client.post(
        "/login",
        data={
            "email": "usera1@example.com",
            "password": "Password123"
        }
    )

    print("LOGIN STATUS:", login_response.status_code)
    print("LOGIN LOCATION:", login_response.headers.get("location"))

    response = client.post(
        "/ask",
        data={
            "question": "This is User A's private question"
        }
    )

    print("ASK STATUS:", response.status_code)

    from app.database import get_all_conversations

    conversations = get_all_conversations("usera1@example.com")

    print("USER A DATABASE:", conversations)

    response = client.get("/history")

    print("HISTORY STATUS:", response.status_code)
    print("QUESTION IN HTML:", "This is User A's private question" in response.text)

    assert response.status_code == 200
    assert "This is User A's private question" in response.text