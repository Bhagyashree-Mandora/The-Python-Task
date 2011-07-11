from flask import Flask , redirect , url_for, request
from pymongo.connection import Connection

app = Flask(__name__)
#Show Page
@app.route("/")
def show():
	t=open("static/task.html","w")
	part1=open("static/part1.html","r")
	part2=open("static/part2.html","r")
	part3=open("static/part3.html","r")

	f1=part1.readlines()
	for i in f1:
		t.write(i)	
	f2=part2.readlines()
#First Dynamic Part
	connection = Connection("localhost") 
	db = connection.task 
	i=1
	for d in db.task.find({"status": "Not Done"}):
		t.write("<tr><form action=\"../update/task.html\" method=\"POST\">    <td scope=\"col\">")
		#automated number here
		t.write(`i`)
		i=i+1
		t.write("</td>	<input name=\"TaskId\" type=\"hidden\" value=\"")
		t.write(`d["task_id"]`)
  		t.write("\"><td scope=\"col\">")
		t.write(d["task_name"])
		t.write("</th><td scope=\"col\"><input type=\"submit\" value=\"Done\"></td></form>  </tr> ")
#End of First Dynamic Part

	for i in f2:
		t.write(i)	
	f3=part3.readlines()

#Second Dynamic Part
	i=1
	for d in db.task.find({"status": "Done"}):
		t.write("<tr>   <td scope=\"col\">")
		#automated number here
		t.write(`i`)
		i=i+1
		t.write("</td>    <td scope=\"col\">")
		t.write(d["task_name"])
		t.write("</td></tr>")
#End of Second Dynamic Part

	for i in f3:
		t.write(i)	
	
	t.close()
	part1.close()
	part2.close()
	part3.close()
	return redirect(url_for("static",filename="task.html"))
	
@app.route("/update/task.html",methods=['POST'])
def update():
	#print "I came in Update"
	#if request.method == 'POST':
	tobedone=request.form['TaskId']
	#print "to be done is " + tobedone
	connection=Connection("127.0.0.1")
	db=connection.task
	for d in db.task.find({"task_id": int(tobedone)}):
		#print d
		db.task.update({"task_id": int(tobedone) }, {"$set":{"status":"Done"}})
	#	print "update sucessfull"
	return redirect("")	

@app.route("/insert/task.html",methods=['POST'])
def insert():
	toadd=request.form['newtask']
	if toadd=="":
#		print "User tried to insert blank task"
		return redirect("")	
	#print "to be added is " + toadd
	connection=Connection("127.0.0.1")
	db=connection.task	
	ls=[]
	for d in db.task.find():
		ls.append(d["task_id"])
	newid=int(max(ls))+1
	db.task.save({"user_id":001, "task_id":newid, "task_name":toadd, "status":"Not Done", "description":"", "priority":1})
	return redirect("")	

if __name__ == "__main__":
	app.debug = True
	app.run()

