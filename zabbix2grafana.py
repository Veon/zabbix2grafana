#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import requests
import json
import sys
import os

config = ""

parser = argparse.ArgumentParser(prog='zabbix2grafana')
parser.add_argument('-c', '--config', type=str, help="Path to config file", default="./config.yml", required=True)
parser.add_argument('-id', '--screen_id', type=int, help="Zabbix screen ID", required=True)
parser.add_argument('-up', '--update', action='store_true', help="Delete dashboard before create - update")
args = parser.parse_args()
print args
if args.screen_id != None:
    zabbix_screen_id = args.screen_id
else:
    exit("Zabbix screen ID is 'None'")
if os.path.isfile(args.config):
    config_file = args.config
else:
     exit("Wrong config file")

def read_config(config_file):
    file = open(config_file, "r")
    jsonc = file.read()
    return json.loads(jsonc)

def get_zabbix_key():
    r = requests.post(zabbix_api_url, data=auth_query, headers=headers)

    if r.status_code == 200:
        print "Connection OK, getting api key..."
    else:
        exit("Connection FAILED")

    return json.loads(r.content)['result']

execfile('templates.py')

config = read_config(config_file)
headers = {'Content-Type': 'application/json'}
headers_grafana = {'Content-Type': 'json', 'Authorization': 'Bearer ' + config['grafana']['api_key']}
zabbix_api_url = config['zabbix']['url'] + "/api_jsonrpc.php"
auth_query = '{ "jsonrpc": "2.0", "method": "user.login", "params": { "user": "' + config['zabbix']['login'] + '", "password": "' + config['zabbix']['password'] + '"},"id":1}'

api_key = get_zabbix_key()
print "API Key: " + api_key

r = requests.get(zabbix_api_url, data=get_screen.replace('AUTH_KEY', api_key), headers=headers)

screen = json.loads(r.content)['result'][0]
screen_name = json.loads(r.content)['result'][0]['name'].replace(' ', '_')

if args.update == True:
    r = requests.delete(config['grafana']['url'] + "/api/dashboards/db/" + screen_name, data=result_json, headers=headers_grafana)

result_json = result_json.replace('SCREEN_ID', 'null')
result_json = result_json.replace('DASHBOARD_NAME', screen_name)
graph_count = len(screen['screenitems'])
counter = 1
rows_count = graph_count / 4

print "Graph count: " + str(graph_count)
print "Generating JSON..."

for graph_item in range (0, graph_count):
    metrics_count = 0;
    metric_name = ""

    graph_id = screen['screenitems'][graph_item]['resourceid']

    get_graph = get_graph.replace('AUTH_KEY', api_key)
    get_graph_json = get_graph.replace('GRAPH_ID', graph_id)
    r_graph = requests.get(zabbix_api_url, data=get_graph_json, headers=headers)

    host_id = json.loads(r_graph.content)['result'][0]['items'][0]['hostid']

    get_host = get_host.replace('AUTH_KEY', api_key)
    get_host_json = get_host.replace('HOST_ID', host_id)
    r_host = requests.get(zabbix_api_url, data=get_host_json, headers=headers)

    metrics_count = len(json.loads(r_graph.content)['result'][0]['items'])

    host_name = json.loads(r_host.content)['result'][0]['name']
    host_group = json.loads(r_host.content)['result'][0]['groups'][0]['name']

    if counter == graph_count:
        result_json = result_json + panel_tpl.replace('_BRACKET_','}').replace('TMP_HOST', host_name).replace('PANEL_ID', str(counter)) \
                                                    .replace('_PANEL_TITLE_', host_name + ' - ' + json.loads(r_graph.content)['result'][0]['name'])
    elif counter == 1:
        result_json = result_json + panel_tpl.replace('_BRACKET_','},').replace('TMP_HOST', host_name).replace('PANEL_ID', str(counter)) \
                                                    .replace('_PANEL_TITLE_', host_name + ' - ' + json.loads(r_graph.content)['result'][0]['name'])
    elif counter%rows_count == 0:
        result_json = result_json + panel_tpl.replace('_BRACKET_','}') .replace('TMP_HOST', host_name).replace('PANEL_ID', str(counter)) \
                                                    .replace('_PANEL_TITLE_', host_name + ' - ' + json.loads(r_graph.content)['result'][0]['name'])
        result_json = result_json + '''
                ],
                "title": "Row"
            }, { "collapse": false,
                "editable": true,
                "height": "250px",
                "panels": [
            '''
    else:
        result_json = result_json + panel_tpl.replace('_BRACKET_','},').replace('TMP_HOST', host_name).replace('PANEL_ID', str(counter)) \
                                                    .replace('_PANEL_TITLE_', host_name + ' - ' + json.loads(r_graph.content)['result'][0]['name'])

    counter += 1

    i = 0
    target_json = ""
    for metric_item in range(0,metrics_count):
        metric_name = json.loads(r_graph.content)['result'][0]['items'][metric_item]['name']
        data = [host_name, host_group, metric_name]

        target_json = target_json + target_tpl.replace('HOST_NAME', host_name) \
                                        .replace('HOST_GROUP', host_group) \
                                        .replace('METRIC', metric_name)
        if i != metrics_count - 1:
            target_json = target_json.replace('_BRACKET_', '},')
        else:
            target_json = target_json.replace('_BRACKET_', '}')

        i += 1

        if i%metrics_count == 0:
           result_json = result_json.replace('_TARGETS_' + host_name + '_', target_json)

result_json = result_json + footer_tpl

print result_json

r = requests.post(config['grafana']['url'] + "/api/dashboards/db", data=result_json, headers=headers_grafana)

response = "\nResult\nHTTP code: " + str(r.status_code) + ",\nHTTP response: " +  r.content

print response
