import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import './MarkdownDisplay.css';
import './MarkdownDisplay.css';

function MarkdownDisplay({ content }) {
  return (
    <div className="markdown-display">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ node, children, ...props }) => <h1 className="md-h1" {...props}>{children}</h1>,
          h2: ({ node, children, ...props }) => <h2 className="md-h2" {...props}>{children}</h2>,
          h3: ({ node, children, ...props }) => <h3 className="md-h3" {...props}>{children}</h3>,
          h4: ({ node, children, ...props }) => <h4 className="md-h4" {...props}>{children}</h4>,
          h5: ({ node, children, ...props }) => <h5 className="md-h5" {...props}>{children}</h5>,
          h6: ({ node, children, ...props }) => <h6 className="md-h6" {...props}>{children}</h6>,
          p: ({ node, children, ...props }) => <p className="md-paragraph" {...props}>{children}</p>,
          ul: ({ node, children, ...props }) => <ul className="md-ul" {...props}>{children}</ul>,
          ol: ({ node, children, ...props }) => <ol className="md-ol" {...props}>{children}</ol>,
          li: ({ node, children, ...props }) => <li className="md-li" {...props}>{children}</li>,
          blockquote: ({ node, children, ...props }) => <blockquote className="md-blockquote" {...props}>{children}</blockquote>,
          table: ({ node, children, ...props }) => <table className="md-table" {...props}>{children}</table>,
          thead: ({ node, children, ...props }) => <thead {...props}>{children}</thead>,
          tbody: ({ node, children, ...props }) => <tbody {...props}>{children}</tbody>,
          tr: ({ node, children, ...props }) => <tr className="md-tr" {...props}>{children}</tr>,
          th: ({ node, children, ...props }) => <th className="md-th" {...props}>{children}</th>,
          td: ({ node, children, ...props }) => <td className="md-td" {...props}>{children}</td>,
          code: ({ node, inline, className, children, ...props }) => {
            const match = /language-(\w+)/.exec(className || '');
            return !inline && match ? (
              <SyntaxHighlighter
                style={atomDark}
                language={match[1]}
                PreTag="div"
                className="md-code-block"
                {...props}
              >
                {String(children).replace(/\n$/, '')}
              </SyntaxHighlighter>
            ) : (
              <code className="md-inline-code" {...props}>
                {children}
              </code>
            );
          },
          a: ({ node, children, ...props }) => <a className="md-link" target="_blank" rel="noopener noreferrer" {...props}>{children}</a>,
          strong: ({ node, ...props }) => <strong className="md-strong" {...props} />,
          em: ({ node, ...props }) => <em className="md-em" {...props} />,
          hr: ({ node, ...props }) => <hr className="md-hr" {...props} />,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

export default MarkdownDisplay;
