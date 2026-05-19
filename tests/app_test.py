ALLOWED_DIAGNOSTICS = {
    "saudavel",
    "falta_agua",
    "excesso_agua",
    "pouca_luz",
    "excesso_sol",
    "possivel_praga",
    "necessita_adubo"
}


def test_health_should_return_ok(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.get_json()

    assert data["status"] == "ok"
    assert "service" in data


def test_predict_should_return_valid_response_for_healthy_plant(client):
    payload = {
        "tipo_planta": "jiboia",
        "dias_sem_rega": 2,
        "frequencia_ideal_rega": 3,
        "umidade_solo": "normal",
        "luz_recebida": "media",
        "temperatura_media_c": 24,
        "folhas_amareladas": "nao",
        "folhas_murchas": "nao",
        "manchas_folhas": "nao",
        "crescimento_lento": "nao",
        "solo_compactado": "nao"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.get_json()

    assert data["diagnostico"] in ALLOWED_DIAGNOSTICS
    assert "nivel_risco" in data
    assert "recomendacao" in data


def test_predict_should_return_valid_response_for_lack_of_water_scenario(client):
    payload = {
        "tipo_planta": "jiboia",
        "dias_sem_rega": 8,
        "frequencia_ideal_rega": 3,
        "umidade_solo": "seca",
        "luz_recebida": "alta",
        "temperatura_media_c": 29,
        "folhas_amareladas": "nao",
        "folhas_murchas": "sim",
        "manchas_folhas": "nao",
        "crescimento_lento": "sim",
        "solo_compactado": "nao"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.get_json()

    assert data["diagnostico"] in ALLOWED_DIAGNOSTICS
    assert data["nivel_risco"] in {"baixo", "medio", "alto", "indefinido"}
    assert isinstance(data["recomendacao"], str)
    assert len(data["recomendacao"]) > 0


def test_predict_should_accept_unknown_plant_type(client):
    payload = {
        "tipo_planta": "planta_desconhecida",
        "dias_sem_rega": 5,
        "frequencia_ideal_rega": 3,
        "umidade_solo": "seca",
        "luz_recebida": "media",
        "temperatura_media_c": 26,
        "folhas_amareladas": "nao",
        "folhas_murchas": "sim",
        "manchas_folhas": "nao",
        "crescimento_lento": "sim",
        "solo_compactado": "nao"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.get_json()

    assert data["diagnostico"] in ALLOWED_DIAGNOSTICS
    assert "recomendacao" in data


def test_predict_without_json_should_return_bad_request(client):
    response = client.post("/predict")

    assert response.status_code == 400

    data = response.get_json()

    assert "error" in data

    
def test_predict_with_missing_fields_should_return_bad_request(client):
    payload = {
        "tipo_planta": "jiboia",
        "dias_sem_rega": 8,
        "frequencia_ideal_rega": 3,
        "umidade_solo": "seca"
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Missing required fields"
    assert "luz_recebida" in data["fields"]
    assert "temperatura_media_c" in data["fields"]
    assert "folhas_murchas" in data["fields"]