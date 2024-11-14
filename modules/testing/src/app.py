from flask import Flask, request, jsonify
import json

app = Flask(__name__)

jobs = {
  "softwareEngineer": "Software Engineer",
  "backendEngineer": "Backend Engineer",
  "frontendEngineer": "Frontend Engineer",
  "qaEngineer": "QA Engineer",
  "softwareEngineerIntern": "Software Engineer Intern"
}


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
    return jsonify({"job_id": job_id,
                       "title": jobs_update[role].get("title"), 
                       "description": jobs_update[role].get("desc"), 
                       "available": jobs_update[role].get("available"), 
                       "date": jobs_update[role].get("date")
                       }), 200
  
  elif request.method == "PUT":
    data = request.get_json()
    if not data:
      return json.dumps({"success": False, "error": "No data"}), 404
    
    updated_data = {
      "title": data.get("title", jobs[role]),
      "description": data.get("description", "")
    }
    
    return json.dumps({"success": True, "data": {"id": id, "role": role, "updated_data": updated_data}}), 200
  elif request.method == "DELETE":
    job = jobs.get(role, None)
    
    if not job:
      return json.dumps({"success": False, "error": "Job not found!"}), 404
    del jobs[role]
    return json.dumps({"success": True, "data": job}), 200
  
@app.route("/api/<string:role>/apply")
def get_application(role):
  return "Application"

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
    return json.dumps({"success": False, "error": "Missing name"}), 400
  
  if not email:
    return json.dumps({"success": False, "error": "Missing email"}), 400
  
  if not phone:
    return json.dumps({"success": False, "error": "Missing phone"}), 400
  
  if not education:
    return json.dumps({"success": False, "error": "Missing education"}), 400
  
  if not major:
    return json.dumps({"success": False, "error": "Missing major"}), 400
  
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
    "role": role,
    "applicant": applications_db[application_id]
  }
  
  application_id += 1
  
  return json.dumps({"success": True, "data": response}), 200

@app.route("/api/<string:role>/apply/<int:application_id>", methods=["PUT"])
def update_application(role, application_id):
  data = request.json
  
  application = applications_db.get(application_id)
  
  if not application:
    return json.dumps({"success": False, "error": "Application not found!"}), 400
  
  name = data.get("name")
  email = data.get("email")
  phone = data.get("phone")
  education = data.get("education")
  major = data.get("major")
  
  if not any([name, email, phone, education, major]):
    return json.dumps({"success": False, "error": "No field provided for update!"}), 400
  
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
  
  return json.dumps({"success": True, "data": response}), 200

@app.route("/api/<string:role>/success/<int:application_id>")
def confirm(role, application_id):
  application = applications_db.get(application_id)
  
  if not application:
    return json.dumps({"success": False, "error": "Application not found!"}), 404
  
  response = {
    "message": f"Application for {role} has been successfully submitted!",
  }
  
  return json.dumps({"success": True, "data": response}), 200

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8000, debug=True)
