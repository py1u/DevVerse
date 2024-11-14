import pytest
from src import app as flask_app

# set PYTHONPATH=%cd%
# pytest

@pytest.fixture()
def client():
    flask_app.config.update({"TESTING": True})
    with flask_app.test_client() as client:
        yield client
        

# test a home root directory I created
# def test_root_directory(client):
#     response = client.get("/")
    
#     assert response.status_code == 200
#     assert b"Hello World!" in response.data
    
    
# test all possible jobs and their respective ids
@pytest.mark.parametrize("role,job_id,expected_response_data", 
                         [("softwareEngineer",0,{"job_id": 0, "title":"Software Engineer"}), 
                          ("backendEngineer",1,{"job_id": 1, "title":"Backend Engineer"})
                          ])

def test_get_any_role(client,role,job_id,expected_response_data):
    response = client.get(f"/api/engineering/{role}/{job_id}")
    
    assert response.status_code == 200
    
    data = response.get_json()
    
    assert data == expected_response_data
    
   
    
    