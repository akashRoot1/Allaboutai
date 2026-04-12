"""Tests for HTML page structure across all site pages."""

import os
import unittest

from bs4 import BeautifulSoup

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# All HTML pages that are part of the site (relative to BASE_DIR).
# article.html is excluded from shared nav/footer/canonical checks because
# it is a standalone article template with its own lightweight structure.
MAIN_PAGES = [
    "index.html",
    "blog.html",
]

TOPIC_PAGES = [
    "topics/ai-agents-guide.html",
    "topics/best-ai-tools-2025.html",
    "topics/chatgpt-job-search.html",
    "topics/langchain-llm-apps.html",
    "topics/n8n-beginners-guide.html",
    "topics/prompt-engineering.html",
]

WORKFLOW_PAGES = [
    "workflows/ai-resume-tailor.html",
    "workflows/linkedin-automation.html",
    "workflows/make-job-tracker.html",
    "workflows/n8n-job-search-automation.html",
    "workflows/zapier-job-alerts.html",
]

# Pages that share the full nav/footer/meta pattern.
FULL_PAGES = MAIN_PAGES + TOPIC_PAGES + WORKFLOW_PAGES

# All HTML files, including the standalone article template.
ALL_HTML_FILES = FULL_PAGES + ["article.html"]

# Internal links that resolve to a file path on disk (fragment links excluded).
INTERNAL_FILE_LINKS = {
    "/": "index.html",
    "/blog.html": "blog.html",
    "/topics/ai-agents-guide.html": "topics/ai-agents-guide.html",
    "/topics/best-ai-tools-2025.html": "topics/best-ai-tools-2025.html",
    "/topics/chatgpt-job-search.html": "topics/chatgpt-job-search.html",
    "/topics/langchain-llm-apps.html": "topics/langchain-llm-apps.html",
    "/topics/n8n-beginners-guide.html": "topics/n8n-beginners-guide.html",
    "/topics/prompt-engineering.html": "topics/prompt-engineering.html",
    "/workflows/ai-resume-tailor.html": "workflows/ai-resume-tailor.html",
    "/workflows/linkedin-automation.html": "workflows/linkedin-automation.html",
    "/workflows/make-job-tracker.html": "workflows/make-job-tracker.html",
    "/workflows/n8n-job-search-automation.html": "workflows/n8n-job-search-automation.html",
    "/workflows/zapier-job-alerts.html": "workflows/zapier-job-alerts.html",
    "/sitemap.xml": "sitemap.xml",
    "/css/styles.css": "css/styles.css",
}


def _load(relative_path):
    """Return a BeautifulSoup object for the given relative path."""
    abs_path = os.path.join(BASE_DIR, relative_path)
    with open(abs_path, encoding="utf-8") as fh:
        return BeautifulSoup(fh.read(), "lxml")


def _raw(relative_path):
    """Return raw file content for the given relative path."""
    abs_path = os.path.join(BASE_DIR, relative_path)
    with open(abs_path, encoding="utf-8") as fh:
        return fh.read()


class TestAllHTMLFilesExist(unittest.TestCase):
    """Every HTML file that belongs to the site must exist on disk."""

    def test_all_html_files_exist(self):
        for page in ALL_HTML_FILES:
            with self.subTest(page=page):
                self.assertTrue(
                    os.path.isfile(os.path.join(BASE_DIR, page)),
                    f"{page} not found",
                )


class TestDoctype(unittest.TestCase):
    """Every HTML file must begin with <!DOCTYPE html>."""

    def test_all_pages_have_doctype(self):
        for page in ALL_HTML_FILES:
            with self.subTest(page=page):
                raw = _raw(page)
                self.assertTrue(
                    raw.strip().lower().startswith("<!doctype html"),
                    f"{page} missing <!DOCTYPE html>",
                )


class TestLangAttribute(unittest.TestCase):
    """Every HTML file must declare the document language."""

    def test_all_pages_have_lang_en(self):
        for page in ALL_HTML_FILES:
            with self.subTest(page=page):
                soup = _load(page)
                html_tag = soup.find("html")
                self.assertIsNotNone(html_tag, f"{page}: no <html> tag")
                lang = html_tag.get("lang", "")
                self.assertEqual(
                    lang,
                    "en",
                    f"{page}: expected lang='en', got lang='{lang}'",
                )


class TestRequiredMetaTags(unittest.TestCase):
    """Every HTML file must have charset, viewport, title, and description."""

    def test_charset_utf8(self):
        for page in ALL_HTML_FILES:
            with self.subTest(page=page):
                soup = _load(page)
                charset = soup.find("meta", attrs={"charset": True})
                self.assertIsNotNone(charset, f"{page}: missing charset meta")
                self.assertEqual(
                    charset["charset"].upper(),
                    "UTF-8",
                    f"{page}: charset is not UTF-8",
                )

    def test_viewport_meta(self):
        for page in ALL_HTML_FILES:
            with self.subTest(page=page):
                soup = _load(page)
                viewport = soup.find("meta", attrs={"name": "viewport"})
                self.assertIsNotNone(viewport, f"{page}: missing viewport meta")
                content = viewport.get("content", "")
                self.assertIn(
                    "width=device-width",
                    content,
                    f"{page}: viewport missing width=device-width",
                )

    def test_title_non_empty(self):
        for page in ALL_HTML_FILES:
            with self.subTest(page=page):
                soup = _load(page)
                title = soup.find("title")
                self.assertIsNotNone(title, f"{page}: missing <title>")
                self.assertTrue(
                    title.get_text(strip=True),
                    f"{page}: <title> is empty",
                )

    def test_description_meta(self):
        for page in ALL_HTML_FILES:
            with self.subTest(page=page):
                soup = _load(page)
                desc = soup.find("meta", attrs={"name": "description"})
                self.assertIsNotNone(desc, f"{page}: missing description meta")
                self.assertTrue(
                    desc.get("content", "").strip(),
                    f"{page}: description meta is empty",
                )


class TestOpenGraphTags(unittest.TestCase):
    """Full site pages must have Open Graph meta tags."""

    OG_PROPERTIES = ["og:title", "og:description", "og:image", "og:url"]

    def test_og_tags_present(self):
        for page in FULL_PAGES:
            for prop in self.OG_PROPERTIES:
                with self.subTest(page=page, property=prop):
                    soup = _load(page)
                    tag = soup.find("meta", attrs={"property": prop})
                    self.assertIsNotNone(
                        tag, f"{page}: missing <meta property='{prop}'>"
                    )
                    self.assertTrue(
                        tag.get("content", "").strip(),
                        f"{page}: <meta property='{prop}'> content is empty",
                    )

    def test_og_image_points_to_site_image(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                tag = soup.find("meta", attrs={"property": "og:image"})
                self.assertIsNotNone(tag, f"{page}: missing og:image")
                self.assertIn(
                    "thatai.me",
                    tag.get("content", ""),
                    f"{page}: og:image does not point to thatai.me",
                )

    def test_og_url_points_to_site(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                tag = soup.find("meta", attrs={"property": "og:url"})
                self.assertIsNotNone(tag, f"{page}: missing og:url")
                self.assertIn(
                    "thatai.me",
                    tag.get("content", ""),
                    f"{page}: og:url does not point to thatai.me",
                )


class TestTwitterCardTags(unittest.TestCase):
    """Full site pages must have Twitter Card meta tags."""

    TWITTER_NAMES = ["twitter:card", "twitter:title", "twitter:description"]

    def test_twitter_card_tags_present(self):
        for page in FULL_PAGES:
            for name in self.TWITTER_NAMES:
                with self.subTest(page=page, name=name):
                    soup = _load(page)
                    tag = soup.find("meta", attrs={"name": name})
                    self.assertIsNotNone(
                        tag, f"{page}: missing <meta name='{name}'>"
                    )
                    self.assertTrue(
                        tag.get("content", "").strip(),
                        f"{page}: <meta name='{name}'> content is empty",
                    )

    def test_twitter_card_type(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                tag = soup.find("meta", attrs={"name": "twitter:card"})
                self.assertIsNotNone(tag, f"{page}: missing twitter:card")
                self.assertEqual(
                    tag.get("content", ""),
                    "summary_large_image",
                    f"{page}: unexpected twitter:card value",
                )


class TestCanonicalLink(unittest.TestCase):
    """Full site pages must have a canonical link pointing to thatai.me."""

    def test_canonical_link_present(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                canon = soup.find("link", attrs={"rel": "canonical"})
                self.assertIsNotNone(canon, f"{page}: missing canonical link")

    def test_canonical_link_points_to_site(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                canon = soup.find("link", attrs={"rel": "canonical"})
                self.assertIsNotNone(canon, f"{page}: missing canonical link")
                href = canon.get("href", "")
                self.assertIn(
                    "thatai.me",
                    href,
                    f"{page}: canonical href does not contain thatai.me",
                )

    def test_canonical_link_uses_https(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                canon = soup.find("link", attrs={"rel": "canonical"})
                self.assertIsNotNone(canon, f"{page}: missing canonical link")
                href = canon.get("href", "")
                self.assertTrue(
                    href.startswith("https://"),
                    f"{page}: canonical href not https: {href}",
                )


class TestStylesheetLink(unittest.TestCase):
    """Full site pages must link to css/styles.css."""

    def test_stylesheet_link_present(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                css = soup.find("link", attrs={"rel": "stylesheet"})
                self.assertIsNotNone(css, f"{page}: no stylesheet link")
                href = css.get("href", "")
                self.assertIn(
                    "styles.css",
                    href,
                    f"{page}: stylesheet link does not point to styles.css",
                )


class TestNavigation(unittest.TestCase):
    """Full site pages must have a navigation section with expected links."""

    def test_nav_element_present(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                self.assertIsNotNone(
                    soup.find("nav"), f"{page}: no <nav> element"
                )

    def test_nav_has_home_link(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                nav = soup.find("nav")
                self.assertIsNotNone(nav, f"{page}: no <nav> element")
                links = [a.get("href", "") for a in nav.find_all("a")]
                self.assertIn("/", links, f"{page}: nav missing home link")

    def test_nav_has_blog_link(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                nav = soup.find("nav")
                self.assertIsNotNone(nav, f"{page}: no <nav> element")
                links = [a.get("href", "") for a in nav.find_all("a")]
                self.assertIn("/blog.html", links, f"{page}: nav missing blog link")

    def test_nav_has_logo(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                nav = soup.find("nav")
                self.assertIsNotNone(nav, f"{page}: no <nav> element")
                logo = nav.find("a", class_="nav-logo")
                self.assertIsNotNone(logo, f"{page}: nav missing logo link")


class TestFooter(unittest.TestCase):
    """Full site pages must have a footer."""

    def test_footer_element_present(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                self.assertIsNotNone(
                    soup.find("footer"), f"{page}: no <footer> element"
                )

    def test_footer_has_copyright_text(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                footer = soup.find("footer")
                self.assertIsNotNone(footer, f"{page}: no <footer> element")
                text = footer.get_text()
                self.assertIn("AllAboutAI", text, f"{page}: footer missing AllAboutAI")

    def test_footer_has_sitemap_link(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                footer = soup.find("footer")
                self.assertIsNotNone(footer, f"{page}: no <footer> element")
                links = [a.get("href", "") for a in footer.find_all("a")]
                self.assertIn(
                    "/sitemap.xml", links, f"{page}: footer missing sitemap link"
                )


class TestInternalLinks(unittest.TestCase):
    """Internal file links referenced in pages must resolve to existing files."""

    def test_internal_links_resolve(self):
        for src_page in FULL_PAGES:
            soup = _load(src_page)
            for a_tag in soup.find_all("a", href=True):
                href = a_tag["href"]
                # Only check absolute internal links that correspond to files
                if href in INTERNAL_FILE_LINKS:
                    target = INTERNAL_FILE_LINKS[href]
                    with self.subTest(src=src_page, href=href):
                        self.assertTrue(
                            os.path.isfile(os.path.join(BASE_DIR, target)),
                            f"{src_page}: link '{href}' -> '{target}' not found",
                        )

    def test_css_file_exists(self):
        """The stylesheet referenced by pages must exist on disk."""
        self.assertTrue(
            os.path.isfile(os.path.join(BASE_DIR, "css", "styles.css"))
        )


class TestArticlePage(unittest.TestCase):
    """Structural tests specific to article.html (standalone template)."""

    PAGE = "article.html"

    def test_article_has_title(self):
        soup = _load(self.PAGE)
        title = soup.find("title")
        self.assertIsNotNone(title)
        self.assertTrue(title.get_text(strip=True))

    def test_article_has_description(self):
        soup = _load(self.PAGE)
        desc = soup.find("meta", attrs={"name": "description"})
        self.assertIsNotNone(desc)
        self.assertTrue(desc.get("content", "").strip())

    def test_article_has_nav(self):
        soup = _load(self.PAGE)
        self.assertIsNotNone(soup.find("nav"))

    def test_article_has_footer(self):
        soup = _load(self.PAGE)
        self.assertIsNotNone(soup.find("footer"))

    def test_article_has_body(self):
        soup = _load(self.PAGE)
        self.assertIsNotNone(soup.find("body"))

    def test_article_has_heading(self):
        soup = _load(self.PAGE)
        h1 = soup.find("h1")
        self.assertIsNotNone(h1, "article.html should have an <h1>")
        self.assertTrue(h1.get_text(strip=True))


class TestProgressBar(unittest.TestCase):
    """Full site pages should include the scroll-progress bar element."""

    def test_progress_bar_present(self):
        for page in FULL_PAGES:
            with self.subTest(page=page):
                soup = _load(page)
                bar = soup.find(id="progressBar")
                self.assertIsNotNone(
                    bar, f"{page}: missing #progressBar element"
                )


if __name__ == "__main__":
    unittest.main()
