const fs = require('fs');

const pages = {
  'markets/australia.html': 'australia.md',
  'markets/china.html': 'china.md',
  'markets/dubai.html': 'dubai.md',
  'markets/indonesia.html': 'Indonesia.md',
  'markets/japan.html': 'japan.md',
  'markets/malaysia.html': 'malaysia.md',
  'markets/north-america.html': 'North America.md',
  'markets/philippines.html': 'Philippines.md',
  'markets/singapore.html': 'singapore.md',
  'markets/sri-lanka.html': 'srilanka.md',
  'markets/thailand.html': 'thailand.md',
  'markets/uae.html': 'uae.md',
  'markets/vietnam.html': 'vietnam.md'
};

// Additional markets
pages['markets/cambodia.html'] = 'cambodia.md';
pages['markets/hong-kong.html'] = 'hong-kong.md';
pages['markets/laos.html'] = 'laos.md';
pages['markets/qatar.html'] = 'Qatar.md';
pages['markets/saudi.html'] = 'Saudi.md';

function embed(htmlPath, mdPath) {
  const markdown = fs.readFileSync(mdPath, 'utf8');
  let html = fs.readFileSync(htmlPath, 'utf8');
  html = html.replace(/<script id="md"[\s\S]*?<\/script>/gm, '');
  html = html.replace(/<script>[\s\S]*?<\/script>\s*<\/body>/gm, '</body>');
  const escape = markdown.replace(/</g, '&lt;');
  const block = `\n    <!-- embedded markdown (auto) -->\n    <script id="md" type="text/markdown">\n${escape}\n    </script>\n\n    <script>\n      document.getElementById('content').innerHTML = marked.parse(document.getElementById('md').textContent);\n    </script>\n    <script src="../assets/app.js"></script>`;
  html = html.replace('</body>', `${block}\n</body>`);
  fs.writeFileSync(htmlPath, html);
  console.log('✔', htmlPath);
}

for (const [html, md] of Object.entries(pages)) {
  if (fs.existsSync(html) && fs.existsSync(md)) embed(html, md);
  else console.warn('⚠️ missing', html, md);
} 