from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DatabaseUitls():

    def save(self):
        '''Utility method for saving new objects'''
        db.session.add(self)
        db.session.commit()

    def delete(self):
        '''Utility method for deleting objects'''
        db.session.delete(self)
        db.session.commit()
