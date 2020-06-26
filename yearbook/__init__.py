from flask import Flask
from yearbook.config import Config
import os

# the following sets up the table and creates connection to db
def create_sql_db(db_url = 'sqlite:///site.db'):

    # needed imports
    from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
    
    # creating the database now:
    engine = create_engine('sqlite:///site.db', echo = True)

    # metadata to set up tables with
    metadata = MetaData()

    # sets up the table
    messages = Table('messages', metadata,
        Column('id', Integer, primary_key = True),
        Column('message', String)
    )

    metadata.create_all(engine)

    # returns the engine and messages table
    return (engine, messages) 


# creates the app
def create_app(config_class = Config):
    # creates it with the set configuration
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # before the first request, it creates a table with an image id and a blob
    @app.before_first_request
    def create_tables():

        create_sql_db()


    # adds in the main routes
    from yearbook.main.routes import main

    app.register_blueprint(main)

    return app


def insert_messages(message):
    with engine.connect() as conn:

        messages_sql = f"""SELECT messages.message
        FROM {table_name}"""

        result = conn.execute(messages_sql)

        for row in result:
            print(row)

        insert_sql = f"""
        INSERT INTO {table_name}
        VALUES (?);
        ('{message}')
        """

        conn.execute(insert_sql)


def view_messages():
    messages = []
    with engine.connect() as conn:
        messages_sql = f"""SELECT messages.message
        FROM {table_name}"""

        result = conn.execute(messages_sql)

        # now gets all the messages
        messages = [row[0] for row in result]
    
    return messages