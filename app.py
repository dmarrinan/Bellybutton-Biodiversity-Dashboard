import pandas as pd
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import(
    Flask,
    render_template,
    jsonify
)

# Database Setup
engine = create_engine("sqlite:///db/belly_button_biodiversity.sqlite")

# reflect existing database into new model
Base = automap_base()

# reflect tables
Base.prepare(engine, reflect=True)

# save reference to tables
otus = Base.classes.otu
samples = Base.classes.samples
samples_metadata = Base.classes.samples_metadata

# create session to query tables
session = Session(engine)

# create inspector to get column names
inspector = inspect(engine)

app = Flask(__name__)

# create route to return list of sample names


@app.route("/names")
def names():
    results = session.query(samples_metadata.SAMPLEID).all()
    names = list(np.ravel(results))
    for index in range(len(names)):
        names[index] = "BB_" + str(names[index])
    print(names)
    return jsonify(names)

# create route to return metadata for a given sample


@app.route('/metadata/<sample>')
def metadata(sample):
    sample_id = sample.split('_')[1]
    results = session.query(samples_metadata).filter(
        samples_metadata.SAMPLEID == sample_id).all()
    metadata_dict = {}
    for sample in results:
        metadata_dict["SAMPLEID"] = int(sample.SAMPLEID)
        metadata_dict["ETHNICITY"] = str(sample.ETHNICITY)
        metadata_dict["GENDER"] = str(sample.GENDER)
        metadata_dict["AGE"] = int(sample.AGE)
        metadata_dict["BBTYPE"] = str(sample.BBTYPE)
        metadata_dict["LOCATION"] = str(sample.LOCATION)
        metadata_dict["WFREQ"] = float(sample.WFREQ)

    print(metadata_dict)
    return jsonify(metadata_dict)


@app.route('/piechart/<sample>')
def pie_chart(sample):
    # get sample values and otuIDs
    samples_df = pd.read_sql_table('samples', session.bind)
    sample_df = samples_df.loc[:, ['otu_id', sample]
                               ].sort_values(sample, ascending=False)
    otu_ids_sorted = list(sample_df.iloc[:10, 0])
    samples_sorted = list(sample_df.iloc[:10, 1])

    # get otu descriptions
    results = session.query(otus.lowest_taxonomic_unit_found).all()
    otu_descriptions = list(np.ravel(results))
    otu_descriptions_sorted = []
    for index in range(len(otu_ids_sorted)):
        otu_id = otu_ids_sorted[index]
        otu_descriptions_sorted.append(otu_descriptions[otu_id])

   #build response object
    response_object = {'otu_ids': otu_ids_sorted,'sample_values': samples_sorted,'otu_descriptions' : otu_descriptions_sorted}
    
    #return response object
    return jsonify(response_object)

@app.route('/wfreq/<sample>')
def wfreq(sample):
    wfreq = 0
    sample_id = sample.split('_')[1]
    print(sample_id)
    results = session.query(samples_metadata).filter(
        samples_metadata.SAMPLEID == sample_id).all()
    for sample in results:
        wfreq = sample.WFREQ
    print(wfreq)
    return wfreq

@app.route('/bubblechart/<sample>')
def bubble_chart(sample):
    # get otu descriptions
    results = session.query(otus.lowest_taxonomic_unit_found).all()
    otu_descriptions = list(np.ravel(results))

    # get sample values and otuIDs
    samples_df = pd.read_sql_table('samples', session.bind)
    samples_df ['otu_descriptions'] = pd.Series(otu_descriptions)
    sample_df = samples_df.loc[:, ['otu_id', sample,'otu_descriptions']
                               ].sort_values(sample, ascending=False)
    otu_ids_sorted = list(sample_df.iloc[:, 0])
    samples_sorted = list(sample_df.iloc[:, 1])
    otu_descriptions_sorted = list(sample_df.iloc[:,2])

   #build response object
    response_object = {'otu_ids': otu_ids_sorted,'sample_values': samples_sorted,'otu_descriptions' : otu_descriptions_sorted}
    
    #return response object
    return jsonify(response_object)


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
