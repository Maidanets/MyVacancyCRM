from flask import Flask
from flask import request

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


@app.route("/vacancy/", methods=['GET', 'POST'])
def vacancies():
    return vacancies_date


@app.route("/vacancy/<vacancy_id>/", methods=['GET', 'PUT'])
def vacancy_id(id_vacancy):
    for vacancy in vacancies_date:
        if vacancy['id'] == id_vacancy:
            return vacancy


@app.route("/vacancy/<vacancy_id>/events/", methods=['GET', 'POST'])
def vacancy_events(id_vacancy):
    events_list = []
    for event in events_date:
        if event['vacancy_id'] == id_vacancy:
            events_list.append(event)
    return events_list



@app.route("/vacancy/<vacancy_id>/events/<events_id>/", methods=['GET', 'PUT'])
def vacancy_events_id(id_event):
    for event in events_date:
        if event['id'] == id_event:
            return event


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
