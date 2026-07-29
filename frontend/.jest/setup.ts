import '@testing-library/jest-dom'

// jest-environment-jsdom não expõe `structuredClone` no global (mesmo em Node
// com suporte nativo) — código de produção que o usa (ex.: finishFormApacRequest.tsx)
// quebra em teste sem isso. Polyfill simples: os dados clonados aqui são sempre
// JSON-serializáveis (formulário), não precisa da fidelidade completa da API real.
if (typeof global.structuredClone !== 'function') {
  global.structuredClone = <T>(value: T): T => JSON.parse(JSON.stringify(value));
}