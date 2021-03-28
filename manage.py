import sys
from backend import get_app

if __name__ == '__main__':
    if len(sys.argv) == 1:
        DEBUG = 1
    elif sys.argv[1] == "PRODUCTION":
        DEBUG = 0
    else:
        DEBUG = 1
    app = get_app(DEBUG)
    app.run(host='0.0.0.0', debug=DEBUG)