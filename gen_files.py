import os

BASE = "/home/runner/work/Allaboutai/Allaboutai"

NAV = """  <nav class="nav-wrapper">
    <div class="nav-inner">
      <a href="/" class="nav-logo">🤖 AllAboutAI</a>
      <ul class="nav-links">
        <li><a href="/">Home</a></li>
        <li><a href="/blog.html">Blog</a></li>
        <li class="dropdown"><a href="#">Workflows ▾</a>
          <div class="dropdown-menu">
            <a href="/workflows/n8n-job-search-automation.html">🔍 n8n Job Search</a>
            <a href="/workflows/linkedin-automation.html">💼 LinkedIn Automation</a>
            <a href="/workflows/ai-resume-tailor.html">📄 AI Resume Tailor</a>
            <a href="/workflows/make-job-tracker.html">📊 Make.com Tracker</a>
            <a href="/workflows/zapier-job-alerts.html">🔔 Zapier Job Alerts</a>
          </div>
        </li>
        <li class="dropdown"><a href="#">Topics ▾</a>
          <div class="dropdown-menu">
            <a href="/topics/ai-agents-guide.html">🤖 AI Agents Guide</a>
            <a href="/topics/best-ai-tools-2025.html">🛠️ Best AI Tools 2025</a>
            <a href="/topics/chatgpt-job-search.html">💬 ChatGPT Tips</a>
            <a href="/topics/n8n-beginners-guide.html">📊 n8n Guide</a>
            <a href="/topics/prompt-engineering.html">🎯 Prompt Engineering</a>
            <a href="/topics/langchain-llm-apps.html">🔗 LangChain</a>
          </div>
        </li>
        <li><a href="/blog.html#about">About</a></li>
      </ul>
      <button class="hamburger" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </nav>
  <div class="mobile-menu" id="mobileMenu">
    <a href="/">Home</a><a href="/blog.html">Blog</a>
    <a href="/workflows/n8n-job-search-automation.html">🔍 n8n Job Search</a>
    <a href="/workflows/linkedin-automation.html">💼 LinkedIn Automation</a>
    <a href="/workflows/ai-resume-tailor.html">📄 AI Resume Tailor</a>
    <a href="/workflows/make-job-tracker.html">📊 Make.com Tracker</a>
    <a href="/workflows/zapier-job-alerts.html">🔔 Zapier Job Alerts</a>
    <a href="/topics/ai-agents-guide.html">🤖 AI Agents</a>
    <a href="/topics/best-ai-tools-2025.html">🛠️ Best AI Tools</a>
    <a href="/topics/chatgpt-job-search.html">💬 ChatGPT Tips</a>
    <a href="/topics/n8n-beginners-guide.html">📊 n8n Guide</a>
    <a href="/topics/prompt-engineering.html">🎯 Prompts</a>
    <a href="/topics/langchain-llm-apps.html">🔗 LangChain</a>
  </div>"""

FOOTER = """  <footer class="footer">
    <div class="footer-grid">
      <div>
        <div style="font-size:1.4rem;font-weight:800;margin-bottom:0.75rem;">🤖 AllAboutAI</div>
        <p style="color:var(--muted);font-size:0.95rem;line-height:1.7;max-width:280px;">Your guide to AI automation. Free workflows, guides, and tools for the AI-powered generation.</p>
      </div>
      <div><h4>Workflows</h4><ul>
        <li><a href="/workflows/n8n-job-search-automation.html">n8n Job Search</a></li>
        <li><a href="/workflows/linkedin-automation.html">LinkedIn Automation</a></li>
        <li><a href="/workflows/ai-resume-tailor.html">AI Resume Tailor</a></li>
        <li><a href="/workflows/make-job-tracker.html">Make.com Tracker</a></li>
        <li><a href="/workflows/zapier-job-alerts.html">Zapier Job Alerts</a></li>
      </ul></div>
      <div><h4>Topics</h4><ul>
        <li><a href="/topics/ai-agents-guide.html">AI Agents Guide</a></li>
        <li><a href="/topics/best-ai-tools-2025.html">Best AI Tools 2025</a></li>
        <li><a href="/topics/chatgpt-job-search.html">ChatGPT Job Search</a></li>
        <li><a href="/topics/n8n-beginners-guide.html">n8n Guide</a></li>
        <li><a href="/topics/prompt-engineering.html">Prompt Engineering</a></li>
      </ul></div>
      <div><h4>About</h4><ul>
        <li><a href="/blog.html">All Posts</a></li>
        <li><a href="/blog.html#about">About Us</a></li>
        <li><a href="/sitemap.xml">Sitemap</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <span>© 2025 AllAboutAI | thatai.me</span>
      <span>Built by Akash with ❤️ + n8n</span>
    </div>
  </footer>"""

SCRIPT = """  <script>
    window.addEventListener('scroll', () => {
      const bar = document.getElementById('progressBar');
      if(bar) bar.style.width = (window.scrollY / (document.body.scrollHeight - window.innerHeight) * 100) + '%';
    });
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    if(hamburger) hamburger.addEventListener('click', () => mobileMenu.classList.toggle('open'));
    document.querySelectorAll('.faq-question').forEach(q => {
      q.addEventListener('click', () => {
        q.nextElementSibling.classList.toggle('open');
        const icon = q.querySelector('.faq-icon');
        if(icon) icon.classList.toggle('open');
      });
    });
    const observer = new IntersectionObserver(entries => {
      entries.forEach(e => { if(e.isIntersecting) e.target.classList.add('visible'); });
    }, {threshold: 0.1});
    document.querySelectorAll('[data-animate]').forEach(el => observer.observe(el));
    const tocLinks = document.querySelectorAll('.toc a');
    const sections = document.querySelectorAll('h2[id], h3[id]');
    window.addEventListener('scroll', () => {
      let current = '';
      sections.forEach(s => { if(window.scrollY >= s.offsetTop - 120) current = s.id; });
      tocLinks.forEach(a => { a.classList.toggle('active', a.getAttribute('href') === '#' + current); });
    });
  </script>"""

print("Templates ready")
