from flask import Flask


def create_app():
    app = Flask(__name__)

    with app.app_context():
        from home import home_bp
        from cash import cash_bp
        from stock import stock_bp
        app.register_blueprint(home_bp)
        app.register_blueprint(cash_bp)
        app.register_blueprint(stock_bp)
    return app
