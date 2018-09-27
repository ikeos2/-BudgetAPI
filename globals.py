from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from jwcrypto import jwk

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://webapp:secret@localhost:5432/purchases"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_DEBUG'] = True
db = SQLAlchemy(app)

# TODO: Dont store creds like an idiot
engine = create_engine('postgresql://webapp:secret@localhost:5432/purchases',
                       pool_size=5, max_overflow=0, echo=True)
session = sessionmaker(bind=engine)
Session = session()

key = jwk.JWK(generate='oct', size=256)
