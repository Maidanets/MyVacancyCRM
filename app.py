from flask import Flask
from flask import request, render_template
from models import Vacancy, Event
import db_alchemy
import db_processes

app = Flask(__name__)


@app.route("/vacancy/", methods=['GET', 'POST'])
def vacancies():
    db_alchemy.init_db()
    if request.method == 'POST':
        company = request.form.get('company')
        position_name = request.form.get('position_name')
        description = request.form.get('description')
        contacts_ids = request.form.get('contacts_ids')
        comment = request.form.get('comment')
        current_vacancies = Vacancy(company, position_name, description, contacts_ids, comment, status=1, user_id=1)
        db_alchemy.db_session.add(current_vacancies)
        db_alchemy.db_session.commit()
    result = db_alchemy.db_session.query(Vacancy).all()
    return render_template('vacancy.html', vacancies=result)


@app.route("/vacancy/<int:id_vacancy>/", methods=['GET', 'POST'])
def vacancy_id(id_vacancy):
    db_alchemy.init_db()
#    if request.method == 'POST':  # 'PUT'
#        company = request.form.get('company')
#        position_name = request.form.get('position_name')
#        description = request.form.get('description')
#        contacts_ids = request.form.get('contacts_ids')
#        comment = request.form.get('comment')
#        current_vac = Vacancy(company, position_name, description, contacts_ids, comment, status=1, user_id=1)
    result = db_alchemy.db_session.query(Vacancy).filter_by(id=id_vacancy).all()
    return render_template('vacancy-one.html', vacancy=result, id_vacancy=id_vacancy)


@app.route("/vacancy/<int:id_vacancy>/events/", methods=['GET', 'POST'])
def vacancy_events(id_vacancy):
    db_alchemy.init_db()
    if request.method == 'POST':
        vacancy_id = id_vacancy
        description = request.form.get('description')
        event_date = request.form.get('event_date')
        title = request.form.get('title')
        deadline_date = request.form.get('deadline_date')
        current_events = Event(vacancy_id, description, event_date, title, deadline_date, status=1)
        db_alchemy.db_session.add(current_events)
        db_alchemy.db_session.commit()
    result = db_alchemy.db_session.query(Event).filter_by(vacancy_id=id_vacancy).all()
    return render_template('event.html', event=result, id_vacancy=id_vacancy)


@app.route("/vacancy/<int:id_vacancy>/events/<int:id_events>/", methods=['GET', 'POST'])
def vacancy_events_id(id_vacancy, id_events):
    db_alchemy.init_db()
#    if request.method == 'POST':  # 'PUT'
#        description = request.form.get('description')
#        event_date = request.form.get('event_date')
#        title = request.form.get('title')
#        deadline_date = request.form.get('deadline_date')
#        current_events = Event(vacancy_id, description, event_date, title, deadline_date, status=1)
    result = db_alchemy.db_session.query(Event).filter_by(vacancy_id=id_vacancy, id=id_events).all()
    return render_template('event-one.html', event=result, id_vacancy=id_vacancy, id_events=id_events)


@app.route("/vacancy/<id>/history/", methods=['GET'])
def vacancy_history():
    return "Vacancy history"


@app.route("/user/", methods=['GET'])
def user_main_page():
    return "User main page"


@app.route("/user/calendar/", methods=['GET'])
def user_calendar():
    return "User Calendar"


@app.route("/user/mail/", methods=['GET'])
def user_mail():
    return "User Mail"


@app.route("/user/settings/", methods=['GET', 'PUT'])
def user_settings():
    return "User Settings"


@app.route("/user/documents/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_documents():
    return "User Documents"


@app.route("/user/templates/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_templates():
    return "User Templates"


if __name__ == '__main__':
    app.run()
