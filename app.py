###test version
import sqlite3

from flask import Flask, render_template, url_for, request, send_from_directory, session, redirect
app = Flask(__name__)
app.secret_key = 'lolcatz'
app.threaded = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

## This is the first page you come to in the program, this displays the home page, which is the search. Within this "index.html" file these is
## a html element that give the user a text box to type in. That text is then carried over to @app.route(/profile) which the HTML file redirects the program
## to go to thus not having to make the python code do it.

@app.route('/')
def index():
	return render_template("index.html")

##This is where the magic happens... all the back-end magic happens here. The subroutine takes the text inputted from the user in the html page and feeds
## it into the database where it is checked if it is real then is moved into the /ret subroutine.

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

##

@app.route("/doedit")
def doedit():
	return render_template ("doedit.html")

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
	return redirect(url_for('editchanges'))

@app.route("/editchanges")
def editchanges():
	if session.get('db_data') != None:
		value = session.get('db_data')
		return render_template("editchanges.html", value_name = value)
	else:
		return'failed'


@app.route("/editedchange", methods=["POST", "GET"])
def editedchange():
	conn = sqlite3.connect("stock.db")
	c = conn.cursor()
	value = {}
	value['Name'] = request.form["editName"] 
	value['Id'] = request.form["editId"] 
	value['Price'] = request.form["editPrice"]
	c.execute("UPDATE * FROM data WHERE name=?;", (name,))
	return render_template("finaledited.html", value_name = value)



















if __name__ == '__main__':
	app.run(debug=True, port=5000)




