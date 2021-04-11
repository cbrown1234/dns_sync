from functools import partial

import pytest as pytest
from fastapi.testclient import TestClient

from app import models
from app.database import _get_fastapi_sessionmaker, get_db
from app.main import app

TEST_SQLALCHEMY_DATABASE_URL = 'sqlite:///.test.db?check_same_thread=False'

override_get_db = partial(get_db, db_url=TEST_SQLALCHEMY_DATABASE_URL)
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope='session', autouse=True)
def setup_database():

    session_maker = _get_fastapi_sessionmaker(TEST_SQLALCHEMY_DATABASE_URL)
    models.Base.metadata.bind = session_maker.cached_engine
    models.Base.metadata.create_all()

    yield

    models.Base.metadata.drop_all()


def test_read_main():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'Running'}


def test_get_dns_records_start_empty():
    response = client.get('/dns-records')
    assert response.status_code == 200
    assert response.json() == []


record = {
    'type': 'CNAME',
    'name': 'test.example.com',
    'content': '0.0.0.0',
    'ttl': '1',
    'proxied': True,
    'owner': 'test',
}


def test_upsert_dns_record():
    response = client.patch('/dns-records', json=record)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == record


def test_get_dns_records():
    response = client.get('/dns-records')
    assert response.status_code == 200
    assert response.json() == [dict(to_delete=False, **record)]


def test_delete_dns_record():
    response = client.delete('/dns-records/test.example.com')
    assert response.status_code == 200
    assert response.json() == {'deleted': True}


def test_get_dns_records_end_empty():
    response = client.get('/dns-records')
    assert response.status_code == 200
    assert response.json() == [dict(to_delete=True, **record)]
