# caguei metasploit

```text
   ____    _    ____ _   _ _____ ___
  / ___|  / \  / ___| | | | ____|_ _|
 | |     / _ \| |  _| | | |  _|  | |
 | |___ / ___ \ |_| | |_| | |___ | |
  \____/_/   \_\____|\___/|_____|___|

  __  __ _____ _____  _    ____  ____  _     ___ ___ _____
 |  \/  | ____|_   _|/ \  / ___||  _ \| |   / _ \_ _|_   _|
 | |\/| |  _|   | | / _ \ \___ \| |_) | |  | | | | |  | |
 | |  | | |___  | |/ ___ \ ___) |  __/| |__| |_| | |  | |
 |_|  |_|_____| |_/_/   \_\____/|_|   |_____\___/___| |_|


```

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

Para exibir novamente o banner:

```bash
cmsp banner
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

## Modelo de segurança

O scope guard falha de forma fechada: o arquivo deve declarar `authorized_use_only: true`, uma justificativa de autorização e ao menos uma rede CIDR ou hostname. A confirmação deriva dessa justificativa; qualquer mudança nela invalida a confirmação anterior. Na importação, ativos fora do escopo são ignorados e, se nenhum ativo for aceito, a operação falha. Auditorias e relatórios também exigem a confirmação.

Limite conhecido: a ferramenta valida autorização declarada, mas não consegue provar juridicamente que ela existe. O operador continua responsável por obter permissão escrita e respeitar leis, contratos e políticas aplicáveis.

## Desenvolvimento e testes

```bash
python -m pip install pytest
python -m pytest
```

Consulte [ARCHITECTURE.md](ARCHITECTURE.md) para os limites e pontos de extensão. Novos módulos devem analisar apenas registros locais e retornar achados; módulos que abram sockets, executem comandos remotos ou alterem alvos não serão aceitos.


Não versionar `.cmsp`, scopes reais, XMLs de varredura ou relatórios. O `.gitignore` já cobre os caminhos padrão.

## Uso responsável

Use somente em ativos próprios ou com autorização explícita. Achados são indícios de configuração e precisam de validação humana; não equivalem, isoladamente, a vulnerabilidades confirmadas.
