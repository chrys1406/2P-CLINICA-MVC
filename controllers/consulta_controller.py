from flask import request, redirect, url_for, Blueprint
from datetime import datetime

from models.consulta_model import Consulta
from models.medico_model import Medico
from models.paciente_model import Paciente
from views import consulta_view

consulta_bp = Blueprint('consulta', __name__, url_prefix="/consultas")

@consulta_bp.route("/")
def index():
    fecha_filtro = request.args.get('fecha')
    if fecha_filtro:
        fecha_dt = datetime.strptime(fecha_filtro, '%Y-%m-%d').date()
        consultas = Consulta.query.filter(
            Consulta.fecha >= datetime.combine(fecha_dt, datetime.min.time()),
            Consulta.fecha < datetime.combine(fecha_dt, datetime.max.time())
        ).all()
    else:
        consultas = Consulta.get_all()
    return consulta_view.list(consultas, fecha_filtro=fecha_filtro)

@consulta_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        medico_id = request.form['medico_id']
        paciente_id = request.form['paciente_id']
        fecha_str = request.form['fecha']
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']

        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')

        consulta = Consulta(fecha=fecha, diagnostico=diagnostico,
                            tratamiento=tratamiento, medico_id=medico_id,
                            paciente_id=paciente_id)
        consulta.save()
        return redirect(url_for('consulta.index'))

    medicos = Medico.query.all()
    pacientes = Paciente.query.all()
    return consulta_view.create(medicos, pacientes)

@consulta_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    consulta = Consulta.get_by_id(id)
    if request.method == 'POST':
        medico_id = request.form['medico_id']
        paciente_id = request.form['paciente_id']
        fecha_str = request.form['fecha']
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']

        fecha = datetime.strptime(fecha_str, '%Y-%m-%d')

        consulta.update(fecha=fecha, diagnostico=diagnostico,
                        tratamiento=tratamiento, medico_id=medico_id,
                        paciente_id=paciente_id)
        return redirect(url_for('consulta.index'))

    medicos = Medico.query.all()
    pacientes = Paciente.query.all()
    return consulta_view.edit(consulta, medicos, pacientes)

@consulta_bp.route("/delete/<int:id>")
def delete(id):
    consulta = Consulta.get_by_id(id)
    consulta.delete()
    return redirect(url_for('consulta.index'))
