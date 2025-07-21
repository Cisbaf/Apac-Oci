import React from 'react';
import ReactMarkdown from 'react-markdown';
import dedent from 'dedent';
import { ApacRequest } from '../schemas/apacRequest';

interface MarkdownProps {
  apacRequest: ApacRequest;
}

export default function ApacRequestDataMarkDown({ apacRequest }: MarkdownProps) {
  const markdown = dedent(`
    ## Identificação do estabelecimento de Saúde

    | Nome do Estabelecimento       | CNES       |
    | ----------------------------- |:----------:|
    | ${apacRequest.establishment.name} | ${apacRequest.establishment.cnes} |
  `);

  return (
    <div className="markdown">
      <ReactMarkdown>{markdown}</ReactMarkdown>
    </div>
  );
}
