## Apagador de mensagens do Discord

Este projeto permite a um usuário autenticado apagar suas mensagens em um servidor no Discord, utilizando a ferramenta Selenium (v4.17.2) para interação virtual programada com a versão web da aplicação em PT-BR.

Toda a execução é feita em função dos parâmetros em *settings.py*, arquivo que deve ser examinado pelo usuário. Assim é possível determinar, por exemplo, uma chave de busca que indica as mensagens a serem apagadas.

### Limitações

A busca pelas mensagens alvo da deleção tira proveito do sistema de busca do próprio Discord.

O programa tentará excluir mensagens em ordem, da mais antiga para a mais recente. No entanto, não é possível garantir isso, e uma ordem de exclusão aparentemente aleatória pode ocorrer.

Deve-se observar também que a exclusão de várias mensagens pode não se refletir instantaneamente em todos os clientes.

### Entrada de dados

Dados de entrada são lidos do arquivo *config/config.json*, estruturado de acordo com o *template* no mesmo diretório. Se o arquivo não existir, o *script* principal o criará.

#### Opções de entrada

Os campos em *global_options*, em arquivos de configuração, explicam-se assim:

- ***login_attempts***: Número máximo de vezes que o programa tentará fazer login.

- ***selection_attempts***: Número máximo de vezes que o programa tentará adentrar o servidor indicado.

- ***nil_tolerance***: Número máximo permitido de iterações que completam sem apagar nenhuma mensagem.

- ***target_count***: Número de mensagens a deletar.

#### Outras observações

- Informe datas no formato *aaaa-mm-dd*.
- É possível informar uma chave completa de busca no campo *"searchkey"*. Pode-se inclusive realizar uma busca no Discord e colar nesse campo o conteúdo da caixa de busca.
- Atribua *null* aos filtros que você não quiser utilizar.

### Créditos

* [Discord](https://discord.com)
* [Selenium](https://selenium.dev/)
