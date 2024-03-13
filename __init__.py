from flask import Flask, render_template
from flask_socketio import SocketIO
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, DateTime, Boolean, ForeignKey,ARRAY
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

app = Flask(__name__)
socketio = SocketIO(app)
Base = declarative_base()

