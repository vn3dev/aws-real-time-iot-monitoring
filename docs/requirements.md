
---

[🇧🇷 Versão em Português](#-versão-em-português)

## 1. Visão Geral

Uma frota de impressoras IoT distribuídas em múltiplas instalações enviam telemetria operacional contendo métricas como temperatura e carga de trabalho.

Foram identificados episódios de comportamento anômalo, como superaquecimento e variações inesperadas de carga, impactando a operação.

Este documento define os requisitos do MVP de um sistema de detecção de anomalias em tempo quase real, com base em limites configuráveis por impressora, incluindo registro de eventos e notificação ao time de operações.

## 2. Escopo do projeto

O MVP cobre ingestão de telemetria, detecção de anomalia baseada em limites por impressora, contagem de eventos, notificação e geração de um ranking simples por frequência de anomalias.

## 3. Premissas e restrições

O MVP deve usar os serviços AWS disponíveis no ambiente de conta do projeto, incluindo AWS IoT Core, AWS Lambda, DynamoDB e SNS.
O MVP deve processar mensagens publicadas pelas impressoras sem necessidade de servidores gerenciados manualmente.

## 4. Requisitos Funcionais

### RF-01 Ingestão de telemetria
O sistema deve receber e processar mensagens de telemetria enviadas por múltiplas impressoras via AWS IoT Core.

### RF-02 Identificação do dispositivo
Cada mensagem processada deve identificar de forma inequívoca a impressora de origem, por meio de um identificador de impressora.

### RF-03 Métrica e valor
Cada mensagem processada deve conter uma métrica e um valor numérico associado, permitindo avaliação de comportamento anômalo.

### RF-04 Perfis por impressora
O sistema deve manter uma fonte de configuração por impressora contendo limites aceitáveis para as leituras e um parâmetro de sensibilidade para disparo de anomalia.

### RF-05 Avaliação de limites
Para cada mensagem, o sistema deve comparar a leitura recebida com os limites configurados para a impressora correspondente e determinar se a leitura está dentro ou fora da faixa aceitável.

### RF-06 Confirmação de anomalia por recorrência
O sistema deve considerar uma anomalia confirmada apenas quando ocorrerem violações consecutivas em quantidade igual ou superior ao parâmetro de sensibilidade configurado para a impressora.

### RF-07 Registro e contagem de anomalias
Quando uma anomalia for confirmada, o sistema deve registrar o evento e atualizar a contagem total de anomalias associada à impressora.

### RF-08 Notificação ao time de operações
Quando uma anomalia for confirmada, o sistema deve enviar uma notificação ao time de operações por meio de SNS.

### RF-09 Conteúdo mínimo da notificação
A notificação deve incluir o identificador da impressora e informação suficiente para orientar uma ação inicial, incluindo a métrica e o valor observado.

### RF-10 Ranking por frequência
O sistema deve disponibilizar uma visão ordenada das impressoras com maior número de anomalias registradas, em ordem decrescente, baseada nos dados disponíveis no MVP.

## 5. Requisitos Não Funcionais

### RNF-01 Tempo de detecção
O sistema deve ser capaz de emitir notificação em até 5 segundos após a chegada da mensagem que confirma a anomalia, em condições normais de operação.

### RNF-02 Processamento orientado a eventos
O sistema deve processar telemetria sob demanda, acionado por eventos de chegada de mensagens, sem depender de execução manual.

### RNF-03 Confiabilidade de atualização de contadores
A contagem de anomalias por impressora deve ser atualizada de forma consistente, evitando perda de incrementos em cenários de mensagens próximas no tempo.

### RNF-04 Observabilidade mínima
O sistema deve registrar logs suficientes para auditoria e troubleshooting, incluindo identificador do dispositivo, métrica, valor, decisão de dentro ou fora do limite e ocorrência ou não de anomalia confirmada.

### RNF-05 Evolução sem reimplantação completa
A configuração de limites por impressora deve poder ser alterada sem necessidade de redeploy de código do processamento.

## 6. Requisitos de Segurança

### RS-01 Controle de publicação
Somente dispositivos ou entidades autorizadas devem poder publicar telemetria para o canal de ingestão utilizado.

### RS-02 Privilégio mínimo
O componente de processamento deve operar com permissões mínimas para ler configurações, atualizar contadores, publicar notificações e registrar logs.

### RS-03 Proteção de notificações
O canal de notificação deve estar disponível apenas para destinatários autorizados.