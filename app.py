from flask import Flask
from flask import request, render_template
import db_processes


app = Flask(__name__)

vacancies_date = [
    {
        'id': 1,
        'creation_date': "02.02.2023",
        'status': 1,
        'company': "Company name 1",
        'contacts_ids': [1, 2],
        'description': "Description vacancy 1",
        'position_name': "Python developer",
        'comment': "My comment for vacancy 1",
        'user_id': 1
    },
    {
        'id': 2,
        'creation_date': "01.02.2023",
        'status': 1,
        'company': "Company name 2",
        'contacts_ids': [3],
        'description': "Description vacancy 2",
        'position_name': "Backend developer",
        'comment': "My comment for vacancy 2",
        'user_id': 1
    },
    {
        'id': 3,
        'creation_date': "25.01.2023",
        'status': 1,
        'company': "Company name 3",
        'contacts_ids': [4, 5],
        'description': "Description vacancy 3",
        'position_name': "ISO developer",
        'comment': "My comment for vacancy 2",
        'user_id': 1
    }
]

events_date = [
    {
        'id': 1,
        'vacancy_id': 1,
        'description': "Description event 1",
        'event_date': "04.02.2023",
        'title': "Event title for vacancy 1",
        'due_to_date': "08.02.2023",
        'status': 1
    },
    {
        'id': 2,
        'vacancy_id': 2,
        'description': "Description event 2",
        'event_date': "06.02.2023",
        'title': "Event title for vacancy 2",
        'due_to_date': "15.02.2023",
        'status': 1
    },
    {
        'id': 3,
        'vacancy_id': 2,
        'description': "Description event 3",
        'event_date': "07.02.2023",
        'title': "Event title for vacancy 2",
        'due_to_date': "15.02.2023",
        'status': 1
    }
]


@app.route("/vacancy/", methods=['GET', 'POST', 'PUT'])
def vacancies():
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
        db_processes.insert_info("vacancy", vacancy_data)
        all_vacancies = db_processes.select_info("SELECT * FROM vacancy")
        return render_template('vacancy.html', vacancies=all_vacancies)
    elif request.method == 'PUT':
        pass
    else:  # 'GET'
        all_vacancies = db_processes.select_info("SELECT * FROM vacancy")
        return render_template('vacancy.html', vacancies=all_vacancies)


@app.route("/vacancy/<int:id_vacancy>/", methods=['GET', 'PUT'])
def vacancy_id(id_vacancy):
    if request.method == 'GET':
        one_vacancy = db_processes.select_info(f"SELECT * FROM vacancy where id = {id_vacancy}")
        return render_template('vacancy-one.html', one_vacancy=one_vacancy, id_vacancy=id_vacancy)


@app.route("/vacancy/<int:id_vacancy>/events/", methods=['GET', 'POST'])
def vacancy_events(id_vacancy):
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
        db_processes.insert_info("events", event_data)
        all_event = db_processes.select_info(f"SELECT * FROM events where vacancy_id = {id_vacancy}")
        return render_template('event.html', event=all_event, id_vacancy=id_vacancy)
    else:  # 'GET'
        all_event = db_processes.select_info(f"SELECT * FROM events where vacancy_id = {id_vacancy}")
        return render_template('event.html', event=all_event, id_vacancy=id_vacancy)


@app.route("/vacancy/<int:id_vacancy>/events/<int:id_events>/", methods=['GET', 'PUT'])
def vacancy_events_id(id_vacancy, id_events):
    if request.method == 'GET':
        one_event = db_processes.select_info(f"SELECT * FROM events where vacancy_id = {id_vacancy} AND id = {id_events}")
        return render_template('event-one.html', one_event=one_event, id_vacancy=id_vacancy, id_events=id_events)


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
