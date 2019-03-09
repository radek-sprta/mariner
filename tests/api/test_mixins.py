import pytest

from mariner import mixins, torrent


@pytest.mark.smoke
class TestComparableMixin:
    @pytest.fixture(scope="class", params=[10, 19, -1])
    def torrent1(self, request):
        return torrent.Torrent("name", "tracker", seeds=request.param)

    @pytest.fixture(scope="class")
    def torrent2(self):
        return torrent.Torrent("name", "tracker", seeds=20)

    def test_eq(self, torrent1, torrent2):
        """Equality comparison."""
        assert torrent1 == torrent1
        assert torrent2 == torrent2

    def test_ne(self, torrent1, torrent2):
        """Non equality comparison."""
        assert torrent1 != torrent2
        assert torrent2 != torrent1

    def test_lt(self, torrent1, torrent2):
        """Lesser then comparison."""
        assert torrent1 < torrent2
        assert not torrent2 < torrent1

    def test_gt(self, torrent1, torrent2):
        """Greater than comparison."""
        assert torrent2 > torrent1
        assert not torrent1 > torrent2

    def test_le(self, torrent1, torrent2):
        """Lesser equal comparison."""
        assert torrent1 <= torrent2
        assert torrent1 <= torrent1
        assert not torrent2 <= torrent1

    def test_ge(self, torrent1, torrent2):
        """Greater equal comparison."""
        assert torrent2 >= torrent1
        assert torrent2 >= torrent2
        assert not torrent1 >= torrent2

    def test_non_mixing(self, torrent1):
        """Raise exception when comparing to noncomparable."""

        class NonComparable:
            pass

        noncomparable = NonComparable()
        assert torrent1 != noncomparable


class TestRequestMixin:
    def test_get(self, event_loop):
        # GIVEN an event_loop
        # WHEN requesting a url
        search = event_loop.run_until_complete(
            mixins.RequestMixin().get("http://httpbin.org/robots.txt")
        )
        # THEN it should return expected result
        expected = "User-agent: *\nDisallow: /deny\n"
        assert search == expected

    def test_request_get(self, event_loop):
        # GIVEN an event_loop
        # WHEN requesting a url
        search = event_loop.run_until_complete(
            mixins.RequestMixin().request("get", "http://httpbin.org/robots.txt")
        )
        # THEN it should return expected result
        expected = "User-agent: *\nDisallow: /deny\n"
        assert search == expected

    def test_request_post(self, event_loop):
        # GIVEN an event_loop
        # WHEN posting to url
        response = event_loop.run_until_complete(
            mixins.RequestMixin().request("post", "http://httpbin.org/anything", data='hello')
        )
        # THEN it should post the payload
        assert 'hello' in response
