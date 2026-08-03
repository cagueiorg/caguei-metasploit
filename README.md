# caguei metasploit

Uma CLI **defensiva, offline e orientada a evidências** para organizar resultados de laboratórios autorizados. 

## Recursos do MVP

- workspaces isolados em SQLite;
- scope guard obrigatório, com redes/hosts autorizados e confirmação vinculada à autorização;
- importação de Nmap XML, descartando hosts fora do escopo;
- catálogo extensível de auditorias não destrutivas;
- checagens de protocolos sem criptografia, interfaces de gestão e serviços não identificados;
- relatórios Markdown, JSON e HTML;
- biblioteca padrão Python no runtime; testes com pytest.

## Instalação

Requer Python 3.10 ou mais recente.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -e .
```

## Uso rápido

```bash
cmsp workspace create meu-lab
```

Copie `.cmsp/meu-lab/scope.example.json` para `scope.json`, substitua as redes/hosts pelos ativos expressamente autorizados e descreva a autorização. Gere a confirmação:

```bash
cmsp scope-ack scope.json
```

Use o valor retornado em cada operação protegida:

```bash
cmsp import-nmap meu-lab scan.xml --scope scope.json --ack AUTORIZADO-xxxxxxxxxxxx
cmsp modules list
cmsp audit meu-lab all --scope scope.json --ack AUTORIZADO-xxxxxxxxxxxx
cmsp report meu-lab --scope scope.json --ack AUTORIZADO-xxxxxxxxxxxx --format md --output relatorio.md
```

O diretório de dados padrão é `.cmsp`; altere com `--data-dir CAMINHO` ou `CMSP_HOME`.

## Desenvolvimento e testes

```bash
python -m pip install pytest
python -m pytest
```

Consulte [ARCHITECTURE.md](ARCHITECTURE.md) para os limites e pontos de extensão. Novos módulos devem analisar apenas registros locais e retornar achados; módulos que abram sockets, executem comandos remotos ou alterem alvos não serão aceitos.




## Uso responsável

Use somente em ativos próprios ou com autorização explícita. Achados são indícios de configuração e precisam de validação humana; não equivalem, isoladamente, a vulnerabilidades confirmadas.
