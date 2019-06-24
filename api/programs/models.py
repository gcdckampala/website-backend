from api.utils.database import DatabaseUitls, db, ma
from sqlalchemy.orm import validates
from ..users.models import UserSchema
from ..utils.storage import upload_file

learners = db.Table('learners',
                    db.Column('learner_id', db.Integer, db.ForeignKey(
                        'users.id'), primary_key=True),
                    db.Column('program_id', db.Integer, db.ForeignKey(
                        'programs.id'), primary_key=True)
                    )

facilitators = db.Table('facilitators',
                        db.Column('facilitator_id', db.Integer, db.ForeignKey(
                            'users.id'), primary_key=True),
                        db.Column('program_id', db.Integer, db.ForeignKey(
                            'programs.id'), primary_key=True)
                        )

organizers = db.Table('organizers',
                      db.Column('organizer_id', db.Integer, db.ForeignKey(
                          'users.id'), primary_key=True),
                      db.Column('program_id', db.Integer, db.ForeignKey(
                          'programs.id'), primary_key=True)
                      )


class Program(db.Model, DatabaseUitls):

    __tablename__ = 'programs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    program_image = db.Column(db.String())
    description = db.Column(db.JSON)
    learners = db.relationship('User', secondary=learners, lazy='subquery',
                               backref=db.backref('learners', lazy=True), single_parent=True,)
    facilitators = db.relationship('User', secondary=facilitators,
                                   lazy='subquery',
                                   backref=db.backref('facilitators', lazy=True))
    organizers = db.relationship('User', secondary=organizers,
                                 lazy='subquery',
                                 backref=db.backref('organizers', lazy=True))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    application_deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String())
    duration = db.Column(db.String())
    location = db.Column(db.String())
    curriculum = db.Column(db.String())

    def __init__(self, *args):
        name, program_image, description, start_date, end_date, \
            application_deadline, status, duration, location, curriculum = args

        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.application_deadline = application_deadline
        self.status = status
        self.duration = duration
        self.location = location
        self.curriculum = curriculum
        self.program_image = program_image

    def __repr__(self):
        return f"<Program: {self.name}>"

    @classmethod
    def get_program(cls, name=None, id=None):
        if name and id:
            program = cls.query.filter_by(name=name, id=id)
        elif name and not id:
            program = cls.query.filter_by(name=name)
        elif id and not name:
            program = cls.query.filter_by(id=id)
        return program

    @validates('name')
    def validate_username(self, key, name):
        if not name:
            raise AssertionError('Program Name Not Provided')

        if self.get_program(name=name).first():
            raise AssertionError('Program Name Exists')

        if len(name) < 5:
            raise AssertionError('Program name should be greater than 5 chars')

        return name

    @validates('start_date')
    def validate_start_date(self, key, start_date):
        if not start_date:
            raise AssertionError('No Start Date provided')
        return start_date

    @validates('end_date')
    def validate_end_date(self, key, end_date):
        if not end_date:
            raise AssertionError('No End Date provided')
        return end_date

    @validates('application_deadline')
    def validate_application_deadline(self, key, application_deadline):
        if not application_deadline:
            raise AssertionError('No Application Deadline  provided')
        return application_deadline

    @validates('status')
    def validate_status(self, key, status):
        if not status:
            raise AssertionError('No status provided')
        return status

    @validates('description')
    def validate_description(self, key, description):
        if not description:
            raise AssertionError('No description provided')
        return description

    @validates('duration')
    def validate_duration(self, key, duration):
        if not duration:
            raise AssertionError('No durationprovided')
        return duration

    @validates('location')
    def validate_location(self, key, location):
        if not location:
            raise AssertionError('No location provided')
        return location

    @validates('program_image')
    def validate_program_image(self, key, program_image):
        if not program_image:
            raise AssertionError('No Program Image provided')
        program_image = upload_file(program_image.read(
        ), program_image.filename, program_image.content_type)
        return program_image

    @validates('curriculum')
    def validate_curriculum(self, key, curriculum):
        if not curriculum:
            raise AssertionError('No curriculum provided')
        curriculum = upload_file(
            curriculum.read(), curriculum.filename, curriculum.content_type)
        return curriculum


class ProgramSchema(ma.ModelSchema):
    class Meta:
        model = Program
        sqla_session = db.session
    learners = ma.Nested(UserSchema, many=True)
    organizers = ma.Nested(UserSchema, many=True)
    facilitators = ma.Nested(UserSchema, many=True)
