[🇧🇷 Versão em Português](#-versão-em-português)

## 1. Overview

A fleet of IoT-enabled printers distributed across multiple facilities sends operational telemetry containing metrics such as temperature and workload.

Episodes of anomalous behavior have been identified, including overheating and unexpected workload variations, impacting operations.

This document defines the requirements of the MVP for a near real-time anomaly detection system based on configurable per-printer thresholds, including event logging and notification to the operations team.

## 2. Project Scope

The MVP covers telemetry ingestion, anomaly detection based on per-printer thresholds, event counting, notification, and generation of a simple ranking based on anomaly frequency.

## 3. Assumptions and Constraints

The MVP must use the AWS services available in the project account, including AWS IoT Core, AWS Lambda, DynamoDB, and SNS.  
The MVP must process messages published by printers without requiring manually managed servers.

## 4. Functional Requirements

### FR-01 Telemetry Ingestion  
The system must receive and process telemetry messages sent by multiple printers via AWS IoT Core.

### FR-02 Device Identification  
Each processed message must unambiguously identify the source printer through a printer identifier.

### FR-03 Metric and Value  
Each processed message must contain a metric and an associated numeric value, enabling anomaly evaluation.

### FR-04 Per-Printer Profiles  
The system must maintain a per-printer configuration source containing acceptable reading thresholds and a sensitivity parameter for anomaly triggering.

### FR-05 Threshold Evaluation  
For each message, the system must compare the received value against the configured thresholds for the corresponding printer and determine whether the reading is within or outside the acceptable range.

### FR-06 Anomaly Confirmation by Recurrence  
The system must consider an anomaly confirmed only when consecutive violations reach or exceed the configured sensitivity parameter.

### FR-07 Anomaly Logging and Counting  
When an anomaly is confirmed, the system must log the event and update the total anomaly count associated with the printer.

### FR-08 Notification to the Operations Team  
When an anomaly is confirmed, the system must send a notification to the operations team via SNS.

### FR-09 Minimum Notification Content  
The notification must include the printer identifier and sufficient information to support initial action, including the metric and the observed value.

### FR-10 Frequency-Based Ranking  
The system must provide an ordered view of printers with the highest number of recorded anomalies in descending order, based on the data available in the MVP.

## 5. Non-Functional Requirements

### NFR-01 Detection Time  
The system must be capable of issuing a notification within 5 seconds after receiving the message that confirms the anomaly under normal operating conditions.

### NFR-02 Event-Driven Processing  
The system must process telemetry on demand, triggered by message arrival events, without manual execution.

### NFR-03 Reliable Counter Updates  
The anomaly count per printer must be updated consistently, preventing lost increments in scenarios where messages arrive close in time.

### NFR-04 Minimum Observability  
The system must record logs sufficient for auditing and troubleshooting, including device identifier, metric, value, in-range or out-of-range decision, and whether an anomaly was confirmed.

### NFR-05 Configuration Without Redeployment  
Per-printer threshold configurations must be modifiable without requiring redeployment of the processing code.

## 6. Security Requirements

### SR-01 Publication Control  
Only authorized devices or entities must be allowed to publish telemetry to the ingestion channel.

### SR-02 Least Privilege  
The processing component must operate with minimal permissions required to read configurations, update counters, publish notifications, and record logs.

### SR-03 Notification Protection  
The notification channel must be available only to authorized recipients.

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