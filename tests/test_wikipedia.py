from modern_python import wikipedia


def test_random_page_uses_given_language(mock_requests_get):
    wikipedia.random_page(language="de")
    args, _ = mock_requests_get.call_args
    assert "de.wikipedia.org" in args[0]


def test_random_page_uses_local_language(mock_requests_get):
    wikipedia.random_page(language="local")
    args, _ = mock_requests_get.call_args
    assert "wikipedia.org" in args[0]
