# Contribuindo

Antes de enviar uma mudança, execute `python -m pytest` e confirme que nenhum dado real de laboratório foi incluído.

Contribuições devem manter a ferramenta passiva e offline. Módulos podem interpretar inventário e configurações importadas, mas não podem abrir conexões, explorar falhas, executar ações remotas, testar credenciais, instalar persistência, evitar controles ou modificar alvos. Inclua testes e documentação para todo comportamento novo.

Ao relatar um bug, use dados sintéticos e endereços reservados para documentação, como `192.0.2.0/24`, `198.51.100.0/24` e `203.0.113.0/24`.
