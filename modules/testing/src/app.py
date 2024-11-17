from flask import Flask, request, jsonify
import json

app = Flask(__name__)

job_db = {
  "softwareEngineer":{
   'job_id': 0,
   'title': "Software Engineer",
   'description': "SWE at Artr",
   'available': True, 
   'date': "2024-10-8"
  },
  "backendEngineer":{
   'job_id': 1,
   'title': "Backend Engineer",
   'description': "Backend dev at Artr",
   'available': False, 
   'date': "2024-10-2"
  },
  "frontendEngineer": {
    'job_id': 2,
    'title': "Frontend Engineer",
    'description': "Frontend dev at Artr",
    'available': False,
    'date': "2024-10-9"
  },
  "qaEngineer": {
    'job_id': 3,
    'title': "QA Engineer",
    'description': "QA dev at Artr",
    'available': False,
    'date': "2024-11-2"
  },
  "softwareEngineerIntern": {
    'job_id': 4,
    'title': "Software Engineer Intern",
    'description': "Software engineer intern at Artr",
    'available': False,
    'date': "2024-11-8"
  }
}

applications_db = {}
application_id = len(job_db)

#added helper functions
def client_success_res(data):
  return jsonify({"Success": True, "Data" : data}),200

def client_failure_res(message):
  return jsonify({"Success": False, "Error": message}),404

def valid_form_apply(payload):
  
  name = payload.get("name")
  email = payload.get("email")
  phone = payload.get("phone")
  education = payload.get("education")
  major = payload.get("major")
  
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
  
  return payload
  

@app.route("/")
def hello():
  return "Hello World!"

@app.route("/api/engineering/<string:role>/<int:job_id>", methods=["GET", "PUT", "DELETE"])
def handle_job_description(role, job_id):
  if role not in job_db:
    return client_failure_res("Job not found!")
  
  if request.method == "GET":
    
    position = job_db[role]
    data = {"job_id": job_id,
            "title": position.get("title"), 
            "description": position.get("description"), 
            "available": position.get("available"), 
            "date": position.get("date")
            }

    return client_success_res(data)
  
  elif request.method == "PUT":
    
    body = json.loads(request.data)
    position = job_db.get(role)
    if not position:
      return client_failure_res("Job not found!")
    
    position["job_id"] = position.get("job_id")
    position["title"] = body.get("title")
    position["description"] =  body.get("description")
    position["available"] = body.get("available")
    position["date"] = position.get("date")
              
    return client_success_res(position)
  
  elif request.method == "DELETE":
    job = job_db[role]
    
    if not job:
      return client_failure_res("Job not found!")
    
    del job_db[role]
    return client_success_res(job)
  
@app.route("/api/<string:role>/apply")
def get_application(role):
  if role not in job_db:
    return client_failure_res("Job not found!")
  
  position = job_db[role]
  print(f"retrieve {positon}")
  
  data = {
    "job_id": position.get("job_id"),
    "title": position.get("title"),
    "desc": position.get("desc"),
    "available": position.get("available"),
    "date": position.get("date")
  }
  
  return client_success_res(data)

@app.route("/api/<string:role>/apply", methods=["POST"])
def post_application(role):
  global application_id
  
  body = json.loads(request.data)
  return_payload = validate_form_apply(body)
  
  applications_db[application_id] = {
    "application_id": application_id,
    "role": return_payload[role],
    "name": return_payload[name],
    "email": return_payload[email],
    "phone": return_payload[phone],
    "education": return_payload[education],
    "major": return_payload[major]
  }
  
  data = applications_db[application_id]
  application_id += 1

  return client_success_res(data)

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
    
