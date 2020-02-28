from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, escape, request, jsonify

app = Flask(__name__)

stud = []
classes = []

type_defs = load_schema_from_path('schema.graphql')

query = QueryType()
mutation = MutationType()

def getStudent(*_, id):
	if id < len(stud):
		return stud[id]
	return None

def getClass(*_, id):
	if id < len(classes):
		return classes[id]
	return None

def createStudent(*_, name):
	stud.append({"name":name})
	return stud[-1]

def createClass(*_, name):
	classes.append({"name":name, "students":[]})
	return {"name":classes[-1]["name"], "students":classes[-1]["students"]}

def addStudent(*_, sid, cid):
	classes[cid]["students"].append(stud[sid])
	return {"name":classes[cid]["name"], "students":classes[cid]["students"]}


query.set_field('get_student', getStudent)
query.set_field('get_class', getClass)
mutation.set_field('create_student', createStudent)
mutation.set_field('create_class', createClass)
mutation.set_field('add_student', addStudent)


schema = make_executable_schema(type_defs, query, mutation)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/graphql', methods=['GET'])
def playground():
    return PLAYGROUND_HTML, 200

@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
    schema,
    data,
    context_value=None,
    debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

