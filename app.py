from flask import Flask, redirect, url_for
from flask import request, render_template
from flask import session
from models import Vacancy, Event, EmailCredentials, User
from datetime import datetime
from bson.objectid import ObjectId
import db_alchemy
import email_lib
import db_mongo
from celery_worker import send_mail

app = Flask(__name__)
app.secret_key = 'mysecretkey'


@app.route("/welcome/", methods=['GET', 'POST'])
def welcome_vacancies():
    current_user = session.get('user_name', None)
    if request.method == 'POST':
        db_alchemy.init_db()
        result = db_alchemy.db_session.query(Vacancy).all()
        return render_template('vacancies.html', vacancies=result)
    return render_template('welcome-vacancy.html', user_name=current_user)


@app.route("/registration/", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form.get('username')
        useremail = request.form.get('useremail')
        userlogin = request.form.get('userlogin')
        userpassword = request.form.get('userpassword')
        if username == "" or useremail == "" or userlogin == "" or userpassword == "":
            return redirect(url_for('registration'))

        new_user = User(name=username, email=useremail, login=userlogin, password=userpassword)
        db_alchemy.db_session.add(new_user)
        db_alchemy.db_session.commit()

        return redirect(url_for('login'))
    return render_template('registration.html')


@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userlogin = request.form.get('userlogin')
        userpassword = request.form.get('userpassword')
        if userlogin == "" or userpassword == "":
            return redirect(url_for('login'))
        user = db_alchemy.db_session.query(User).filter(User.login == userlogin).first()
        if user is None:
            return redirect(url_for('login'))
        if user.password != userpassword:
            return redirect(url_for('login'))
        session['user_id'] = user.id
        session['user_name'] = user.name
        return redirect(url_for('welcome_vacancies'))
    return render_template('login.html')


@app.route("/logout/", methods=['GET'])
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('login'))


@app.route("/vacancy/", methods=['GET', 'POST'])
def vacancies():
    if session.get('user_id', None) is None:
        return redirect(url_for('login'))
    db_alchemy.init_db()
    result = db_alchemy.db_session.query(Vacancy).filter_by(user_id=session.get('user_id')).all()
    return render_template('vacancies.html', vacancies=result)


@app.route("/vacancy/<int:id_vacancy>/", methods=['GET', 'POST'])
def vacancy_id(id_vacancy):
    if session.get('user_id', None) is None:
        return redirect(url_for('login'))
    db_alchemy.init_db()
    db_mongo.init_db_mongo()
    result = db_alchemy.db_session.query(Vacancy).filter_by(id=id_vacancy).all()
    for item in result:
        contacts = item.contacts_ids.split(',')
        contacts_result = []
        for contact in contacts:
            date = db_mongo.init_db_mongo().find_one({'_id': ObjectId(contact)})
            contacts_result.append(date)
        return render_template('vacancy-one.html', vacancy=result, id_vacancy=id_vacancy, contacts_result=contacts_result)


@app.route("/vacancy-add/", methods=['GET', 'POST'])
def vacancies_add():
    if session.get('user_id', None) is None:
        return redirect(url_for('login'))
    db_alchemy.init_db()
    db_mongo.init_db_mongo()

    if request.method == 'POST':
        company = request.form.get('company')
        position_name = request.form.get('position_name')
        description = request.form.get('description')
        contacts_name = request.form.get('contacts_name')
        contacts_mobile = request.form.get('contacts_mobile')
        contacts_email = request.form.get('contacts_email')
        comment = request.form.get('comment')
        user_id = session.get('user_id')

        contacts_id_inserted = db_mongo.init_db_mongo().insert_one(
            {"name": contacts_name, "mobile": contacts_mobile, "email": contacts_email}
        ).inserted_id

        current_vacancies = Vacancy(company, position_name, description, str(contacts_id_inserted), comment, status=1, user_id=user_id)
        db_alchemy.db_session.add(current_vacancies)
        db_alchemy.db_session.commit()
        result = db_alchemy.db_session.query(Vacancy).filter_by(user_id=session.get('user_id')).all()

        return render_template('vacancies.html', vacancies=result)
    return render_template('vacancy-add.html')


@app.route("/vacancy/<int:id_vacancy>/events/", methods=['GET', 'POST'])
def vacancy_events(id_vacancy):
    if session.get('user_id', None) is None:
        return redirect(url_for('login'))
    db_alchemy.init_db()
    result = db_alchemy.db_session.query(Event).filter_by(vacancy_id=id_vacancy).all()
    return render_template('events.html', events=result, id_vacancy=id_vacancy)


@app.route("/vacancy/<int:id_vacancy>/events/<int:id_events>/", methods=['GET', 'POST'])
def vacancy_events_id(id_vacancy, id_events):
    if session.get('user_id', None) is None:
        return redirect(url_for('login'))
    db_alchemy.init_db()
    result = db_alchemy.db_session.query(Event).filter_by(vacancy_id=id_vacancy, id=id_events).all()
    return render_template('event-one.html', events=result, id_vacancy=id_vacancy, id_events=id_events)


@app.route("/vacancy/<int:id_vacancy>/events-add/", methods=['GET', 'POST'])
def vacancy_events_add(id_vacancy):
    if session.get('user_id', None) is None:
        return redirect(url_for('login'))
    db_alchemy.init_db()
    if request.method == 'POST':
        vacancy_id = id_vacancy
        description = request.form.get('description')
        title = request.form.get('title')

        input_event_date_str = request.form.get('event_date')
        input_event_date = datetime.strptime(input_event_date_str, '%Y-%m-%dT%H:%M')
        event_date = input_event_date.strftime('%Y-%m-%d %H:%M:%S.%f')

        input_deadline_date_str = request.form.get('deadline_date')
        input_deadline_date = datetime.strptime(input_deadline_date_str, '%Y-%m-%dT%H:%M')
        deadline_date = input_deadline_date.strftime('%Y-%m-%d %H:%M:%S.%f')

        current_events = Event(vacancy_id, description, event_date, title, deadline_date, status=1)
        db_alchemy.db_session.add(current_events)
        db_alchemy.db_session.commit()
        result = db_alchemy.db_session.query(Event).filter_by(vacancy_id=id_vacancy).all()
        return render_template('events.html', events=result, id_vacancy=id_vacancy)
    return render_template('event-add.html', id_vacancy=id_vacancy)


@app.route("/vacancy/<id>/history/", methods=['GET'])
def vacancy_history():
    if session.get('user_id', None) is None:
        return redirect(url_for('login'))
    return "Vacancy history"


@app.route("/user/", methods=['GET'])
def user_main_page():
    if session.get('user_id', None) is None:
        return redirect(url_for('login'))
    return "User main page"


@app.route("/user/calendar/", methods=['GET'])
def user_calendar():
    if session.get('user_id', None) is None:
        return redirect(url_for('login'))
    return "User Calendar"


@app.route("/user/mail/", methods=['GET', 'POST'])
def user_mail():
    if session.get('user_id', None) is None:
        return redirect(url_for('login'))
    user_email_settings = db_alchemy.db_session.query(EmailCredentials).filter_by(user_id=session.get('user_id')).first()
    email_obj = email_lib.EmailWrapper(
        user_email_settings.email,
        user_email_settings.login,
        user_email_settings.password,
        user_email_settings.smtp_server,
        user_email_settings.smtp_port,
        user_email_settings.pop_server,
        user_email_settings.pop_port,
        user_email_settings.imap_server,
        user_email_settings.imap_port
    )
    if request.method == 'POST':

        recipient = request.form.get('recipient')
        email_message = request.form.get('email_message')
        send_mail.apply_async(args=[user_email_settings.id, recipient, email_message])
        return "SEND MAIL"
    emails = email_obj.get_emails([1, 2, 3], protocol='pop3')
    return render_template('send_email.html', emails=emails)


@app.route("/user/settings/", methods=['GET', 'PUT'])
def user_settings():
    if session.get('user_id', None) is None:
        return redirect(url_for('login'))
    return "User Settings"


@app.route("/user/documents/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_documents():
    if session.get('user_id', None) is None:
        return redirect(url_for('login'))
    return "User Documents"


@app.route("/user/templates/", methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_templates():
    if session.get('user_id', None) is None:
        return redirect(url_for('login'))
    return "User Templates"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005)
