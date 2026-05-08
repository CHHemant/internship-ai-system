def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_parse_job_endpoint(client):
    response = client.post("/api/job/parse", json={"job_description": "Required Python and NLP"})
    assert response.status_code == 200
    payload = response.json()
    assert "keywords" in payload


def test_recommendations_endpoint(client):
    payload = {
        "profile": {
            "skills": ["Python", "NLP"],
            "research_interests": ["LLM"],
            "projects": [],
            "education": [],
            "certifications": [],
            "experience": [],
            "raw_text": ""
        },
        "internships": [
            {"title": "NLP RA", "description": "Work on Python NLP models", "keywords": ["python", "nlp"], "lab": "AI Lab"}
        ]
    }
    response = client.post("/api/recommendations", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert len(body["ranked_internships"]) == 1
    assert body["suggested_professors_or_labs"] == ["AI Lab"]
