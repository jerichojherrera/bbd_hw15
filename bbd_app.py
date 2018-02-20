from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import pandas as pd


engine = create_engine("sqlite:///belly_button_biodiversity.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)


samples = Base.classes.samples
otu = Base.classes.otu


session = Session(engine)


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("bbd_index.html")



@app.route('/names')
def names():
    results = session.query(samples).statement
    results_df = pd.read_sql_query(results, session.bind)
    results_df.set_index('otu_id', inplace=True)
    return jsonify(list(results_df.columns))

@app.route('/otu')
def otu():
    otus = session.query(otu).statement
    otus_df = pd.read_sql_query(otus, session.bind)
    otus_df.set_index('otu_id', inplace=True)
    return jsonify(otus_df)



if __name__ == "__main__":
    app.run(debug=True)