import pytest
from flask_login import current_user
from app import create_app, db

@pytest.fixture()
def app():
    app = create_app(config_name='test')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def register_user(client):
    with client:
        client.post('/register', data={'username': 'test', 'email': 'test@gmail.com',  'password': '123456', "confirm_password": '123456'},
                    follow_redirects=True)

@pytest.fixture
def login_user(client):
    with client:
        client.post('/login', data={'email': 'test@gmail.com',  'password': '123456', 'remember': True}, 
                    follow_redirects=True)

@pytest.fixture
def create_cat(client, register_user, login_user):
    client.post('/category/create', data={'name': 'Football'}, 
                follow_redirects=True)


@pytest.fixture
def create_task(client, register_user, login_user, create_cat):
    data = {
        'title': 'Test Title',  
        'description': 'Test desc', 
        'deadline': '2022-12-22',
        'priority': 1,
        'progress': 1,
        'category': 1
    }
    resp = client.post('/task/create', data=data, 
                follow_redirects=True)


def test_setup(client):
    assert client is not None
    

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Yevhen Brusak' in response.data


def test_user_register_login(client):
    with client:
            resp = client.post('/register', data={'username': 'test', 'email': 'test@test.com',  'password': '11111111Ab', "confirm_password": '11111111Ab'}, 
                follow_redirects=True)
            assert resp.status_code == 200
            assert 'Login' in resp.get_data(as_text=True)
            resp = client.post('/login', data={'email': 'test@test.com',  'password': '11111111Ab', 'remember': 'y'}, 
                follow_redirects=True)
            assert resp.status_code == 200
            assert current_user.username == "test"
            resp = client.get('logout', follow_redirects=True)
            assert resp.status_code == 200
            assert current_user.is_anonymous       


def test_task_create(client, create_cat):
    data = {
        'title': 'Test Title',  
        'description': 'Test desc', 
        'deadline': '2022-12-22',
        'priority': 1,
        'progress': 1,
        'category': 1
    }
    resp = client.post('/task/create', data=data, 
                follow_redirects=True)
    
    assert "Task created!" in resp.get_data(as_text=True)

def test_list_tasks(client, create_task):
    resp = client.get('/task', follow_redirects=True)

    assert 'Test Title' in resp.get_data(as_text=True)

def test_detail_task(client, create_task):
    resp = client.get('/task/1', follow_redirects=True)
    assert 'Test desc' in resp.get_data(as_text=True)

def test_task_update(client, create_task):
    data = {
        'title': 'Test Title2',  
        'description': 'Test desc2', 
        'deadline': '2022-12-22',
        'priority': 1,
        'progress': 1,
        'category': 1
    }
    resp = client.post('/task/1/update', data=data, follow_redirects=True)
    assert 'Test desc2' in resp.get_data(as_text=True)


def test_task_delete(client, create_task):
    resp = client.post('/task/1/delete', follow_redirects=True)
    assert 'Test Title' not in resp.get_data(as_text=True)
