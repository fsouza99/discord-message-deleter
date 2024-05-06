## Apagador de mensagens do Discord

Este projeto permite a um usuário autenticado apagar suas mensagens em um servidor no Discord, utilizando a ferramenta Selenium (v4.17.2) para interação virtual programada com a versão web da aplicação em PT-BR.

Toda a execução é feita em função dos parâmetros em *settings.py*, arquivo que deve ser examinado pelo usuário. Assim é possível determinar, por exemplo, uma chave de busca que indica as mensagens a serem apagadas.

### Limitações

A busca pelas mensagens alvo da deleção tira proveito do sistema de busca do próprio Discord.

O programa tentará excluir mensagens em ordem, da mais antiga para a mais recente. No entanto, não é possível garantir isso, e uma ordem de exclusão aparentemente aleatória pode ocorrer.

Deve-se observar também que a exclusão de várias mensagens pode não se refletir instantaneamente em todos os clientes.

### Créditos

* [Discord](https://discord.com)
* [Selenium](https://selenium.dev/)
