from http import HTTPStatus

from tests.factories import ConnectionFactory

from connections.models.connection import Connection

EXPECTED_FIELDS = [
    'id',
    'from_person_id',
    'from_person',
    'to_person_id',
    'to_person',
    'connection_type'
]

EXPECTED_PERSON_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'email',
]


def test_get_connections(db, testapp):
    ConnectionFactory.create_batch(3)
    db.session.commit()

    res = testapp.get('/connections')

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 3
    for connection in res.json:
        for field in EXPECTED_FIELDS:
            assert field in connection
        for field in EXPECTED_PERSON_FIELDS:
            assert field in connection['from_person']
        for field in EXPECTED_PERSON_FIELDS:
            assert field in connection['to_person']