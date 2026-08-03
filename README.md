# caguei metasploit

Uma CLI **defensiva, offline e orientada a evidências** para organizar resultados de laboratórios autorizados. O nome é irreverente; o comportamento é deliberadamente conservador. O projeto é apenas inspirado na ideia de uma console modular: não copia código, marca ou interface do Metasploit.

> Este software não contém exploits, payloads, persistência, evasão, execução remota ou scanner de rede. Ele nunca inicia conexões com os alvos: analisa somente arquivos Nmap XML já existentes.

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

## Modelo de segurança

O scope guard falha de forma fechada: o arquivo deve declarar `authorized_use_only: true`, uma justificativa de autorização e ao menos uma rede CIDR ou hostname. A confirmação deriva dessa justificativa; qualquer mudança nela invalida a confirmação anterior. Na importação, ativos fora do escopo são ignorados e, se nenhum ativo for aceito, a operação falha. Auditorias e relatórios também exigem a confirmação.

Limite conhecido: a ferramenta valida autorização declarada, mas não consegue provar juridicamente que ela existe. O operador continua responsável por obter permissão escrita e respeitar leis, contratos e políticas aplicáveis.

## Desenvolvimento e testes

```bash
python -m pip install pytest
python -m pytest
```

Consulte [ARCHITECTURE.md](ARCHITECTURE.md) para os limites e pontos de extensão. Novos módulos devem analisar apenas registros locais e retornar achados; módulos que abram sockets, executem comandos remotos ou alterem alvos não serão aceitos.

## Publicar no GitHub

1. Crie um repositório vazio no GitHub, preferencialmente privado durante a revisão inicial.
2. Revise o nome, o arquivo `LICENSE` e remova dados reais de laboratório.
3. Execute os testes.
4. Publique:

```bash
git init
git add .
git commit -m "Initial safe defensive MVP"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/caguei-metasploit.git
git push -u origin main
```

Não versionar `.cmsp`, scopes reais, XMLs de varredura ou relatórios. O `.gitignore` já cobre os caminhos padrão.

## Uso responsável

Use somente em ativos próprios ou com autorização explícita. Achados são indícios de configuração e precisam de validação humana; não equivalem, isoladamente, a vulnerabilidades confirmadas.
