# Arquitetura

```text
CLI (argparse)
  ├── Scope guard ── valida JSON, confirmação e pertinência dos ativos
  ├── Importador ─── lê Nmap XML, filtra e normaliza
  ├── Catálogo ───── executa regras puras sobre registros locais
  ├── Storage ────── SQLite por workspace
  └── Relatórios ─── Markdown / JSON / HTML
```

## Fronteiras de confiança

O XML e o scope são entradas não confiáveis. O parser XML usado não resolve entidades externas nem acessa a rede. Consultas SQLite usam parâmetros. O HTML escapa todo o Markdown produzido antes de renderizá-lo. Nenhum componente possui uma primitiva de rede ou execução de processos.

## Modelo de dados

Cada workspace contém `hosts`, `services` e `findings`. Serviços são únicos por host, porta e protocolo. Achados são deduplicados por módulo, host, porta e título. Reimportações atualizam inventário sem duplicá-lo.

## Extensão segura

Um módulo recebe linhas imutáveis de serviços e retorna objetos `Finding`. Registre-o em `MODULES`. Mantenha módulos determinísticos, somente leitura e sem rede. Teste pelo menos um caso positivo, um negativo e a severidade/recomendação.

## Fora de escopo

Descoberta ativa, exploração, payloads, sessões remotas, brute force, persistência, evasão, movimentação lateral, coleta de credenciais e alteração de sistemas-alvo.

