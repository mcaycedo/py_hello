from flask import Flask, request, jsonify
app = Flask(__name__)
import sqlite3
from sqlite3 import Error

@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print(f"got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        conn = create_connection("data.db")
        nombre = ('Mario', 'Caycedo')
        insert_tabla(conn, (name, name))
       
        cur = conn.cursor()
        res = cur.execute("select count(*) cuenta from tabla")
        conn.commit()
        cuenta =  str(list(res)[0][0])
        response["MESSAGE"] = f"Welcome {name} to our awesome platform!!{cuenta}"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def insert_tabla(conn, name):
    sql = "INSERT INTO tabla(nombre,apellido, fecha) select ?,?, datetime('now')"
    #sql = "INSERT INTO tabla(nombre,apellido) select ?, ?"
    cur = conn.cursor()
    cur.execute(sql, name)
    conn.commit()
    return cur.lastrowid
    
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)