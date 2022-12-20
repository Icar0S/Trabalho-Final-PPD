# Trabalho-Final-PPD
Trabalho Final de Programação Paralela e Distribuida utilizando RCP/RMI + MOM + TuplaSpace

# Projeto Final

Objetivo: Implementar um sistema de comunicação baseado em localização. As
funcionalidades básicas a serem incluídas são as seguintes:

1. Deve haver comunicação síncrona entre usuários ONLINE que deve ocorrer
através de sockets ou RPC/RMI.
2. Deve haver comunicação assíncrona entre usuários OFFLINE que deve ocorrer
através de uma fila de mensagens gerenciada por um MOM (Middleware
Orientado à Mensagens) compartilhado entre os usuários.
3. As mensagens assíncronas enviadas para um usuário só devem ser mostradas
quando este estiver ONLINE.
4. Deve haver uma lista de contatos para cada usuário. Esses contatos devem ser
atualizados dinamicamente através de informações retiradas de um espaço de
tuplas compartilhado.
5. As informações sobre usuários (nome e apelido), localização (latitude e
longitude) e status (online ou offline) devem ser armazenados em tuplas em um
espaço de tuplas compartilhado.
6. Deve ser possível indicar um raio de distância para a realização de
comunicações com contatos.
7. Novos contatos devem ser atualizados sempre que entrarem no raio de
comunicação do usuário.
8. Deve ser possível atualizar a localização, o status de usuários e o raio de
distância de comunicação.
9. Só pode haver comunicação síncrona para contatos que estejam ONLINE e
dentro do raio de distância indicado.
10.A comunicação assíncrona deve acontecer para contatos OFFLINE ou que
estejam fora do raio de comunicação.

Critérios de Avaliação:
1. UI (0-10).
2. Definição de operações (RMI/RPC) ou protocolo (sockets) (0-10).
3. Modelagem de tuplas (0-10).
4. Implementação de Funcionalidades (0-10).
