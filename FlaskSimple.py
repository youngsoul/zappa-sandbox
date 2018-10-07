from flask import Flask
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


app = Flask(__name__)

# here is how we are handling routing with flask:
@app.route('/')
def index():
    logger.debug("FlaskSimple.index: debug message")
    logger.info("FlaskSimple.index: info message")
    logger.warning("FlaskSimple.index: warn message")
    logger.error("FlaskSimple.index: error message")
    return "Hello Zappa, Flask, AWS Lambda World!", 200

# include this for local dev

if __name__ == '__main__':
    app.run()