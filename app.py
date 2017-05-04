###test version
import sqlite3

from flask import Flask, render_template, url_for, request, send_from_directory, session, redirect
app = Flask(__name__)
app.secret_key = 'lolcatz'
app.threaded = True
app.config["TEMPLATES_AUTO_RELOAD"] = True



@app.route('/')
def index():
	return render_template("index.html")

# @app.route('/<path:path>')
# def static_file(path):
# 	return app.send_static_file(path)

@app.route("/profile", methods=["POST"])
def profile():
	if request.method == 'POST':
		name = request.form["username"]
		conn = sqlite3.connect("stock.db")
		c = conn.cursor()
		c.execute("SELECT * FROM data WHERE name=?;", (name,))
		rows = [c.fetchone()]
		data = [{c.description[idx][0]:rows[row][idx] for idx in range(len(rows[row]))} for row in range(len(rows))]
		session["db_data"] = data[0]
		conn.close()

	return redirect(url_for('ret'))

@app.route('/ret')
def ret():
	
	if session.get('db_data') != None:
		value = session.get('db_data')
		return render_template("return.html", value_name = value)

	else:
		return''

## id is capitalized ##
@app.route('/new', methods=["POST", "GET"]) 
def new():
	if request.method == 'POST':
		#setting returned input into values.
		conn = sqlite3.connect("stock.db")
		c = conn.cursor()
		c.execute("SELECT * FROM data WHERE id={};".format(request.form["id"]))
		if len(c.fetchall()) > 0:

			return 'value exists'
			conn.commit()
			conn.close()
			# c.close()
		else:
			ID = request.form["id"]
			name = request.form["name"]
			price = request.form["price"]
			##connecting to the Database
			c.execute("INSERT INTO data ('id','name','price') VALUES(?,?,?)",
	    		(ID, name, price))
			conn.commit()
			conn.close()
			




		return render_template("new.html")
	return render_template("new.html")

## This is the backend code for editing/removing values in the database.
##vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

# @app.route('/edit', method=["POST"])
# def edit():
# 	if request.method == 'POST':
# 		name = request.form["item"]
@app.route("/doedit")
def doedit():
	return render_template ("edit.html")

@app.route("/edit", methods=["POST", "GET"])
def edit():
	if request.method == 'POST':
		name = request.form["item"]
		conn = sqlite3.connect("stock.db")
		c = conn.cursor()
		c.execute("SELECT * FROM data WHERE name=?;", (name,))
		rows = [c.fetchone()]
		data = [{c.description[idx][0]:rows[row][idx] for idx in range(len(rows[row]))} for row in range(len(rows))]
		session["db_data"] = data[0]
		
		conn.close()
	return redirect(url_for('editret'))

@app.route("/editret")
def editret():
	
	if session.get('db_data') != None:
		value = session.get('db_data')
		return render_template("editret.html", value_name = value)

	else:
		return'failed'

















if __name__ == '__main__':
	app.run(debug=True, port=5000)




