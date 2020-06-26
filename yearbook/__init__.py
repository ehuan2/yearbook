from flask import Flask
from yearbook.config import Config
import os

# the following sets up the table and creates connection to db
def create_sql_db(db_url = 'sqlite:///site.db'):

    # needed imports
    from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
    
    # creating the database now:
    engine = create_engine('sqlite:///site.db', echo = False)

    # metadata to set up tables with
    metadata = MetaData()

    # sets up the table
    messages = Table('messages', metadata,
        Column('id', Integer, primary_key = True),
        Column('message', String),
        Column('name', String)
    )

    metadata.create_all(engine)

    # returns the engine and messages table
    return (engine, messages) 


# for the engine and the messages table
global_engine, global_messages = create_sql_db()

# creates the app
def create_app(config_class = Config):
    # creates it with the set configuration
    app = Flask(__name__)
    app.config.from_object(config_class)

    # adds in the main routes
    from yearbook.main.routes import main

    app.register_blueprint(main)

    return app


# a method to insert new messages
def insert_messages(message, name):
    
    with global_engine.connect() as conn:

        messages_sql = f"""SELECT messages.message, messages.name
        FROM messages"""

        result = conn.execute(messages_sql)

        for row in result:
            print(row)

        insert_sql = global_messages.insert().values(message = message, name = name)

        conn.execute(insert_sql)


# a method to view all the messages
def view_messages():
    messages = []
    with global_engine.connect() as conn:
        messages_sql = f"""SELECT messages.message, messages.name
        FROM messages"""

        result = conn.execute(messages_sql)

        # now gets all the messages
        messages = [(row[0], row[1]) for row in result]
    
    return messages