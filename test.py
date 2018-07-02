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