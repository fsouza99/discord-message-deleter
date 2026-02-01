## Apagador de mensagens do Discord

Este projeto permite a um usuário autenticado apagar suas mensagens em um servidor no Discord, utilizando a ferramenta Selenium (v4.17.2) para interação virtual programada com a versão web da aplicação em PT-BR.

### Entrada de dados

Dados de entrada são lidos do arquivo *config/config.json*, estruturado de acordo com o *template* no mesmo diretório. Se o arquivo não existir, o *script* principal o criará.

#### Opções de entrada

Os campos em *run*, em arquivos de configuração, explicam-se assim:

- ***login_attempts***: Número máximo de vezes que o programa tentará fazer login.

- ***selection_attempts***: Número máximo de vezes que o programa tentará adentrar o servidor indicado.

- ***nil_tolerance***: Número máximo permitido de iterações que completam sem apagar nenhuma mensagem.

- ***target_count***: Número de mensagens a deletar.

#### Outras observações

- Informe datas no formato *aaaa-mm-dd*.
- É possível informar uma chave completa de busca no campo *searchkey*.
    - Pode-se inclusive realizar uma busca no Discord e colar nesse campo o conteúdo da caixa de busca.
- Atribua *null* aos filtros que você não quiser utilizar.

### Limitações

A busca pelas mensagens alvo da deleção tira proveito do sistema de busca do próprio Discord, estando sujeita às suas limitações, e.g.:

- Uma exclusão de mensagem pode não se refletir instantaneamente em todos os clientes.
- Uma mensagem pode não aparecer em resultados de buscas imediatamente após ser enviada, mas somente após algum tempo de espera.
- A contagem de mensagens no painel de resultados pode também não refletir mudanças recentes, incluindo exclusões.

O programa tentará excluir mensagens em ordem, da mais antiga para a mais recente, mas não é possível garantir isso, e uma ordem de exclusão aparentemente aleatória pode ocorrer. É possível ainda que mensagens sejam puladas devido à rapidez da interação, o que é mitigado pelo uso da função de *sleep* do Python.

Mudanças no DOM do Discord podem defasar o código.

### Créditos

* [Discord](https://discord.com)
* [Selenium](https://selenium.dev/)
