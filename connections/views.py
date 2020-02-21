from http import HTTPStatus

from flask import Blueprint
from webargs import fields
from webargs.flaskparser import use_args

from connections.models.person import Person
from connections.models.connection import Connection, ConnectionType
from connections.schemas import ConnectionSchema, PersonSchema



blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
def get_people():
    people_schema = PersonSchema(many=True)
    people = Person.query.all()
    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['GET'])
def get_connections():
    connection_schema = ConnectionSchema(many=True)
    connections = Connection.query.all()
    return connection_schema.jsonify(connections), HTTPStatus.OK

# Get all Connections
@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED

# Handle updating connection_type
@blueprint.route("/connections/<connection_id>", methods=['PATCH'])
@use_args({"connection_type": fields.Str(required=True)}, locations=('json',))  # TODO: Determine if we can use enumfield here
def update_connection_type(args, connection_id):
    connection_schema = ConnectionSchema()
    new_connection_type = args['connection_type']

    connection = Connection.query.get_or_404(connection_id) # If not found, return 404

    # Validate Connection Type
    if not new_connection_type in ConnectionType.list():
        return "Invalid Connection Type", HTTPStatus.BAD_REQUEST

    # Set value and save
    connection.connection_type = ConnectionType[new_connection_type]
    connection.save()

    return connection_schema.jsonify(connection), HTTPStatus.OK
