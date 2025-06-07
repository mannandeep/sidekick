from flask import Flask, request, jsonify
from flask_cors import CORS

from .sidekick import sidekick_core
from .context.context_memory import set_context_field

app = Flask(__name__)
CORS(app)

@app.route('/sidekick', methods=['POST'])
def sidekick_route():
    notes = request.get_json().get('notes', '')
    result = sidekick_core(notes)
    return jsonify(result)

@app.route('/set_project', methods=['POST'])
def set_project_route():
    key = request.get_json().get('key')
    if not key:
        return jsonify({'error': 'Missing project key'}), 400
    set_context_field('active_project_key', key)
    return jsonify({'active_project_key': key})

@app.route('/set_assignee', methods=['POST'])
def set_assignee_route():
    assignee = request.get_json().get('assignee')
    if not assignee:
        return jsonify({'error': 'Missing assignee'}), 400
    set_context_field('default_assignee', assignee)
    return jsonify({'default_assignee': assignee})

if __name__ == '__main__':
    app.run(debug=True)
