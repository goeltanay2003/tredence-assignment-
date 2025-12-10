from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print('GET /')
resp = client.get('/')
print(resp.status_code)
print(resp.json())

print('\nGET /graph/demo/code-review')
resp = client.get('/graph/demo/code-review')
print(resp.status_code)
schema = resp.json()
print(schema)

# Transform nodes/edges to match /graph/create expected schema
nodes = []
for n in schema['nodes']:
    nodes.append({
        'name': n['name'],
        'node_type': n['type'],
        'tool_name': n.get('tool'),
        'metadata': {}
    })

edges = []
for e in schema['edges']:
    edges.append({
        'from_node': e['from'],
        'to_node': e['to'],
        'condition': e.get('condition')
    })

create_payload = {
    'name': schema['name'],
    'description': schema.get('description'),
    'nodes': nodes,
    'edges': edges,
    'entry_point': schema['entry_point'],
    'exit_point': schema.get('exit_point')
}

print('\nPOST /graph/create')
resp = client.post('/graph/create', json=create_payload)
print(resp.status_code)
create_resp = resp.json()
print(create_resp)

graph_id = create_resp['graph_id']

print('\nPOST /graph/run')
code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total
"""
run_payload = {
    'graph_id': graph_id,
    'initial_state': { 'code': code }
}
resp = client.post('/graph/run', json=run_payload)
print(resp.status_code)
run_resp = resp.json()
print(run_resp)

run_id = run_resp['run_id']

print(f'\nGET /graph/state/{run_id}')
resp = client.get(f'/graph/state/{run_id}')
print(resp.status_code)
print(resp.json())
