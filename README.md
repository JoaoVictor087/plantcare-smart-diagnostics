# PlantCare Smart Diagnostics

## 1. Descrição da Solução
O PlantCare é um sistema inteligente de monitoramento de plantas que utiliza sensores IoT para coletar dados em tempo real. A solução processa esses dados através de um modelo de Inteligência Artificial para diagnosticar a saúde da planta, permitindo intervenções preventivas. O sistema é composto por um microsserviço Java, um modelo de IA em Python e integração analítica com Oracle APEX.

## 2. Explicação do Modelo de IA
* **Modelo Utilizado:** LogisticRegression
* **Justificativa:** Escolhemos este modelo devido à sua alta eficiência em classificação de dados tabulares (umidade, temperatura, luz) e baixo tempo de inferência, ideal para integrações em tempo real.
* **Treinamento:** O modelo foi treinado com um dataset contendo aproxidamente 300 amostras de estados de saúde de plantas (seco, ideal, encharcado), garantindo precisão nas predições de estresse hídrico e térmico.

## 3. Fluxo de Integração (Diagrama de Arquitetura)
O fluxo de dados ocorre da seguinte forma:
1. **Coleta:** Sensores enviam dados via HTTP para nossa API Java.
2. **Diagnóstico:** A API Spring Boot encaminha os dados para o microsserviço de IA na Azure (`/predict`).
3. **Persistência:** O resultado é salvo no **Oracle Database** (Tabela `T_PC_DIAGNOSTICOS_IA`).
4. **Analytics:** O **Oracle APEX** processa esse histórico via ORDS, gerando métricas de saúde (Saudômetro) consumidas pelo aplicativo Mobile.


## 4. Instruções de Uso

### Pré-requisitos
* Python 3.14
* Flask
* scikit-learn
*joblib
*flask
*pytest
* Acesso ao Oracle Autonomous Database (Wallet configurada)
* Variáveis de ambiente configuradas no arquivo `.env`

### Configuração
1. Clone o repositório: `git clone https://github.com/JoaoVictor087/plantcare-smart-diagnostics`
2. Configure o arquivo `.env` na raiz do projeto:
   ```env
   DB_URL=jdbc:oracle:thin:@...
   DB_USERNAME=ADMIN
   DB_PASSWORD=...
   AI_API_URL=https://<url-da-sua-ia-python>.azurewebsites.net
