from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Event:
    db = 'events'

    @staticmethod
    def create_event(data):
        query = """
        INSERT INTO events (name, location, date, details, user_id)
        VALUES (%(name)s, %(location)s, %(date)s, %(details)s, %(user_id)s)
        """
        return connectToMySQL(Event.db).query_db(query, data)

    @staticmethod
    def get_all_events():
        query = """
        SELECT events.*, users.first_name, users.last_name
        FROM events
        JOIN users ON events.user_id = users.id
        """
        return connectToMySQL(Event.db).query_db(query)

    @staticmethod
    def get_event_by_id(event_id):
        query = """
        SELECT events.*, users.first_name, users.last_name
        FROM events
        JOIN users ON events.user_id = users.id
        WHERE events.id = %(id)s
        """
        data = {'id': event_id}
        result = connectToMySQL(Event.db).query_db(query, data)
        return result[0] if result else None

    @staticmethod
    def update_event(data):
        query = """
        UPDATE events
        SET name = %(name)s, location = %(location)s, date = %(date)s, details = %(details)s
        WHERE id = %(id)s
        """
        return connectToMySQL(Event.db).query_db(query, data)

    @staticmethod
    def delete_event(event_id):
        query = "DELETE FROM events WHERE id = %(id)s"
        data = {'id': event_id}
        return connectToMySQL(Event.db).query_db(query, data)

    @staticmethod
    def validate_event(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("El nombre del evento debe tener al menos 3 caracteres", 'event')
            is_valid = False
        if len(data['location']) < 3:
            flash("La ubicación del evento debe tener al menos 3 caracteres", 'event')
            is_valid = False
        if len(data['details']) < 3:
            flash("Los detalles del evento deben tener al menos 3 caracteres", 'event')
            is_valid = False
        return is_valid
