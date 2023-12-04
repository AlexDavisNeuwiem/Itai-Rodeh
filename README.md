# Itai-Rodeh

Implementação do algoritmo de Itai-Rodeh para a eleição de líderes em sistemas distribuídos

## Links Úteis

Link para acessar o vídeo de apresentação
```
https://youtu.be/OrdNBnl70BA
```

## Sobre o programa

### Configuração

As configurações padrão dos nodos funcionam localmente. Porém, é possível alterá-las para rodar em computadores
diferentes em rede. A configuração é realiza por meio das variáveis definidas antes da definição das classes em 
`init_node.py` e `application_node.py`.

Node e InitNode podem confirgurar seu ip e porta. Além disso, o InitNode pode configurar a quantidade
de nodes e número de ids. Por fim, o Node pode definir endereço e porta do init node que tentará se conectar.

### Execução

Para executar o InitNode, basta rodar o comando:

```shell
python3 init_node.py
```

Criar N terminais e rodar em cada um o comando:
```shell
python3 application_node.py
```
