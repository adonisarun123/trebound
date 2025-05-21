/* Auto accordion: wrap every H2 section into <details>/<summary> */
function transformSections() {
  const body = document.querySelector('.markdown-body');
  if (!body) return;
  const children = Array.from(body.children);
  for (let i = 0; i < children.length; i++) {
    const node = children[i];
    if (node.tagName === 'H2') {
      const details = document.createElement('details');
      details.className = 'accordion';
      const summary = document.createElement('summary');
      summary.innerHTML = node.innerHTML;
      details.appendChild(summary);
      const wrap = document.createElement('div');
      wrap.className = 'accordion-content';
      let next = node.nextSibling;
      while (next && !(next.tagName && next.tagName.match(/^H[12]$/))) {
        const temp = next.nextSibling;
        wrap.appendChild(next);
        next = temp;
      }
      details.appendChild(wrap);
      node.parentNode.insertBefore(details, node);
      node.remove();
    }
  }
}

// run after DOM ready
document.addEventListener('DOMContentLoaded', () => {
  transformSections();
}); 