from flask import Flask,redirect,request,jsonify,render_template
from neo4j import GraphDatabase
from decouple import config


username=config('NEO4J_USERNAME')
pwd=config('NEO4J_PASSWORD')
uri=config('NEO4J_URI')


# database connections
driver=GraphDatabase.driver(uri=uri,auth=(username,pwd))
session=driver.session()
app = Flask(__name__)

# routes


# Create new user
@app.route("/create_one/<string:name>&<int:id>",methods=["POST","GET"])
def create_one(name,id):
    q1="""
    create (n:Employee{NAME:$name, ID:$id})
    """
    map={"name":name,"id":id}
    try:
        session.run(q1,map)
        return (f"Employee node create with employee name={name} and employee id={id}")
    except Exception as e:
        return (str(e))

# Get all users
@app.route("/display_all",methods=["GET","POST"])
def display_all():
    q1="""
    match (n) return n.NAME as NAME, n.ID as ID
    """
    result=session.run(q1)
    data = result.data()
    return (jsonify(data))

# Get a single user
@app.route("/display_one/<int:id>",methods=["GET","POST"])
def display_one(id):
    q1="""
        match(n) WHERE n.ID =$id return n.ID as ID, n.NAME as NAME
    """
    map={"id":id}
    result=session.run(q1,map)
    data = result.data()
    return (jsonify(data))




if __name__=="__main__":
    app.run(port=5050)