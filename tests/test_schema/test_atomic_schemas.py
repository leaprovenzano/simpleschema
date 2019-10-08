import pytest

from simpleschema.formats import Format
from simpleschema.schema import StringSchema, NumberSchema, IntegerSchema, NullSchema, BooleanSchema


class SchemaSuite:

    SchemaCls = NotImplemented
    expected_type = NotImplemented

    def test_no_inp(self):
        schema = self.SchemaCls()
        assert schema.to_dict() == {'type': self.expected_type}

    def test_no_with_title_and_description(self):
        schema = self.SchemaCls(title='some_title', description='blah blah blah')
        assert schema.to_dict() == {
            'type': self.expected_type,
            'title': 'some_title',
            'description': 'blah blah blah',
        }

    def test_fixed_fields_on_init(self):
        errmsg = f'field bullshit is invalid for {self.SchemaCls.__name__}'
        with pytest.raises(ValueError) as errinfo:
            self.SchemaCls(bullshit=1)
            assert errmsg in errinfo.value

    def test_fixed_fields_post_init(self):
        errmsg = f'field bullshit is invalid for {self.SchemaCls.__name__}'
        schema = self.SchemaCls()
        with pytest.raises(ValueError) as errinfo:
            schema.bullshit = 1
            assert errmsg in errinfo.value


class TestNullSchema(SchemaSuite):

    SchemaCls = NullSchema
    expected_type = 'null'


class TestBoolSchema(SchemaSuite):

    SchemaCls = BooleanSchema
    expected_type = 'boolean'


class TestStringSchema(SchemaSuite):

    SchemaCls = StringSchema
    expected_type = 'string'

    def test_with_format(self):
        schema = self.SchemaCls(format=Format.email)
        assert schema.to_dict() == {'type': self.expected_type, 'format': 'email'}

    def test_immutable_fields(self):
        errmsg = 'fields in a schema are immutable once set'
        schema = self.SchemaCls(min_length=1)
        with pytest.raises(ValueError) as errinfo:
            schema.min_length = 2
            assert errmsg in errinfo.value

    def test_pascalizing(self):
        schema = self.SchemaCls(min_length=1)
        schema.to_dict() == {'type': 'string', 'minLength': 1}

    def test_all_fields(self):
        schema = self.SchemaCls(
            min_length=9, max_length=20, pattern=r"[a-z]+@blah\.com", format=Format.email
        )
        schema.to_dict() == {
            'type': 'string',
            'minLength': 9,
            'maxLength': 20,
            'pattern': r"[a-z]+@blah\.com",
            'format': 'email',
        }


class TestNumberSchema(SchemaSuite):

    SchemaCls = NumberSchema
    expected_type = 'number'

    def test_immutable_fields(self):
        errmsg = 'fields in a schema are immutable once set'
        schema = self.SchemaCls(minimum=1)
        with pytest.raises(ValueError) as errinfo:
            schema.minimum = 2
            assert errmsg in errinfo.value

    def test_fixed_fields_on_init(self):
        errmsg = 'field bullshit is invalid for StringSchema'
        with pytest.raises(ValueError) as errinfo:
            StringSchema(bullshit=1)
            assert errmsg in errinfo.value

    def test_all_constr_fields(self):
        schema = self.SchemaCls(
            minimum=1, maximum=10, exclusive_minimum=0, exclusive_maximum=11, multiple_of=2
        )
        schema.to_dict() == {
            'type': self.expected_type,
            'minimum': 1,
            'maximum': 10,
            'exclusiveMinimum': 0,
            'exclusiveMaximum': 11,
            'multipleOf': 2,
        }


class TestIntegerSchema(TestNumberSchema):

    SchemaCls = IntegerSchema
    expected_type = 'integer'

    def test_immutable_fields(self):
        errmsg = 'fields in a schema are immutable once set'
        schema = self.SchemaCls(minimum=1)
        with pytest.raises(ValueError) as errinfo:
            schema.minimum = 2
            assert errmsg in errinfo.value

    def test_fixed_fields_on_init(self):
        errmsg = 'field bullshit is invalid for StringSchema'
        with pytest.raises(ValueError) as errinfo:
            StringSchema(bullshit=1)
            assert errmsg in errinfo.value

    def test_all_constr_fields(self):
        schema = self.SchemaCls(
            minimum=1, maximum=10, exclusive_minimum=0, exclusive_maximum=11, multiple_of=2
        )
        schema.to_dict() == {
            'type': self.expected_type,
            'minimum': 1,
            'maximum': 10,
            'exclusiveMinimum': 0,
            'exclusiveMaximum': 11,
            'multipleOf': 2,
        }
