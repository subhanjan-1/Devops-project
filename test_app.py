from app import app

def test_home_page():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_prediction():
    client = app.test_client()
    
    response = client.post('/', data={
        'age': 22,
        'cgpa': 8.5,
        'backlogs': 0,
        'communication': 7,
        'coding': 8
    })
    
    assert response.status_code == 200