import pytest

from db.models import UserData

CREATE_URL = "/api/v1/drugfreekerala/create/"
GET_URL = "/api/v1/drugfreekerala/get/"

# A real entry from https://mulearn.org/api/v1/register/colleges/
COLLEGE_ID = "02488535-1599-459f-adab-f3ef8fee2281"
COLLEGE_NAME = "GOVERNMENT COLLEGE NEDUMANGAD"


def pledge(**fields):
    return {"name": "Anjali Nair", "email": "anjali@example.com", **fields}


def stored_college(db):
    """(is_student, college_id, college_name) of the only stored pledge."""
    with db() as session:
        user = session.query(UserData).one()
        return user.is_student, user.college_id, user.college_name


def test_student_from_college_list_stores_id_and_name(client, db):
    response = client.post(
        CREATE_URL, json=pledge(is_student=True, college_id=COLLEGE_ID, college_name=COLLEGE_NAME)
    )

    assert response.status_code == 200
    assert stored_college(db) == (True, COLLEGE_ID, COLLEGE_NAME)


def test_student_choosing_other_stores_typed_name_without_id(client, db):
    response = client.post(
        CREATE_URL, json=pledge(is_student=True, college_name="St. Joseph's HSS, Kollam")
    )

    assert response.status_code == 200
    assert stored_college(db) == (True, None, "St. Joseph's HSS, Kollam")


def test_non_student_is_stored_as_false_with_no_college(client, db):
    response = client.post(CREATE_URL, json=pledge(is_student=False))

    assert response.status_code == 200
    assert stored_college(db) == (False, None, None)


def test_pledge_without_student_answer_is_still_accepted(client, db):
    """The frontend that is live today sends only name and email."""
    response = client.post(CREATE_URL, json=pledge())

    assert response.status_code == 200
    assert stored_college(db) == (None, None, None)


def test_college_name_is_trimmed(client, db):
    client.post(CREATE_URL, json=pledge(is_student=True, college_name="  Govt College  "))

    assert stored_college(db) == (True, None, "Govt College")


@pytest.mark.parametrize(
    "fields",
    [
        pytest.param({"is_student": True}, id="student without college"),
        pytest.param({"is_student": True, "college_id": COLLEGE_ID}, id="student with id but no name"),
        pytest.param({"is_student": True, "college_name": "   "}, id="student with blank college"),
        pytest.param({"is_student": True, "college_name": "x" * 256}, id="college name too long"),
        pytest.param(
            {"is_student": True, "college_id": "not-a-uuid", "college_name": COLLEGE_NAME},
            id="malformed college id",
        ),
        pytest.param({"is_student": False, "college_name": COLLEGE_NAME}, id="non-student with college"),
        pytest.param({"is_student": False, "college_id": COLLEGE_ID}, id="non-student with college id"),
        pytest.param({"college_name": COLLEGE_NAME}, id="college without student answer"),
    ],
)
def test_inconsistent_college_fields_are_rejected(client, db, fields):
    response = client.post(CREATE_URL, json=pledge(**fields))

    assert response.status_code == 422
    with db() as session:
        assert session.query(UserData).count() == 0


def test_create_returns_the_new_record_without_college(client):
    response = client.post(
        CREATE_URL, json=pledge(is_student=True, college_id=COLLEGE_ID, college_name=COLLEGE_NAME)
    )

    assert response.json() == {
        "message": "User created",
        "id": 1,
        "name": "Anjali Nair",
        "email": "anjali@example.com",
    }


def test_existing_pledges_are_returned_without_college(client):
    """Anyone can query any email (audit finding B2), so college must not leak."""
    client.post(CREATE_URL, json=pledge(is_student=True, college_id=COLLEGE_ID, college_name=COLLEGE_NAME))

    duplicate = client.post(CREATE_URL, json=pledge(is_student=False))
    lookup = client.get(GET_URL, params={"email": "anjali@example.com"})

    record = {"id": 1, "name": "Anjali Nair", "email": "anjali@example.com"}
    assert duplicate.json() == {"message": "User already exists", "is_error": True, **record}
    assert lookup.json() == record
