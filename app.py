from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/vacancy/", methods=['GET', 'POST'])
def vacancy():
    return "All vacancy"


@app.route("/vacancy/<id>/", methods=['GET', 'PUT'])
def vacancy_id():
    return "Vacancy id"


@app.route("/vacancy/<id>/events/", methods=['GET', 'POST'])
def vacancy_events():
    return "Vacancy events"


@app.route("/vacancy/<id>/events/<events_id>/", methods=['GET', 'PUT'])
def vacancy_events_id():
    return "Vacancy events id"


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
