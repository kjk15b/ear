from flask import Flask, render_template, request, redirect, url_for
import json
import os
import subprocess
import re

app = Flask(__name__)

@app.route('/')
def echotrail_route():
    num_exes = len(os.listdir(os.path.join(os.getcwd(), 'static/echotrail/')))
    return render_template('home.html', page_name='EAR', num_exes=num_exes)


@app.route('/insights/search/<exe>')
def search_exe_route(exe : str):
    exe = exe.lower()
    try:
        f = open('static/echotrail/{}.json'.format(exe), 'r')
        data = json.load(f)
        if 'message' not in data.keys():
            return render_template('service-template.html', exe=exe, svc=data, page_name=exe)
        else:
            return "Try again later, API at limit for: {}".format(exe)
    except FileNotFoundError:
        return "Could not find: {}".format(exe)

@app.route('/api/insights/search/<exe>')
def search_exe_api_route(exe : str):
    exe = exe.lower()
    try:
        f = open('static/echotrail/{}.json'.format(exe), 'r')
        data = json.load(f)
        if 'message' not in data.keys():
            return data
        else:
            return "Try again later, API at limit for: {}".format(exe)
    except FileNotFoundError:
        return "Could not find: {}".format(exe)

@app.route('/insights')
def insights_route():
    payload = []
    files = os.listdir(os.path.join(os.getcwd(), 'static/echotrail/'))
    for exe in files:
        f = open(os.path.join(os.getcwd(), 'static/echotrail/', exe), 'r')
        data = json.load(f)
        name = re.sub('.json', '', exe)
        if 'message' not in data.keys():
            payload.append(
                {
                    'name' : name,
                    'rank' : data['rank'],
                    'host_prev' : data['host_prev']
                }
            )
        f.close()
    return render_template('insights.html', cmds=payload)

@app.route('/api/insights')
def insights_api_route():
    payload = []
    files = os.listdir(os.path.join(os.getcwd(), 'static/echotrail/'))
    for exe in files:
        f = open(os.path.join(os.getcwd(), 'static/echotrail/', exe), 'r')
        data = json.load(f)
        name = re.sub('.json', '', exe)
        if 'message' not in data.keys():
            payload.append(
                {
                    'name' : name,
                    'rank' : data['rank'],
                    'host_prev' : data['host_prev']
                }
            )
        f.close()
    return payload

@app.route('/api/insights/query', methods=['POST'])
def insights_query_api_route():
    query = request.form['query']
    query = query.lower()
    files = os.listdir(os.path.join(os.getcwd(), 'static/echotrail/'))
    json_query = query+'.json'
    if json_query in files:
        if 'exe' in query:
            return redirect(url_for('search_exe_route', exe=query))
        else:
            return "Could not find: {}".format(query)
    else:
        try:
            output = subprocess.check_output('grep -ir {} static/echotrail/'.format(query), shell=True)
            output = output.decode('utf-8')
            json_file = output.split(':')
            json_file = json_file[0]
            json_file = re.sub('static/echotrail/', '', json_file)
            json_file = re.sub('.json', '', json_file)
            print(json_file)
            
            return redirect(url_for('search_exe_route', exe=json_file))
        except:
            return "Could not find any results for: {}".format(query)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)