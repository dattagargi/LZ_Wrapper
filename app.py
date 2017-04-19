'''
This script creats a local server app to host user data and handle json requests for LocusZoom.
When a json request comes in, the app parses the csv generated by createCSV.py to
create and send a response.
'''


from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import json
from flask_cors import CORS
import pandas

app = Flask(__name__)
CORS(app, headers=['Content-Type'])

print 'Initializing data frame'
df=pandas.read_csv('assoc.csv', engine='c', dtype={'chromosome':str})

@app.route('/single/results/', methods=['GET', 'POST'])
def results():
  #analysis in 3 and chromosome in  '15' and position ge 78800000 and position le 78900000
  args = request.args
  filters = args['filter']
  filter_vals=filters.split('and')
 
  analysis = filter_vals[0].split(' in ')[1].strip()
  chrom = filter_vals[1].split(' in ')[1].replace('\'','').strip()
  low_pos = int(filter_vals[2].split(' ge ')[1])
  high_pos = int(filter_vals[3].split(' le ')[1])

  result = parseAssoc(analysis, chrom, low_pos, high_pos) 
  return jsonify(result)

def parseAssoc(analysis, chrom, low_pos, high_pos):
  sub = df[(df.analysis==analysis) & (df.chromosome==chrom) & (df.position >= low_pos) & (df.position <= high_pos)]
  sub["ref_allele_freq"] = None
  sub["score_test_stat"] = None
  data_dict = sub.to_dict(orient='list')
  result = {'data': data_dict, 'last_page':None}
  return result

if __name__ == '__main__':
     app.run(port=8000)
