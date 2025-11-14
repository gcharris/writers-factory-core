/**
 * Export utilities for Writers Factory.
 * Handles exporting scenes/manuscripts to various formats.
 */

/**
 * Export content to Markdown file (.md)
 */
export function exportToMarkdown(title, content) {
  const blob = new Blob([content], { type: 'text/markdown' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${sanitizeFilename(title)}.md`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Export content to plain text file (.txt)
 */
export function exportToText(title, content) {
  // Remove markdown formatting
  const plainText = content
    .replace(/[#*`_~[\]()]/g, '')
    .replace(/\n\n+/g, '\n\n');

  const blob = new Blob([plainText], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${sanitizeFilename(title)}.txt`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Export content to HTML file (.html)
 */
export function exportToHTML(title, content) {
  const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${escapeHtml(title)}</title>
  <style>
    body {
      max-width: 800px;
      margin: 40px auto;
      padding: 0 20px;
      font-family: Georgia, serif;
      line-height: 1.6;
      color: #333;
    }
    h1 { font-size: 2em; margin-bottom: 0.5em; }
    h2 { font-size: 1.5em; margin-top: 1em; }
    h3 { font-size: 1.2em; margin-top: 0.8em; }
    p { margin: 1em 0; }
    code {
      background-color: #f4f4f4;
      padding: 2px 6px;
      border-radius: 3px;
      font-family: monospace;
    }
    pre {
      background-color: #f4f4f4;
      padding: 12px;
      border-radius: 6px;
      overflow-x: auto;
    }
    blockquote {
      border-left: 4px solid #ddd;
      padding-left: 16px;
      margin-left: 0;
      color: #666;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 1em 0;
    }
    table th, table td {
      border: 1px solid #ddd;
      padding: 8px;
      text-align: left;
    }
    table th {
      background-color: #f4f4f4;
    }
  </style>
</head>
<body>
  <h1>${escapeHtml(title)}</h1>
  ${convertMarkdownToHTML(content)}
</body>
</html>
  `.trim();

  const blob = new Blob([htmlContent], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `${sanitizeFilename(title)}.html`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

/**
 * Convert markdown to HTML (basic implementation)
 */
function convertMarkdownToHTML(markdown) {
  let html = markdown;

  // Code blocks (must come before inline code)
  html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, (match, lang, code) => {
    return `<pre><code>${escapeHtml(code.trim())}</code></pre>`;
  });

  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Headers
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

  // Bold and italic
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');

  // Strikethrough
  html = html.replace(/~~(.+?)~~/g, '<del>$1</del>');

  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

  // Images
  html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1">');

  // Blockquotes
  html = html.replace(/^> (.+)$/gim, '<blockquote>$1</blockquote>');

  // Unordered lists
  html = html.replace(/^\* (.+)$/gim, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

  // Ordered lists
  html = html.replace(/^\d+\. (.+)$/gim, '<li>$1</li>');

  // Horizontal rules
  html = html.replace(/^---$/gim, '<hr>');

  // Paragraphs
  html = html.replace(/\n\n/g, '</p><p>');
  html = `<p>${html}</p>`;

  // Clean up empty paragraphs and fix nesting
  html = html.replace(/<p><\/p>/g, '');
  html = html.replace(/<p>(<h[1-6]>)/g, '$1');
  html = html.replace(/(<\/h[1-6]>)<\/p>/g, '$1');
  html = html.replace(/<p>(<pre>)/g, '$1');
  html = html.replace(/(<\/pre>)<\/p>/g, '$1');
  html = html.replace(/<p>(<ul>)/g, '$1');
  html = html.replace(/(<\/ul>)<\/p>/g, '$1');
  html = html.replace(/<p>(<blockquote>)/g, '$1');
  html = html.replace(/(<\/blockquote>)<\/p>/g, '$1');
  html = html.replace(/<p>(<hr>)/g, '$1');
  html = html.replace(/(<hr>)<\/p>/g, '$1');

  return html;
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Sanitize filename (remove invalid characters)
 */
function sanitizeFilename(filename) {
  return filename
    .replace(/[<>:"/\\|?*]/g, '')
    .replace(/\s+/g, '_')
    .substring(0, 100);
}

/**
 * Export entire manuscript (all scenes combined)
 */
export async function exportManuscript(format = 'md') {
  // Fetch manuscript tree
  const response = await fetch('http://localhost:8000/api/manuscript/tree');
  const data = await response.json();

  let fullContent = `# ${data.title}\n\n`;

  // Iterate through acts, chapters, scenes
  for (const act of data.acts || []) {
    fullContent += `\n\n# ${act.title}\n\n`;

    for (const chapter of act.chapters || []) {
      fullContent += `\n## ${chapter.title}\n\n`;

      for (const scene of chapter.scenes || []) {
        // Fetch scene content
        const sceneResp = await fetch(`http://localhost:8000/api/manuscript/explants-v1/scenes/${scene.id}`);
        const sceneData = await sceneResp.json();

        fullContent += `\n### ${scene.title}\n\n`;
        fullContent += sceneData.content + '\n\n';
      }
    }
  }

  // Export based on format
  switch (format) {
    case 'md':
      exportToMarkdown(data.title, fullContent);
      break;
    case 'txt':
      exportToText(data.title, fullContent);
      break;
    case 'html':
      exportToHTML(data.title, fullContent);
      break;
    default:
      exportToMarkdown(data.title, fullContent);
  }
}
