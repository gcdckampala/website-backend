from flask import Blueprint, jsonify, request
from .models import Program, ProgramSchema
from ..users.models import User

programs_app = Blueprint('programs_app', __name__)


@programs_app.route("/api/v1/programs", methods=['POST'])
def add_program():
    program_image = request.files.get('image')
    curriculum = request.files.get('curriculum')
    name = request.form.get('name')
    description = request.form.get('description')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    application_deadline = request.form.get('application_deadline')
    status = request.form.get('status')
    duration = request.form.get('duration')
    location = request.form.get('location')

    if not program_image or not curriculum:
        return jsonify(
            {"error": "Add the Program curriculum and Image"}), 400
    try:
        program = Program(
            name, program_image, description, start_date, end_date,
            application_deadline, status, duration, location, curriculum
        )
        program.save()
        program_schema = ProgramSchema()
        return jsonify(
            {'program': program_schema.dump(program).data}), 201
    except AssertionError as exception_message:
        return jsonify(error=f"{exception_message}."), 400


@programs_app.route("/api/v1/programs")
def get_programs():
    programs = Program.query.all()
    program_schema = ProgramSchema(many=True)
    return jsonify(
        {'programs': program_schema.dump(programs).data}), 200


@programs_app.route("/api/v1/programs/<int:id>")
def get_program(id):
    program = Program.get_program(id=id).first()
    if program:
        program_schema = ProgramSchema()
        return jsonify(
            {'program': program_schema.dump(program).data}), 200
    return jsonify({'error': 'Invalid Object Id'}), 400


@programs_app.route("/api/v1/programs/<int:id>/members",
                    methods=['PATCH'])
def add_learners(id):

    group = request.json.get('group')
    email = request.json.get('email')
    if not email or not group:
        return jsonify(
            {"error": "Both User Group and Email are Required"}), 400

    program = Program.get_program(id=id).first()
    user = User.get_user(email=email).first()
    if program and user:
        program = validate_type(program, group, user)
        if not program:
            return jsonify({"error": "Group Does Not Exist"}), 400
        program.save()
        program_schema = ProgramSchema()
        return jsonify(
            {'program': program_schema.dump(program).data}), 200
    return jsonify({"error": "Invalid Program Id or User Doesnt Exist"}), 400


def validate_type(program, group, user):
    if group == "learners":
        program.learners.append(user)
        return program

    if group == "facilitators":
        program.facilitators.append(user)
        return program

    if group == "organizers":
        program.organizers.append(user)
        return program

    return None


@programs_app.route("/api/v1/programs/<int:id>", methods=['DELETE'])
def delete_program(id):
    program = Program.get_program(id=id).first()
    if program:
        program.delete()
        return jsonify({'message': 'Program successfully deleted'}), 204
    return jsonify({'error': 'Invalid Program Id'}), 400
