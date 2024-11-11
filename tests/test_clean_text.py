from src.app.back import clean_text


def test_should_remove_newline():
    assert clean_text("test\ntest") == "test test"

def test_should_remove_punctuations():
    assert clean_text("test?") == "test"

def test_should_cast_to_lowercase():
    assert clean_text("TEST") == "test"