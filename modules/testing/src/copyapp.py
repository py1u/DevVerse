from flask import Flask, request, jsonify
import json

app = Flask(__name__)

jobs_update = {
  "softwareEngineer":{
   'job_id': 0,
   'title': "Software Engineer",
   'desc': "SWE at Artr",
   'available': True, 
   'date': "2024-10-8"
  },
  "backendEngineer":{
   'job_id': 1,
   'title': "Backend Engineer",
   'desc': "Backend dev at Artr",
   'available': False, 
   'date': "2024-10-2"
  },
  "frontendEngineer": {
    'job_id': 2,
    'title': "Frontend Engineer",
    'desc': "Frontend dev at Artr",
    'available': False,
    'date': "2024-10-9"
  },
  "qaEngineer": {
    'job_id': 3,
    'title': "QA Engineer",
    'desc': "QA dev at Artr",
    'available': False,
    'date': "2024-11-2"
  },
  "softwareEngineerIntern": {
    'job_id': 4,
    'title': "Software Engineer Intern",
    'desc': "Software engineer intern at Artr",
    'available': False,
    'date': "2024-11-8"
  }
}

applications_db = {}
application_id = 0

#added helper functions
def client_success_res(data):
  return json.dumps({"Success": True, "Data" : data}),200

def client_failure_res(message):
  return json.dumps({"Success": False, "Error": message}),404

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/api/engineering/<string:role>/<int:job_id>", methods=["GET", "PUT", "DELETE"])
def handle_job_description(role, job_id):
  if role not in jobs_update:
    return client_failure_res("Job not found!")
    
  if request.method == "GET":
    data = {
      "job_id": job_id,
      "title": jobs_update[role].get("title")
    }
    return client_success_res(data)
  
  elif request.method == "PUT":
    data = request.get_json()
    if not data:
      return client_failure_res("Job not found!")
    
    updated_data = {
      "title": data.get("title", jobs_update[role].get("title")),
      "desc": data.get("desc", jobs_update[role].get("desc")),
    }
    
    jobs_update[role] = updated_data
    
    return client_success_res(updated_data)
  elif request.method == "DELETE":
    job = jobs_update[role]
    
    if not job:
      return client_failure_res("Job not found!")
    del jobs_update[role]
    return client_success_res(job)
  
@app.route("/api/<string:role>/apply")
def get_application(role):
  if role not in jobs_update:
    return client_failure_res("Job not found!")
  
  data = {
    "job_id": jobs_update[role].get("job_id"),
    "title": jobs_update[role].get("title"),
    "desc": jobs_update[role].get("desc"),
    "available": jobs_update[role].get("available"),
    "date": jobs_update[role].get("date")
  }
  
  return client_success_res(data)

@app.route("/api/<string:role>/apply", methods=["POST"])
def post_application(role):
  global application_id
  data = request.json
  
  name = data.get("name")
  email = data.get("email")
  phone = data.get("phone")
  education = data.get("education")
  major = data.get("major")
  
  if not name:
    return client_failure_res("Missing name field!")
  
  if not email:
    return client_failure_res("Missing email field!")
  
  if not phone:
    return client_failure_res("Missing phone field!")
  
  if not education:
    return client_failure_res("Missing education field!")
  
  if not major:
    return client_failure_res("Missing major field!")
  
  applications_db[application_id] = {
    "application_id": application_id,
    "role": role,
    "name": name,
    "email": email,
    "phone": phone,
    "education": education,
    "major": major
  }
  
  response = {
    "message": "Application received!",
    "applicant": applications_db[application_id]
  }
  
  application_id += 1

  return client_success_res(response)

@app.route("/api/<string:role>/apply/<int:application_id>", methods=["PUT"])
def update_application(role, application_id):
  data = request.json
  
  application = applications_db.get(application_id)
  
  if not application:
    return client_failure_res("Application not found!")
  
  name = data.get("name")
  email = data.get("email")
  phone = data.get("phone")
  education = data.get("education")
  major = data.get("major")
  
  if not any([name, email, phone, education, major]):
    return client_failure_res("No field provided for update!")
  
  if name: 
    application["name"] = name
  
  if email:
    application["email"] = email
    
  if phone:
    application["phone"] = phone
    
  if education:
    application["education"] = education
    
  if major:
    application["major"] = major
    
  applications_db[application_id] = application
  
  response = {
    "message": "Application updated!",
    "application_id": application_id,
    "role": role,
    "applicant": application
  }
  
  return client_success_res(response)

@app.route("/api/<string:role>/success/<int:application_id>")
def confirm(role, application_id):
  application = applications_db.get(application_id)
  
  if not application:
    return client_failure_res("Application not found!")
  
  response = {
    "message": f"Application for {role} has been successfully submitted!",
  }
  
  return client_success_res(response)

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8000, debug=True)    