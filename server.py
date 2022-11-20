from flask import Flask, request

from clash_yaml_add_url_test import transfer_logic
from config import config

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def transfer():
    url = request.args.get('url')
    new_config_test = transfer_logic(url)
    return new_config_test


def main():
    from gevent.pywsgi import WSGIServer
    
    http_server = WSGIServer(
        (config.HOST, config.PORT),
        app,
    )
    
    http_server.serve_forever()


if __name__ == '__main__':
    main()
