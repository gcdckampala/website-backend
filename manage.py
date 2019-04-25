import os
import pytest
from flask_script import Manager, Server, Shell
from flask_migrate import Migrate, MigrateCommand
from application import create_app, db
from dotenv import load_dotenv


load_dotenv()


app = create_app(os.getenv('FLASK_ENV', 'development'))
migrate = Migrate(app, db)
manager = Manager(app)


def _make_context():
    return dict(app=app, db=db)


@manager.command
def test():
    pytest.main(["-s", "tests/"])


@manager.command
def test_coverage():
    pytest.main(["--cov=api", "tests/"])


# Turn on reloader
manager.add_command('runserver', Server(
    use_reloader=True,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 5000))
))

# Migrations
manager.add_command('db', MigrateCommand)


manager.add_command("shell", Shell(make_context=_make_context))


if __name__ == '__main__':
    manager.run()
