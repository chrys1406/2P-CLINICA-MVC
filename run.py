from flask import Flask, request, redirect, url_for, session
from controllers import usuario_controller, medico_controller, paciente_controller, consulta_controller
from database import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clinica.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "clinica_secret_key_2026"

db.init_app(app)

app.register_blueprint(usuario_controller.usuario_bp)
app.register_blueprint(medico_controller.medico_bp)
app.register_blueprint(paciente_controller.paciente_bp)
app.register_blueprint(consulta_controller.consulta_bp)

@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path == path else ''
    return dict(is_active=is_active)

@app.context_processor
def inject_session():
    return dict(session=session)

@app.route("/")
def home():
    if 'usuario_id' not in session:
        return redirect(url_for('usuario.login'))
    return redirect(url_for('consulta.index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
