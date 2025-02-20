import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app  # FastAPI 애플리케이션 객체 가져오기
from models import User
from auth import pwd_context, create_token

client = TestClient(app)

@pytest.fixture
def mock_db():
    """가짜 DB 세션을 제공하는 Fixture"""
    return MagicMock()

### 🚀 회원가입 테스트
@pytest.mark.parametrize("username, password, email ,expected_status", [
    ("newuser1", "securePass123!", "new@new.com" ,200,),
    ("newuser2", "Mypassword!", "new1@new.com", 200, ),
    ("existinguser", "anypassword","new@new.com" ,400,),
])
@patch("auth.get_db")
@patch("auth.pwd_context.hash")
def test_register(mock_hash, mock_get_db, username,email, password, expected_status,):
    """ 회원가입 테스트 """
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db

    if username == "existinguser":
        mock_db.query.return_value.filter.return_value.first.return_value = User(username=username)
    else:
        mock_db.query.return_value.filter.return_value.first.return_value = None

    mock_hash.return_value = "hashed_password_example"

    response = client.post("/register", json={"username": username, "password": password,"email": email})

    assert response.status_code == expected_status


### 🚀 로그인 테스트
@pytest.mark.parametrize("username, password, expected_status", [
    ("user1", "password123", 200),
    ("user2", "securePass!", 200),
    ("user3", "wrongPass", 401),  # 잘못된 비밀번호
    ("unknownUser", "randomPass", 401),  # 존재하지 않는 사용자
])
@patch("auth.get_db")
@patch("auth.verify_password")
@patch("auth.creat_token")
def test_login(mock_create_token, mock_verify_password, mock_get_db, username, password, expected_status):
    """ 로그인 테스트 """
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    mock_user = User(username=username, password=pwd_context.hash("password123"))  # 가짜 유저 생성

    if username in ["user1", "user2"]:
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        mock_verify_password.return_value = password == "password123" or password == "securePass!"
        mock_create_token.return_value = "mocked_token"
    else:
        mock_db.query.return_value.filter.return_value.first.return_value = None
        mock_verify_password.return_value = False

    response = client.post("/login", json={"username": username, "password": password})

    assert response.status_code == expected_status
    if expected_status == 200:
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
    else:
        assert response.json()["detail"] == "Invalid username or password"

### 🚀 프로필 조회 테스트
@pytest.mark.parametrize("username, expected_status", [
    ("user1", 200),
    ("user2", 200),
    ("invalid_user", 401),  # 잘못된 토큰
])
@patch("auth.get_db")
@patch("auth.jwt.decode")
def test_get_profile(mock_jwt_decode, mock_get_db, username, expected_status):
    """ 프로필 조회 테스트 """
    mock_db = MagicMock()
    mock_get_db.return_value = mock_db
    mock_user = User(id=1, username=username)

    if username in ["user1", "user2"]:
        mock_jwt_decode.return_value = {"sub": username}
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        token = create_token({"sub": username})
    else:
        mock_jwt_decode.side_effect = Exception("Invalid token")
        token = "invalid_token"

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/profile", headers=headers)

    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json()["username"] == username
    else:
        assert response.json()["detail"] == "Invalid token"
