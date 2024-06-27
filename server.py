from flask import Flask, request
from threading import Thread

app = Flask(__name__)
command_queue = None

@app.route('/mediahub', methods=['GET'])
def handle_media_request():
    state = request.args.get('state')
    obj = request.args.get('object')

    if obj is None:
        return '', 404

    # Add command to the queue
    command_queue.put({'state': state, 'object': obj})
    return '', 200

def run_server(queue):
    global command_queue
    command_queue = queue
    app.run(host='0.0.0.0', port=5000)

def start_server_thread(queue):
    server_thread = Thread(target=run_server, args=(queue,))
    server_thread.daemon = True
    server_thread.start()
