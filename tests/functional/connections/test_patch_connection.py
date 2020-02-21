from http import HTTPStatus

from tests.factories import PersonFactory

from connections.models.connection import Connection


def test_patch_connection(db, testapp):
    person_from = PersonFactory(first_name='Sally')
    person_to = PersonFactory(first_name='Harry')
    db.session.commit()
    payload = {
        'from_person_id': person_from.id,
        'to_person_id': person_to.id,
        'connection_type': 'mother',
    }
    res = testapp.post('/connections', json=payload)

    assert res.status_code == HTTPStatus.CREATED

    assert 'id' in res.json

    # Now Patch!
    payload = {
        'connection_type': 'friend'
    }
    res = testapp.patch('/connections/' + str(res.json['id']), json=payload)

    connection = Connection.query.get(res.json['id'])

    assert connection is not None
    assert connection.from_person_id == person_from.id
    assert connection.to_person_id == person_to.id
    assert connection.connection_type.value == 'friend'


# TODO: Test failure conditions for invalid connection id, connection_type (xfailed?)
