"""Tests for sitemap.xml validity and coverage."""

import os
import unittest
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP_PATH = os.path.join(BASE_DIR, "sitemap.xml")
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"

# All URLs that must appear in the sitemap.
EXPECTED_URLS = {
    "https://thatai.me/",
    "https://thatai.me/blog.html",
    "https://thatai.me/workflows/n8n-job-search-automation.html",
    "https://thatai.me/workflows/linkedin-automation.html",
    "https://thatai.me/workflows/ai-resume-tailor.html",
    "https://thatai.me/workflows/make-job-tracker.html",
    "https://thatai.me/workflows/zapier-job-alerts.html",
    "https://thatai.me/topics/ai-agents-guide.html",
    "https://thatai.me/topics/best-ai-tools-2025.html",
    "https://thatai.me/topics/chatgpt-job-search.html",
    "https://thatai.me/topics/n8n-beginners-guide.html",
    "https://thatai.me/topics/prompt-engineering.html",
    "https://thatai.me/topics/langchain-llm-apps.html",
}

VALID_CHANGEFREQ = {"always", "hourly", "daily", "weekly", "monthly", "yearly", "never"}


def _parse_sitemap():
    """Return the parsed sitemap XML tree."""
    return ET.parse(SITEMAP_PATH)


def _get_url_elements(tree):
    """Return all <url> elements from the parsed tree."""
    root = tree.getroot()
    return root.findall(f"{{{SITEMAP_NS}}}url")


class TestSitemapExists(unittest.TestCase):
    def test_sitemap_file_exists(self):
        self.assertTrue(os.path.isfile(SITEMAP_PATH), "sitemap.xml not found")


class TestSitemapXmlValidity(unittest.TestCase):
    """sitemap.xml must be well-formed XML with the correct namespace."""

    def test_parses_as_valid_xml(self):
        try:
            _parse_sitemap()
        except ET.ParseError as exc:
            self.fail(f"sitemap.xml is not valid XML: {exc}")

    def test_root_element_is_urlset(self):
        tree = _parse_sitemap()
        root = tree.getroot()
        self.assertEqual(
            root.tag,
            f"{{{SITEMAP_NS}}}urlset",
            "Root element must be <urlset> with the sitemap namespace",
        )

    def test_has_at_least_one_url(self):
        tree = _parse_sitemap()
        urls = _get_url_elements(tree)
        self.assertGreater(len(urls), 0, "sitemap.xml contains no <url> entries")


class TestSitemapUrlCoverage(unittest.TestCase):
    """All expected site URLs must be present in the sitemap."""

    def _sitemap_locs(self):
        tree = _parse_sitemap()
        locs = set()
        for url_el in _get_url_elements(tree):
            loc = url_el.find(f"{{{SITEMAP_NS}}}loc")
            if loc is not None and loc.text:
                locs.add(loc.text.strip())
        return locs

    def test_all_expected_urls_present(self):
        locs = self._sitemap_locs()
        for expected in EXPECTED_URLS:
            with self.subTest(url=expected):
                self.assertIn(expected, locs, f"{expected} missing from sitemap")

    def test_all_urls_use_https(self):
        locs = self._sitemap_locs()
        for loc in locs:
            with self.subTest(url=loc):
                self.assertTrue(
                    loc.startswith("https://"),
                    f"Sitemap URL does not use HTTPS: {loc}",
                )

    def test_all_urls_use_canonical_domain(self):
        locs = self._sitemap_locs()
        for loc in locs:
            with self.subTest(url=loc):
                self.assertIn(
                    "thatai.me",
                    loc,
                    f"Sitemap URL does not use thatai.me domain: {loc}",
                )


class TestSitemapUrlFields(unittest.TestCase):
    """Every <url> entry must have required child elements with valid values."""

    def test_every_url_has_loc(self):
        tree = _parse_sitemap()
        for i, url_el in enumerate(_get_url_elements(tree)):
            with self.subTest(index=i):
                loc = url_el.find(f"{{{SITEMAP_NS}}}loc")
                self.assertIsNotNone(loc, f"<url> #{i} missing <loc>")
                self.assertTrue(
                    loc.text and loc.text.strip(),
                    f"<url> #{i} has empty <loc>",
                )

    def test_every_url_has_lastmod(self):
        tree = _parse_sitemap()
        for i, url_el in enumerate(_get_url_elements(tree)):
            with self.subTest(index=i):
                lastmod = url_el.find(f"{{{SITEMAP_NS}}}lastmod")
                self.assertIsNotNone(lastmod, f"<url> #{i} missing <lastmod>")
                self.assertTrue(
                    lastmod.text and lastmod.text.strip(),
                    f"<url> #{i} has empty <lastmod>",
                )

    def test_every_url_has_changefreq(self):
        tree = _parse_sitemap()
        for i, url_el in enumerate(_get_url_elements(tree)):
            with self.subTest(index=i):
                cf = url_el.find(f"{{{SITEMAP_NS}}}changefreq")
                self.assertIsNotNone(cf, f"<url> #{i} missing <changefreq>")
                self.assertIn(
                    cf.text,
                    VALID_CHANGEFREQ,
                    f"<url> #{i} has invalid changefreq: {cf.text}",
                )

    def test_every_url_has_priority(self):
        tree = _parse_sitemap()
        for i, url_el in enumerate(_get_url_elements(tree)):
            with self.subTest(index=i):
                pri = url_el.find(f"{{{SITEMAP_NS}}}priority")
                self.assertIsNotNone(pri, f"<url> #{i} missing <priority>")
                self.assertTrue(
                    pri.text and pri.text.strip(),
                    f"<url> #{i} has empty <priority>",
                )

    def test_priority_values_in_valid_range(self):
        tree = _parse_sitemap()
        for i, url_el in enumerate(_get_url_elements(tree)):
            with self.subTest(index=i):
                pri = url_el.find(f"{{{SITEMAP_NS}}}priority")
                if pri is not None and pri.text:
                    value = float(pri.text)
                    self.assertGreaterEqual(value, 0.0, f"<url> #{i}: priority < 0")
                    self.assertLessEqual(value, 1.0, f"<url> #{i}: priority > 1")

    def test_lastmod_date_format(self):
        """lastmod should be a valid YYYY-MM-DD date string."""
        import re

        date_re = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        tree = _parse_sitemap()
        for i, url_el in enumerate(_get_url_elements(tree)):
            with self.subTest(index=i):
                lastmod = url_el.find(f"{{{SITEMAP_NS}}}lastmod")
                if lastmod is not None and lastmod.text:
                    self.assertRegex(
                        lastmod.text.strip(),
                        date_re,
                        f"<url> #{i} lastmod is not YYYY-MM-DD format",
                    )


class TestSitemapHomepagePriority(unittest.TestCase):
    """The homepage URL should have the highest priority (1.0)."""

    def test_homepage_has_priority_1(self):
        tree = _parse_sitemap()
        for url_el in _get_url_elements(tree):
            loc = url_el.find(f"{{{SITEMAP_NS}}}loc")
            if loc is not None and loc.text and loc.text.strip() in (
                "https://thatai.me/",
                "https://thatai.me",
            ):
                pri = url_el.find(f"{{{SITEMAP_NS}}}priority")
                self.assertIsNotNone(pri, "Homepage <url> missing <priority>")
                self.assertEqual(
                    float(pri.text),
                    1.0,
                    "Homepage priority should be 1.0",
                )
                return
        self.fail("Homepage URL not found in sitemap")


if __name__ == "__main__":
    unittest.main()
