from init import create_app
from db_process import getDB
from flask import  render_template

app = create_app()








if __name__ == '__main__':
    app.run(debug=True, port=3000)
