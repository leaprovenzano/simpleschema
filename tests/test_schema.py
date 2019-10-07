import pytest
from simpleschema.schema import StringSchema, Format


class TestStringSchema:

    def test_with_format(self):
        schema = StringSchema(format=Format.email)
        assert schema.to_dict() == {'type': 'string', 'format': 'email'}

    def test_no_inp(self):
        schema = StringSchema()
        assert schema.to_dict() == {'type': 'string'}

    def test_immutable_fields(self):
        errmsg = 'fields in a schema are immutable once set'
        schema = StringSchema(min_length=1)
        with pytest.raises(ValueError) as errinfo:
            schema.min_length = 2
            assert errmsg in errinfo.value

    def test_fixed_fields_on_init(self):
        errmsg = 'field bullshit is invalid for StringSchema'
        with pytest.raises(ValueError) as errinfo:
            StringSchema(bullshit=1)
            assert errmsg in errinfo.value

    def test_fixed_fields_post_init(self):
        errmsg = 'field bullshit is invalid for StringSchema'
        schema = StringSchema()
        with pytest.raises(ValueError) as errinfo:
            schema.bullshit = 1
            assert errmsg in errinfo.value

    def test_pascalizing(self):
        schema = StringSchema(min_length=1)
        schema.to_dict() == {'type': 'string', 'minLength': 1}

    def test_all_fields(self):
        schema = StringSchema(
            min_length=9, max_length=20, pattern=r"[a-z]+@blah\.com", format=Format.email
        )
        schema.to_dict() == {
            'type': 'string',
            'minLength': 9,
            'maxLength': 20,
            'pattern': r"[a-z]+@blah\.com",
            'format': 'email',
        }
