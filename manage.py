from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User

manager = Manager(app)
manager.add_command('server',Server)

# Creating app instance
app = create_app("production")

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command("server", Server)
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()