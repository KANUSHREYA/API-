from flask import Flask,request, render_template,flash
import mysql.connector
from flask import jsonify

app = Flask(__name__)

mydb=mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="company"
)
@app.route('/create', methods=['POST'])
def create_emp():
    try:
      input_data = request.get_json()
      employee_id = input_data.get('employee_id')
      first_name = input_data.get('first_name','')
      last_name = input_data.get('last_name', '')
      phone_no = input_data.get('phone_no','')
      email=input_data.get('email')
      department = input_data.get('department', '')
      place = input_data.get('place', '')
      gender = input_data.get('gender', '')
      print(input_data)
      
      if not employee_id:
        return "Employee id is required", 400
      elif not first_name:
        return "First name is required", 400
      elif not last_name:
        return "last name is required",400
      elif not phone_no:
        return "phone no. is required",400
      elif not email:
        return "email is required",400
      elif not department:
        return "department is required",400
      elif not place:
        return "place is required",400
      elif not gender:
        return "gender is required", 400      
      else:
        print('every id is inserted')
        mycursor = mydb.cursor()   
        sql= "INSERT INTO employee (employee_id, first_name, last_name,phone_no,email,department,place,gender) VALUES(%s, %s, %s, %s,%s,%s,%s,%s)"
        val = (employee_id,first_name,last_name,phone_no,email,department,place,gender)           
        mycursor.execute(sql,val)        
        mydb.commit()
      response = jsonify('Employee added successfully!')
      response.status_code = 200
      return response
    except Exception as err:                 
        print(str(err))
        return "There is a error -"+str(err), 500

@app.route('/employees')
def view():
   try:  
    total=2
    page=request.args.get('page',1)
    skip=(int(page)-1) * total
    mycursor=mydb.cursor(dictionary=True)
    mycursor.execute("SELECT * FROM employee LIMIT %s, %s", (skip, total))
    print(mycursor.rowcount)
    myresult = mycursor.fetchall()
    print(myresult)
    return myresult, 200
   except Exception as err:
    print (str(err))
    return "There is a error - "+ str(err)

@app.route('/emp/<int:id>')
def employee(id):
  try:
    mycursor = mydb.cursor(dictionary=True)
    sql="SELECT employee_id,first_name,last_name,phone_no,email,department,place,gender FROM employee WHERE id=%s"
    mycursor.execute(sql, (id,))
    myresult=mycursor.fetchone()

    if mycursor.rowcount == 0:
      return "Employee not found", 400

    return jsonify(myresult), 200
  except Exception as err:
    print(str(err))
    return "error"

@app.route('/del/<int:id>',methods=['DELETE'])  
def employee1(id):
  try:
    mycursor=mydb.cursor(dictionary=True)
    sql="SELECT employee_id FROM employee WHERE id=%s"
    mycursor.execute(sql, (id,))
    myresult=mycursor.fetchone()

    if mycursor.rowcount == 1:
       mycursor=mydb.cursor()
       sql="DELETE FROM employee WHERE id=%s"
       mycursor.execute(sql,(id,))
       mydb.commit()
       print(myresult)
       return "Entry deleted successfully",200
    else:
       return"Employee not found",400
  except Exception as err:
      print(str(err))
      return "there is a error"

@app.route('/update/<eid>',methods=['POST','GET'])
def employee2(eid):
  try:
    output_data = request.get_json()
    employee_id=output_data.get('employee_id')
    first_name=output_data.get('first_name')
    last_name=output_data.get('last_name')
    email=output_data.get('email')
   
    mycursor=mydb.cursor()
    mycursor.execute("SELECT * FROM employee WHERE id != %s AND (employee_id=%s OR email=%s) ",(eid,employee_id,email))
    print(mycursor.statement)
    count=mycursor.fetchone()
    if count:
        return "employee_id or phone_no already exists."

    if employee_id and first_name and last_name and request.method == 'POST': 
      sql="UPDATE employee SET employee_id=%s,first_name=%s,last_name=%s,email=%s WHERE id=%s"
      val=(employee_id,first_name,last_name,email,eid)
      mycursor=mydb.cursor()
      mycursor.execute(sql,val)
      mydb.commit()
      print (mycursor.rowcount,"record(s) affected")
    else:
      return "Invalid input", 400
    if(mycursor.rowcount >= 1):
     return 'Updated successfully',200
    else:
       return 'Not updated, please try again',400
  except Exception as err:
    print(str(err))
    return "the entry is not updated",400

@app.route('/joins',methods=['GET'])
def joins():
  try:
      mycursor=mydb.cursor(dictionary=True)
      sql= "SELECT s.eid, s.id , e.first_name, s.salaries FROM salary s INNER JOIN employee e ON s.id = e.id" 
      mycursor.execute(sql)
      myresult = mycursor.fetchall()

      print(myresult)
      return jsonify(myresult), 200
  except Exception as err:
      print(str(err))
      return "there is a error"

if __name__ == "__main__":
    app.run()
