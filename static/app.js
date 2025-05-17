// static/app.js
// Mobile burger interaction
const navToggle = document.getElementById('nav-toggle');
const burger = document.querySelector('.burger');

burger?.addEventListener('click', () => {
  navToggle.checked = !navToggle.checked;
});

// Simple parallax effect for hero on scroll
window.addEventListener('scroll', () => {
  const scrolled = window.pageYOffset;
  const parallaxEls = document.querySelectorAll('.parallax');
  parallaxEls.forEach(el => {
    el.style.backgroundPositionY = `${scrolled * -0.3}px`;
  });
});

// Render markdown content dynamically when a page includes an element
//   <div id="md-content" data-src="path/to/file.md"></div>
document.addEventListener('DOMContentLoaded', () => {
  const mdContainer = document.getElementById('md-content');
  if (mdContainer && mdContainer.dataset.src) {
    const mdPath = mdContainer.dataset.src;
    // Ensure Marked library is loaded
    function render(mdText) {
      if (window.marked) {
        mdContainer.innerHTML = window.marked.parse(mdText);
      } else {
        mdContainer.textContent = 'Error: marked.js not loaded.';
      }
    }
    fetch(mdPath)
      .then((resp) => resp.text())
      .then(render)
      .catch((err) => {
        console.error(err);
        mdContainer.textContent = 'Failed to load content.';
      });
  }

  /* Convert H2 sections into collapsible pastel blocks */
  const prose = document.querySelector('.prose');
  if (prose) {
    const h2s = Array.from(prose.querySelectorAll('h2'));
    h2s.forEach((h2) => {
      const detail = document.createElement('details');
      detail.classList.add('section-block');
      const summary = document.createElement('summary');
      summary.textContent = h2.textContent;
      detail.appendChild(summary);

      // Move all following siblings until next H2 into this details
      let sibling = h2.nextSibling;
      while (sibling && !(sibling.tagName === 'H2')) {
        const next = sibling.nextSibling;
        detail.appendChild(sibling);
        sibling = next;
      }
      // Replace original H2 with the details block
      h2.replaceWith(detail);
      // Open first three sections by default
      const index = Array.from(prose.children).indexOf(detail);
      if (index < 3) detail.open = true;
    });
  }
}); 