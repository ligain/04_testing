import datetime
import pytest

import api


class MockRequest(object):
    field_name = "test_field"

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.fields = {"test_field": None}


@pytest.mark.parametrize("required, nullable, field_value", [
    (True, True, u'test_value'),
    (True, True, "test_value"),
    (True, True, ""),
    (False, False, ""),
    (True, True, None),
    (False, True, None),
])
def test_char_field_ok_cases(required, nullable, field_value):
    _field = api.CharField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)
    assert getattr(mock_obj, "test_field") == field_value


@pytest.mark.parametrize("required, nullable, field_value", [
    (True, False, None),
    (False, False, None),
    (True, True, 12),
    (False, False, []),
])
def test_char_field_bad_cases(required, nullable, field_value):
    _field = api.CharField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    with pytest.raises(api.ValidationError):
        MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)


@pytest.mark.parametrize("required, nullable, field_value", [
    (True, True, {}),
    (False, True, {}),
    (False, True, None),
])
def test_arguments_field_ok_cases(required, nullable, field_value):
    _field = api.ArgumentsField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)
    assert getattr(mock_obj, "test_field") == field_value


@pytest.mark.parametrize("required, nullable, field_value", [
    (True, True, []),
    (True, False, None),
])
def test_arguments_field_bad_cases(required, nullable, field_value):
    _field = api.ArgumentsField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    with pytest.raises(api.ValidationError):
        MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)


@pytest.mark.parametrize("required, nullable, field_value", [
    (True, True, "some@example.com"),
    (False, False, "some@example.com"),
    (False, True, None),
    (False, False, ""),
    (True, True, ""),
])
def test_email_field_ok_cases(required, nullable, field_value):
    _field = api.EmailField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)
    assert getattr(mock_obj, "test_field") == field_value


@pytest.mark.parametrize("required, nullable, field_value", [
    (True, False, "example.com"),
    (False, False, None),
])
def test_email_field_bad_cases(required, nullable, field_value):
    _field = api.EmailField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    with pytest.raises(api.ValidationError):
        MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)


@pytest.mark.parametrize("required, nullable, field_value", [
    (False, True, "70123456789"),
    (False, True, 70123456789),
    (False, True, None),
])
def test_phone_field_ok_cases(required, nullable, field_value):
    _field = api.PhoneField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)
    assert getattr(mock_obj, "test_field") == field_value


@pytest.mark.parametrize("required, nullable, field_value", [
    (False, True, "00123456789"),
    (False, True, "0"),
    (False, True, 1),
    (False, False, None),
])
def test_email_field_bad_cases(required, nullable, field_value):
    _field = api.EmailField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    with pytest.raises(api.ValidationError):
        MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)


def test_date_field_string_parse(required=False, nullable=True,
                                 field_value="31.12.2000"):
    _field = api.DateField(required=required, nullable=nullable)
    _field.field_name = "test_field"
    datetime_value = datetime.datetime.strptime(field_value, "%d.%m.%Y")

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)
    assert getattr(mock_obj, "test_field") == datetime_value


def test_date_field_bad_format_string(required=False, nullable=True,
                                      field_value="31.13.2000"):
    _field = api.DateField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    with pytest.raises(api.ValidationError):
        MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)


def test_date_field_null_value(required=False, nullable=True,
                                      field_value=None):
    _field = api.DateField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)
    assert getattr(mock_obj, "test_field") == field_value


def test_date_field_datime_value(required=False, nullable=True,
                                 field_value=datetime.datetime.utcnow()):
    _field = api.DateField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)
    assert getattr(mock_obj, "test_field") == field_value


def test_birthday_field_too_old_date(required=False, nullable=True,
                                     field_value="31.12.1700"):
    _field = api.BirthDayField(required=required, nullable=nullable)
    _field.field_name = "test_field"
    datetime_value = datetime.datetime.strptime(field_value, "%d.%m.%Y")

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    with pytest.raises(api.ValidationError):
        MockRequest.__dict__["test_field"].__set__(mock_obj, datetime_value)


@pytest.mark.parametrize("required, nullable, field_value", [
    (False, True, 0),
    (False, True, 1),
    (False, True, 2),
    (False, True, None),
])
def test_gender_field_ok_cases(required, nullable, field_value):
    _field = api.GenderField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)
    assert getattr(mock_obj, "test_field") == field_value


@pytest.mark.parametrize("required, nullable, field_value", [
    (False, True, 3),
    (False, True, -1),
    (False, True, "1"),
    (False, True, []),
])
def test_gender_bad_cases(required, nullable, field_value):
    _field = api.GenderField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    with pytest.raises(api.ValidationError):
        MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)


@pytest.mark.parametrize("required, nullable, field_value", [
    (True, False, [1]),
    (True, False, [1, 2]),
    (True, False, (1, 2, 3)),
    (True, True, None),
])
def test_client_id_field_ok_cases(required, nullable, field_value):
    _field = api.ClientIDsField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)
    assert getattr(mock_obj, "test_field") == field_value


@pytest.mark.parametrize("required, nullable, field_value", [
    (True, False, ['1']),
    (True, False, [1, []]),
    (True, False, {}),
    (True, False, ""),
    (True, False, None),
])
def test_client_id_bad_cases(required, nullable, field_value):
    _field = api.GenderField(required=required, nullable=nullable)
    _field.field_name = "test_field"

    MockRequest.test_field = _field
    mock_obj = MockRequest(test_field=field_value)
    mock_obj.fields["test_field"] = _field
    with pytest.raises(api.ValidationError):
        MockRequest.__dict__["test_field"].__set__(mock_obj, field_value)