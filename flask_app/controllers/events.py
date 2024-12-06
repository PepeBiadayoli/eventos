from flask_app import app
from flask import render_template, request, redirect, url_for, session, flash
from flask_app.models.event import Event
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    user = User.get_by_id(session['user_id'])
    events = Event.get_all_events()
    return render_template('dashboard.html', user=user, events=events)

@app.route('/event/new', methods=['GET', 'POST'])
def create_event():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'location': request.form['location'],
            'date': request.form['date'],
            'details': request.form['details'],
            'user_id': session['user_id']
        }

        if not Event.validate_event(data):
            return redirect(url_for('create_event'))
        
        Event.create_event(data)
        return redirect(url_for('dashboard'))

    return render_template('event_create.html')

@app.route('/event/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    event = Event.get_event_by_id(event_id)
    if not event or event['user_id'] != session['user_id']:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        data = {
            'id': event_id,
            'name': request.form['name'],
            'location': request.form['location'],
            'date': request.form['date'],
            'details': request.form['details']
        }

        if not Event.validate_event(data):
            return redirect(url_for('edit_event', event_id=event_id))

        Event.update_event(data)
        return redirect(url_for('dashboard'))

    return render_template('event_edit.html', event=event)

@app.route('/event/view/<int:event_id>')
def view_event(event_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    event = Event.get_event_by_id(event_id)
    if not event:
        return redirect(url_for('dashboard'))

    return render_template('event_view.html', event=event)

@app.route('/event/delete/<int:event_id>')
def delete_event(event_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    event = Event.get_event_by_id(event_id)
    if event and event['user_id'] == session['user_id']:
        Event.delete_event(event_id)
    
    return redirect(url_for('dashboard'))


