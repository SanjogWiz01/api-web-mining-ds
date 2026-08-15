/* ═══════════════════════════════════════════════════════════
   API MASTERY GUIDE — app.js
   Advanced API & Web Mining for Data Science
   ═══════════════════════════════════════════════════════════ */

'use strict';

// ── Navbar scroll effect ─────────────────────────────────────
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
});

// ── Mobile Nav Toggle ────────────────────────────────────────
const navToggle = document.getElementById('navToggle');
const navLinks  = document.getElementById('navLinks');
navToggle.addEventListener('click', () => {
  navLinks.classList.toggle('open');
  navToggle.textContent = navLinks.classList.contains('open') ? '✕' : '☰';
});

// Close nav on link click (mobile)
navLinks.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    navToggle.textContent = '☰';
  });
});

// ── Scroll Reveal ────────────────────────────────────────────
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

document.querySelectorAll([
  '.topic-card', '.method-card', '.stat-card', '.tip-card',
  '.tool-card', '.docs-type-card', '.cs-card', '.feature-item',
  '.check-item', '.cl-item', '.endpoint-row', '.auth-info',
  '.code-block-wrapper', '.status-codes-box', '.url-anatomy',
  '.rate-limit-visual', '.error-flow', '.exception-hierarchy',
  '.oauth-flow', '.fastapi-features', '.security-checklist',
  '.docs-checklist', '.gitignore-box'
].join(',')).forEach(el => {
  el.classList.add('reveal');
  revealObserver.observe(el);
});

// ── Copy Code ────────────────────────────────────────────────
function copyCode(btn) {
  const wrapper = btn.closest('.code-block-wrapper') || btn.closest('.mini-code')?.parentElement;
  const codeEl = wrapper ? wrapper.querySelector('code') : null;
  if (!codeEl) return;
  const text = codeEl.innerText;
  navigator.clipboard.writeText(text).then(() => {
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(() => {
      btn.textContent = 'Copy';
      btn.classList.remove('copied');
    }, 2000);
  }).catch(() => {
    // Fallback for older browsers
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    btn.textContent = 'Copied!';
    setTimeout(() => { btn.textContent = 'Copy'; }, 2000);
  });
}

// ── Auth Tabs ────────────────────────────────────────────────
function showAuth(type) {
  const tabs   = document.querySelectorAll('.auth-tab');
  const panels = document.querySelectorAll('.auth-panel');

  tabs.forEach(t => t.classList.remove('active'));
  panels.forEach(p => p.classList.remove('active'));

  document.getElementById(`tab-${type}`)?.classList.add('active');
  document.getElementById(`auth-${type}`)?.classList.add('active');
}

// ── FastAPI Tabs ─────────────────────────────────────────────
function showFastAPI(type) {
  const tabs   = document.querySelectorAll('.fa-tab');
  const panels = document.querySelectorAll('.fa-panel');

  tabs.forEach(t => t.classList.remove('active'));
  panels.forEach(p => p.classList.remove('active'));

  document.getElementById(`fatab-${type}`)?.classList.add('active');
  document.getElementById(`fa-${type}`)?.classList.add('active');
}

// ── Playground Response Tabs ─────────────────────────────────
function showPGTab(tabName, btn) {
  const tabs    = document.querySelectorAll('.pg-tab');
  const contents = {
    body:    document.getElementById('pg-response-body'),
    headers: document.getElementById('pg-response-headers'),
    curl:    document.getElementById('pg-response-curl'),
  };

  tabs.forEach(t => t.classList.remove('active'));
  Object.values(contents).forEach(c => { if (c) c.style.display = 'none'; });

  btn.classList.add('active');
  if (contents[tabName]) contents[tabName].style.display = 'block';
}

// ── Method body toggle in playground ────────────────────────
const pgMethod   = document.getElementById('pg-method');
const pgBodyWrap = document.getElementById('pg-body-wrap');

if (pgMethod) {
  pgMethod.addEventListener('change', () => {
    const needsBody = ['POST', 'PUT', 'PATCH'].includes(pgMethod.value);
    pgBodyWrap.style.display = needsBody ? 'block' : 'none';
  });
}

// ── Playground — Live Request ─────────────────────────────────
async function sendPlaygroundRequest() {
  const method   = document.getElementById('pg-method').value;
  const url      = document.getElementById('pg-endpoint').value;
  const bodyText = document.getElementById('pg-body').value.trim();

  const sendBtn       = document.getElementById('pg-send');
  const statusBadge   = document.getElementById('pg-status-badge');
  const responseMeta  = document.getElementById('pg-meta');
  const timeEl        = document.getElementById('pg-time');
  const sizeEl        = document.getElementById('pg-size');
  const bodyEl        = document.getElementById('pg-response-body');
  const headersEl     = document.getElementById('pg-response-headers');
  const curlEl        = document.getElementById('pg-response-curl');
  const curlDisplay   = document.getElementById('pg-curl-display');

  // Reset UI
  sendBtn.textContent = 'Sending...';
  sendBtn.disabled = true;
  statusBadge.textContent = '';
  statusBadge.className = 'pg-status-inline';
  bodyEl.innerHTML = '<div class="pg-loading">⏳ Waiting for response...</div>';
  headersEl.textContent = '';
  curlEl.textContent = '';
  responseMeta.style.display = 'none';

  // Build curl command
  const curlCmd = buildCurlCommand(method, url, bodyText);
  curlEl.textContent = curlCmd;
  curlDisplay.style.display = 'block';
  curlDisplay.textContent = curlCmd;

  const start = performance.now();

  try {
    const opts = { method };

    if (['POST', 'PUT', 'PATCH'].includes(method) && bodyText) {
      try {
        JSON.parse(bodyText);
        opts.headers = { 'Content-Type': 'application/json' };
        opts.body = bodyText;
      } catch {
        opts.body = bodyText;
      }
    }

    const response = await fetch(url, opts);
    const elapsed  = Math.round(performance.now() - start);
    const text     = await response.text();
    const size     = new Blob([text]).size;

    // Status badge
    const code = response.status;
    const clsMap = code >= 500 ? 'pg-status-5xx' : code >= 400 ? 'pg-status-4xx' : 'pg-status-2xx';
    statusBadge.textContent = `${code} ${response.statusText}`;
    statusBadge.className   = `pg-status-inline ${clsMap}`;

    // Meta info
    responseMeta.style.display = 'flex';
    timeEl.textContent = `${elapsed}ms`;
    sizeEl.textContent = formatBytes(size);

    // Body — pretty print JSON
    let displayText = text;
    try {
      const parsed = JSON.parse(text);
      displayText = JSON.stringify(parsed, null, 2);
      bodyEl.innerHTML = syntaxHighlightJSON(displayText);
    } catch {
      bodyEl.textContent = text;
    }

    // Headers
    const hdrs = [];
    response.headers.forEach((value, key) => {
      hdrs.push(`${key}: ${value}`);
    });
    headersEl.textContent = hdrs.join('\n');

  } catch (err) {
    const elapsed = Math.round(performance.now() - start);
    statusBadge.textContent = 'Network Error';
    statusBadge.className   = 'pg-status-inline pg-status-5xx';
    bodyEl.textContent = `Error: ${err.message}\n\n(CORS restrictions may apply for some APIs when calling from a browser)`;
    responseMeta.style.display = 'flex';
    timeEl.textContent = `${elapsed}ms`;
    sizeEl.textContent = '-';
  } finally {
    sendBtn.textContent = 'Send →';
    sendBtn.disabled = false;
  }
}

// ── Build curl equivalent ────────────────────────────────────
function buildCurlCommand(method, url, body) {
  let cmd = `curl -X ${method} \\\n  "${url}"`;
  cmd += ` \\\n  -H "Accept: application/json"`;
  if (body) {
    cmd += ` \\\n  -H "Content-Type: application/json"`;
    cmd += ` \\\n  -d '${body}'`;
  }
  return cmd;
}

// ── Format bytes ─────────────────────────────────────────────
function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

// ── Syntax highlight JSON ────────────────────────────────────
function syntaxHighlightJSON(json) {
  json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return json.replace(
    /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
    (match) => {
      let cls = 'num';
      if (/^"/.test(match)) {
        cls = /:$/.test(match) ? 'json-key' : 'str';
      } else if (/true|false/.test(match)) {
        cls = 'kw';
      } else if (/null/.test(match)) {
        cls = 'cm';
      }
      return `<span class="${cls}">${match}</span>`;
    }
  );
}

// ── Active nav link on scroll ────────────────────────────────
const sections = document.querySelectorAll('section[id]');
const navLinksAll = document.querySelectorAll('.nav-link');

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.getAttribute('id');
      navLinksAll.forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
      });
    }
  });
}, { rootMargin: '-40% 0px -55% 0px' });

sections.forEach(s => sectionObserver.observe(s));

// ── Smooth entrance animation for hero ───────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const heroContent = document.querySelector('.hero-content');
  if (heroContent) {
    heroContent.style.opacity = '0';
    heroContent.style.transform = 'translateY(30px)';
    heroContent.style.transition = 'all 0.8s cubic-bezier(0.16, 1, 0.3, 1)';
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        heroContent.style.opacity = '1';
        heroContent.style.transform = 'translateY(0)';
      });
    });
  }

  // Animate RL bars on scroll into view
  const rlBars = document.querySelectorAll('.rl-bar');
  const rlObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        rlBars.forEach((bar, i) => {
          setTimeout(() => {
            bar.style.transform = 'scaleY(1)';
            bar.style.opacity = '1';
          }, i * 100);
        });
        rlObserver.disconnect();
      }
    });
  }, { threshold: 0.5 });

  rlBars.forEach(bar => {
    bar.style.transform = 'scaleY(0)';
    bar.style.opacity = '0';
    bar.style.transformOrigin = 'bottom';
    bar.style.transition = 'all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1)';
  });

  const rlSection = document.querySelector('.rate-limit-visual');
  if (rlSection) rlObserver.observe(rlSection);
});

// ── Keyboard shortcut: / → focus playground ─────────────────
document.addEventListener('keydown', (e) => {
  if (e.key === '/' && document.activeElement.tagName !== 'INPUT' &&
      document.activeElement.tagName !== 'TEXTAREA' &&
      document.activeElement.tagName !== 'SELECT') {
    e.preventDefault();
    document.getElementById('playground')?.scrollIntoView({ behavior: 'smooth' });
    setTimeout(() => document.getElementById('pg-method')?.focus(), 600);
  }
});

// ── Tooltip on URL parts ─────────────────────────────────────
document.querySelectorAll('.url-part[data-label]').forEach(part => {
  part.title = part.getAttribute('data-label');
});

// ── Export copyCode to global scope ─────────────────────────
window.copyCode = copyCode;
window.showAuth = showAuth;
window.showFastAPI = showFastAPI;
window.showPGTab = showPGTab;
window.sendPlaygroundRequest = sendPlaygroundRequest;
