from http import HTTPStatus

import pytest
from tests.factories import ConnectionFactory, PersonFactory


@pytest.mark.xfail
def test_get_mutual_friends(db, testapp):
    instance = PersonFactory()
    target = PersonFactory()

    # some decoy connections (not mutual)
    ConnectionFactory.create_batch(5, to_person=instance)
    ConnectionFactory.create_batch(5, to_person=target)

    mutual_friends = PersonFactory.create_batch(3)
    for f in mutual_friends:
        ConnectionFactory(from_person=instance, to_person=f, connection_type='friend')
        ConnectionFactory(from_person=target, to_person=f, connection_type='friend')

    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person=instance, to_person=decoy, connection_type='coworker')
    ConnectionFactory(from_person=target, to_person=decoy, connection_type='coworker')

    db.session.commit()

    expected_mutual_friend_ids = [f.id for f in mutual_friends]

    # Trigger webservice call to get mutual friends
    res = testapp.get('/people/' + str(instance.id) + '/mutual_friends?target_id=' + str(target.id))

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 3

    for mutual_friend in res.json:
        assert mutual_friend.id in expected_mutual_friend_ids

    # Switch target/instance ids and make sure the resulting friends are the same
    res2 = testapp.get('/people/' + str(target.id) + '/mutual_friends?target_id=' +
                       str(instance.id))

    assert res2.status_code == HTTPStatus.OK

    assert len(res2.json) == 3

    for mutual_friend in res2.json:
        assert mutual_friend.id in expected_mutual_friend_ids
