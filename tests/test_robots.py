"""Tests for robots.txt content and structure."""

import os
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROBOTS_PATH = os.path.join(BASE_DIR, "robots.txt")


def _read_robots():
    """Return the content of robots.txt as a string."""
    with open(ROBOTS_PATH, encoding="utf-8") as fh:
        return fh.read()


class TestRobotsExists(unittest.TestCase):
    def test_robots_file_exists(self):
        self.assertTrue(os.path.isfile(ROBOTS_PATH), "robots.txt not found")

    def test_robots_file_non_empty(self):
        content = _read_robots()
        self.assertTrue(content.strip(), "robots.txt is empty")


class TestRobotsUserAgent(unittest.TestCase):
    """robots.txt must declare at least one User-agent directive."""

    def test_has_user_agent_directive(self):
        content = _read_robots()
        self.assertIn("User-agent:", content, "robots.txt missing User-agent directive")

    def test_wildcard_user_agent_present(self):
        content = _read_robots()
        self.assertIn("User-agent: *", content, "robots.txt missing wildcard User-agent")


class TestRobotsAllowDisallow(unittest.TestCase):
    """robots.txt must allow the root path and disallow sensitive paths."""

    def test_allow_root(self):
        content = _read_robots()
        self.assertIn("Allow: /", content, "robots.txt missing 'Allow: /'")

    def test_disallow_git_directory(self):
        content = _read_robots()
        self.assertIn(
            "Disallow: /.git/",
            content,
            "robots.txt missing 'Disallow: /.git/'",
        )


class TestRobotsSitemapReference(unittest.TestCase):
    """robots.txt must reference the sitemap URL."""

    def test_sitemap_directive_present(self):
        content = _read_robots()
        self.assertIn("Sitemap:", content, "robots.txt missing Sitemap directive")

    def test_sitemap_points_to_correct_url(self):
        content = _read_robots()
        self.assertIn(
            "https://thatai.me/sitemap.xml",
            content,
            "robots.txt Sitemap directive does not point to https://thatai.me/sitemap.xml",
        )

    def test_sitemap_uses_https(self):
        for line in _read_robots().splitlines():
            if line.startswith("Sitemap:"):
                url = line.split(":", 1)[1].strip()
                self.assertTrue(
                    url.startswith("https://"),
                    f"Sitemap URL in robots.txt is not HTTPS: {url}",
                )


class TestRobotsLineEndings(unittest.TestCase):
    """robots.txt should use Unix-style line endings (LF only)."""

    def test_no_windows_line_endings(self):
        with open(ROBOTS_PATH, "rb") as fh:
            content = fh.read()
        self.assertNotIn(
            b"\r\n",
            content,
            "robots.txt contains Windows-style CRLF line endings",
        )


if __name__ == "__main__":
    unittest.main()
