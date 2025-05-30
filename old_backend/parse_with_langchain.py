
from flask import Flask, request, jsonify
from flask_cors import CORS
from notes_parser import parse_notes_into_jira_tasks

app = Flask(__name__)
CORS(app)

from agent_reasoner import run_agent

@app.route('/parse', methods=['POST'])
def parse():
    data = request.get_json()
    notes = data.get("notes", "")

    response = run_agent(notes)
    return jsonify({"result": response})

@app.route('/parse_notes', methods=['POST'])
def parse_notes():
    notes = request.get_json().get("notes", "")
    result = parse_notes_into_jira_tasks(notes)
    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(debug=True)
