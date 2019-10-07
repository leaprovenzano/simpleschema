from simpleschema.atomics import String, Number, Integer, Boolean, Null


class TestString:

    T = String

    def test_schema(self):
        assert self.T.__schema__(min_length=1) == {'type': 'string', 'minLength': 1}

    def test_no_mod_init(self):
        assert self.T('something') == 'something'

    def test_cast(self):
        assert self.T(1) == '1'

    def test_is_supertype(self):
        assert isinstance(self.T('blah'), str)


class TestNumber:

    T = Number

    def test_schema(self):
        assert self.T.__schema__(minimum=1) == {'type': 'number', 'minimum': 1}

    def test_no_mod_init(self):
        assert self.T(2) == 2

    def test_cast(self):
        assert self.T(2) == 2.0

    def test_is_supertype(self):
        assert isinstance(self.T(2), float)


class TestInteger:

    T = Integer

    def test_schema(self):
        assert self.T.__schema__(minimum=1) == {'type': 'integer', 'minimum': 1}

    def test_no_mod_init(self):
        assert self.T(2) == 2

    def test_cast(self):
        assert self.T(2.0) == 2

    def test_is_supertype(self):
        assert isinstance(self.T(2), int)


class TestBoolean:

    T = Boolean

    def test_schema(self):
        assert self.T.__schema__() == {'type': 'boolean'}

    def test_is_supertype(self):
        assert isinstance(self.T(1), bool)

    def test_cast(self):
        assert self.T(1) is True

    def test_no_mod_init(self):
        assert self.T(True) is True


class TestNull:

    T = Null

    def test_schema(self):
        assert self.T.__schema__() == {'type': 'null'}

    def test_is_supertype(self):
        assert isinstance(self.T(), type(None))

    def test_init(self):
        assert self.T() is None
