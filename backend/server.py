from flask import Flask, request, jsonify
from flask_cors import CORS

from .sidekick import sidekick_core
from .context.context_memory import set_context_field
from .utils.credentials import save_credentials

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

@app.route('/set-project', methods=['POST'])
def set_project_dash_route():
    project = request.get_json().get('project')
    if not project:
        return jsonify({'error': 'Missing project'}), 400
    set_context_field('active_project_key', project)
    return jsonify({'active_project_key': project})

@app.route('/set_assignee', methods=['POST'])
def set_assignee_route():
    assignee = request.get_json().get('assignee')
    if not assignee:
        return jsonify({'error': 'Missing assignee'}), 400
    set_context_field('default_assignee', assignee)
    return jsonify({'default_assignee': assignee})


@app.route('/connect_jira', methods=['POST'])
def connect_jira_route():
    data = request.get_json()
    required = ['url', 'email', 'api_token', 'domain']
    if not all(data.get(k) for k in required):
        return jsonify({'error': 'Missing Jira credentials'}), 400

    save_credentials(data['url'], data['email'], data['api_token'], data['domain'])
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
