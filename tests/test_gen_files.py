"""Tests for gen_files.py template constants (NAV, FOOTER, SCRIPT, BASE)."""

import io
import sys
import unittest


def _import_gen_files():
    """Import gen_files while suppressing the print side-effect."""
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        import gen_files
        return gen_files
    finally:
        sys.stdout = old_stdout


gf = _import_gen_files()


class TestBase(unittest.TestCase):
    """Tests for the BASE constant."""

    def test_base_is_defined(self):
        self.assertTrue(hasattr(gf, "BASE"))

    def test_base_is_string(self):
        self.assertIsInstance(gf.BASE, str)

    def test_base_is_non_empty(self):
        self.assertTrue(gf.BASE.strip())


class TestNav(unittest.TestCase):
    """Tests for the NAV template constant."""

    def test_nav_is_defined(self):
        self.assertTrue(hasattr(gf, "NAV"))

    def test_nav_is_string(self):
        self.assertIsInstance(gf.NAV, str)

    def test_nav_has_logo_link(self):
        self.assertIn('href="/"', gf.NAV)
        self.assertIn("AllAboutAI", gf.NAV)

    def test_nav_has_home_link(self):
        self.assertIn('href="/"', gf.NAV)

    def test_nav_has_blog_link(self):
        self.assertIn('href="/blog.html"', gf.NAV)

    def test_nav_has_workflow_n8n_job_search(self):
        self.assertIn("/workflows/n8n-job-search-automation.html", gf.NAV)

    def test_nav_has_workflow_linkedin(self):
        self.assertIn("/workflows/linkedin-automation.html", gf.NAV)

    def test_nav_has_workflow_ai_resume(self):
        self.assertIn("/workflows/ai-resume-tailor.html", gf.NAV)

    def test_nav_has_workflow_make_tracker(self):
        self.assertIn("/workflows/make-job-tracker.html", gf.NAV)

    def test_nav_has_workflow_zapier(self):
        self.assertIn("/workflows/zapier-job-alerts.html", gf.NAV)

    def test_nav_has_topic_ai_agents(self):
        self.assertIn("/topics/ai-agents-guide.html", gf.NAV)

    def test_nav_has_topic_best_ai_tools(self):
        self.assertIn("/topics/best-ai-tools-2025.html", gf.NAV)

    def test_nav_has_topic_chatgpt(self):
        self.assertIn("/topics/chatgpt-job-search.html", gf.NAV)

    def test_nav_has_topic_n8n_guide(self):
        self.assertIn("/topics/n8n-beginners-guide.html", gf.NAV)

    def test_nav_has_topic_prompt_engineering(self):
        self.assertIn("/topics/prompt-engineering.html", gf.NAV)

    def test_nav_has_topic_langchain(self):
        self.assertIn("/topics/langchain-llm-apps.html", gf.NAV)

    def test_nav_has_about_link(self):
        self.assertIn("/blog.html#about", gf.NAV)

    def test_nav_has_hamburger_button(self):
        self.assertIn("hamburger", gf.NAV)

    def test_nav_has_mobile_menu(self):
        self.assertIn("mobileMenu", gf.NAV)

    def test_nav_has_nav_wrapper(self):
        self.assertIn("nav-wrapper", gf.NAV)

    def test_nav_has_dropdown(self):
        self.assertIn("dropdown", gf.NAV)

    def test_nav_workflows_dropdown_label(self):
        self.assertIn("Workflows", gf.NAV)

    def test_nav_topics_dropdown_label(self):
        self.assertIn("Topics", gf.NAV)


class TestFooter(unittest.TestCase):
    """Tests for the FOOTER template constant."""

    def test_footer_is_defined(self):
        self.assertTrue(hasattr(gf, "FOOTER"))

    def test_footer_is_string(self):
        self.assertIsInstance(gf.FOOTER, str)

    def test_footer_has_footer_tag(self):
        self.assertIn("<footer", gf.FOOTER)

    def test_footer_has_logo_text(self):
        self.assertIn("AllAboutAI", gf.FOOTER)

    def test_footer_has_workflow_n8n_job_search(self):
        self.assertIn("/workflows/n8n-job-search-automation.html", gf.FOOTER)

    def test_footer_has_workflow_linkedin(self):
        self.assertIn("/workflows/linkedin-automation.html", gf.FOOTER)

    def test_footer_has_workflow_ai_resume(self):
        self.assertIn("/workflows/ai-resume-tailor.html", gf.FOOTER)

    def test_footer_has_workflow_make_tracker(self):
        self.assertIn("/workflows/make-job-tracker.html", gf.FOOTER)

    def test_footer_has_workflow_zapier(self):
        self.assertIn("/workflows/zapier-job-alerts.html", gf.FOOTER)

    def test_footer_has_topic_ai_agents(self):
        self.assertIn("/topics/ai-agents-guide.html", gf.FOOTER)

    def test_footer_has_topic_best_ai_tools(self):
        self.assertIn("/topics/best-ai-tools-2025.html", gf.FOOTER)

    def test_footer_has_topic_chatgpt(self):
        self.assertIn("/topics/chatgpt-job-search.html", gf.FOOTER)

    def test_footer_has_topic_n8n_guide(self):
        self.assertIn("/topics/n8n-beginners-guide.html", gf.FOOTER)

    def test_footer_has_topic_prompt_engineering(self):
        self.assertIn("/topics/prompt-engineering.html", gf.FOOTER)

    def test_footer_has_blog_link(self):
        self.assertIn("/blog.html", gf.FOOTER)

    def test_footer_has_sitemap_link(self):
        self.assertIn("/sitemap.xml", gf.FOOTER)

    def test_footer_has_copyright(self):
        self.assertIn("2025", gf.FOOTER)
        self.assertIn("AllAboutAI", gf.FOOTER)

    def test_footer_has_footer_grid(self):
        self.assertIn("footer-grid", gf.FOOTER)

    def test_footer_has_footer_bottom(self):
        self.assertIn("footer-bottom", gf.FOOTER)

    def test_footer_has_closing_tag(self):
        self.assertIn("</footer>", gf.FOOTER)

    def test_footer_has_workflows_section_heading(self):
        self.assertIn("Workflows", gf.FOOTER)

    def test_footer_has_topics_section_heading(self):
        self.assertIn("Topics", gf.FOOTER)

    def test_footer_has_about_section_heading(self):
        self.assertIn("About", gf.FOOTER)


class TestScript(unittest.TestCase):
    """Tests for the SCRIPT template constant."""

    def test_script_is_defined(self):
        self.assertTrue(hasattr(gf, "SCRIPT"))

    def test_script_is_string(self):
        self.assertIsInstance(gf.SCRIPT, str)

    def test_script_has_opening_tag(self):
        self.assertIn("<script>", gf.SCRIPT)

    def test_script_has_closing_tag(self):
        self.assertIn("</script>", gf.SCRIPT)

    def test_script_has_progress_bar(self):
        self.assertIn("progressBar", gf.SCRIPT)

    def test_script_has_scroll_listener(self):
        self.assertIn("scroll", gf.SCRIPT)

    def test_script_has_hamburger_handler(self):
        self.assertIn("hamburger", gf.SCRIPT)

    def test_script_has_mobile_menu_toggle(self):
        self.assertIn("mobileMenu", gf.SCRIPT)

    def test_script_has_faq_handler(self):
        self.assertIn("faq-question", gf.SCRIPT)

    def test_script_has_intersection_observer(self):
        self.assertIn("IntersectionObserver", gf.SCRIPT)

    def test_script_has_data_animate_observer(self):
        self.assertIn("data-animate", gf.SCRIPT)

    def test_script_has_toc_scroll_handler(self):
        self.assertIn("tocLinks", gf.SCRIPT)

    def test_script_has_sections_scroll_tracking(self):
        self.assertIn("sections", gf.SCRIPT)

    def test_script_has_active_class_toggle(self):
        self.assertIn("active", gf.SCRIPT)


if __name__ == "__main__":
    unittest.main()
