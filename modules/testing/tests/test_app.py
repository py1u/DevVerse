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
                         [("softwareEngineer",0,
                           {"Success": True, 
                            "Data" : {"job_id": 0, 
                                      "title":"Software Engineer",
                                      "description": "SWE at Artr",
                                      "available": True,
                                      "date": "2024-10-8"
                                      }
                            }), 
                          ("backendEngineer",1,
                           {"Success": True, 
                            "Data" : {"job_id": 1,
                                      "title":"Backend Engineer",
                                      "description": "Backend dev at Artr",
                                      "available": False,
                                      "date": "2024-10-2"}
                            })
                          ])

def test_get_any_role(client,role,job_id,expected_response_data):
    response = client.get(f"/api/engineering/{role}/{job_id}")
    
    assert response.status_code == 200
    
    data = response.get_json()
    
    assert data == expected_response_data
    

# update a existing job title, description, and availability 
@pytest.mark.parametrize("role, job_id, update_data, expected_update_data", 
                         [("softwareEngineer", 1, 
                           {"job_id": 1, 
                            "title": "Software Engineer, Core Infra",
                            "description": "core engineer",
                            "available": False,
                            "date": "2024-10-8"
                            },  
                           
                           {"Success": True, 
                            "Data":{"job_id": 1,
                                    "title": "Software Engineer, Core Infra", 
                                    "description": "core engineer", 
                                    "available": False, 
                                    "date": "2024-10-8"
                                    }
                                }
                           ), ])
def test_update_job(client, role, job_id, update_data, expected_update_data):
  response = client.put(f"/api/engineering/{role}/{job_id}", json=update_data)
  assert response.status_code == 200
  

  # send a GET request to check if the data was updated    
  response = client.get(f"/api/engineering/{role}/{job_id}")
  assert response.status_code == 200
  
  updated_data = response.get_json()
  assert updated_data == expected_update_data
  
  
# send a DELETE request to delete by role
@pytest.mark.parametrize("role, job_id", [("softwareEngineer",1),])
def test_delete_job(client, role, job_id):
  deleted_data = client.delete(f"/api/engineering/{role}/{job_id}")  
  response = client.get(f"/api/engineering/{role}/{job_id}")
  assert response.status_code == 404
  
  
    