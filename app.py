from flask import Flask
from flask import request, render_template
import db_processes


app = Flask(__name__)


@app.route("/vacancy/", methods=['GET', 'POST'])
def vacancies():
    with db_processes.Database() as db:
        if request.method == 'POST':
            company = request.form.get('company')
            position_name = request.form.get('position_name')
            description = request.form.get('description')
            contacts_ids = request.form.get('contacts_ids')
            comment = request.form.get('comment')
            vacancy_data = {
                'user_id': 1,
                'creation_date': "06.02.2023",
                'company': company,
                'position_name': position_name,
                'description': description,
                'contacts_ids': contacts_ids,
                'comment': comment
                }
            db.insert("vacancy", vacancy_data)
            result = db.query("SELECT * FROM vacancy")
        elif request.method == 'GET':
            result = db.query("SELECT * FROM vacancy")
        return render_template('vacancy.html', vacancies=result)


@app.route("/vacancy/<int:id_vacancy>/", methods=['GET', 'POST'])
def vacancy_id(id_vacancy):
    with db_processes.Database() as db:
        if request.method == 'POST':  # 'PUT'
            company = request.form.get('company')
            position_name = request.form.get('position_name')
            description = request.form.get('description')
            contacts_ids = request.form.get('contacts_ids')
            comment = request.form.get('comment')
            vacancy_data = {
                'user_id': 1,
                'creation_date': "06.02.2023",
                'company': company,
                'position_name': position_name,
                'description': description,
                'contacts_ids': contacts_ids,
                'comment': comment
                }
            db.update("vacancy", vacancy_data, f"id = {id_vacancy}")
            result = db.query(f"SELECT * FROM vacancy WHERE id = {id_vacancy}")
        elif request.method == 'GET':
            result = db.query(f"SELECT * FROM vacancy WHERE id = {id_vacancy}")
        return render_template('vacancy-one.html', vacancy=result, id_vacancy=id_vacancy)


@app.route("/vacancy/<int:id_vacancy>/events/", methods=['GET', 'POST'])
def vacancy_events(id_vacancy):
    with db_processes.Database() as db:
        if request.method == 'POST':
            description = request.form.get('description')
            event_date = request.form.get('event_date')
            title = request.form.get('title')
            deadline_date = request.form.get('deadline_date')
            event_data = {
                'vacancy_id': id_vacancy,
                'description': description,
                'event_date': event_date,
                'title': title,
                'deadline_date': deadline_date,
                }
            db.insert("events", event_data)
            result = db.query(f"SELECT * FROM events WHERE vacancy_id = {id_vacancy}")
        elif request.method == 'GET':
            result = db.query(f"SELECT * FROM events WHERE vacancy_id = {id_vacancy}")
        return render_template('event.html', event=result, id_vacancy=id_vacancy)


@app.route("/vacancy/<int:id_vacancy>/events/<int:id_events>/", methods=['GET', 'POST'])
def vacancy_events_id(id_vacancy, id_events):
    with db_processes.Database() as db:
        if request.method == 'POST':  # 'PUT'
            description = request.form.get('description')
            event_date = request.form.get('event_date')
            title = request.form.get('title')
            deadline_date = request.form.get('deadline_date')
            event_data = {
                'vacancy_id': id_vacancy,
                'description': description,
                'event_date': event_date,
                'title': title,
                'deadline_date': deadline_date,
            }
            db.update("events", event_data, f"id = {id_events}")
            result = db.query(f"SELECT * FROM events WHERE vacancy_id = {id_vacancy} AND id = {id_events}")
        elif request.method == 'GET':
            result = db.query(f"SELECT * FROM events WHERE vacancy_id = {id_vacancy} AND id = {id_events}")
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
