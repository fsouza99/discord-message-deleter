## Apagador de mensagens do Discord

Este projeto permite a um usuário autenticado apagar suas mensagens em um servidor no Discord, utilizando a ferramenta Selenium (v4.17.2) para interação virtual programada com a versão web da aplicação em PT-BR.

O código em *main.py* contorna eventuais erros pela repetição do procedimento de busca e remoção de mensagens.

A busca pelas mensagens alvo da deleção tira proveito do próprio sistema de busca do Discord.

Toda a execução é feita em função dos parâmetros em *settings.py*, arquivo que deve ser examinado pelo usuário.

### Créditos

* [Discord](https://discord.com)
* [Selenium](https://selenium.dev/)
