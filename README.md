# PlantCare Smart Diagnostics

API de Inteligência Artificial para diagnóstico inteligente de plantas no projeto PlantCare.

A API recebe dados informados pelo usuário, como umidade do solo, luminosidade, sintomas nas folhas e frequência de rega. Com base nesses dados, um modelo de Machine Learning classifica o possível estado da planta e retorna um diagnóstico, nível de risco e recomendação de cuidado.

## Objetivo

Integrar um componente de IA ao Oracle APEX, permitindo que o APEX envie dados da planta para a API e receba uma recomendação automática.

## Tecnologias

- Python
- Flask
- Pandas
- Scikit-learn
- Joblib
- Oracle APEX como consumidor da API

## Estrutura

```text
plantcare-smart-diagnostics/
├── ai-api/
│   ├── app.py
│   └── train-ai.ipynb
├── data/
│   └── plantcare_dataset_sintetico.csv
├── models/
│   └── plantcare_model.pkl
├── requirements.txt
└── README.md