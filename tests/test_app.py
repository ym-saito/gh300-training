import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # 新規参加者
    activity = "Chess Club"
    email = "pytestuser@mergington.edu"

    # まず登録解除（前回のテスト残り対策）
    client.post(f"/activities/{activity}/unregister", params={"email": email})

    # サインアップ
    res_signup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res_signup.status_code == 200
    assert f"Signed up {email}" in res_signup.json()["message"]

    # 参加者リストに含まれるか
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

    # 登録解除
    res_unreg = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert res_unreg.status_code == 200
    assert f"Unregistered {email}" in res_unreg.json()["message"]

    # 参加者リストから消えているか
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
