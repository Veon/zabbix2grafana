result_json='''{
    "dashboard": {
        "id": SCREEN_ID,
        "title": "DASHBOARD_NAME",
        "version": 12,
        "schemaVersion": 15,
        "originalTitle": "New dashboard",
        "overwrite": true,
        "timezone": "browser",
        "rows": [{
            "collapse": false,
            "editable": true,
            "height": "250px",
            "panels": [
'''
get_screen = '''{
    "jsonrpc": "2.0",
    "method": "screen.get",
    "params": {
        "output": "extend",
        "selectScreenItems": "extend",
        "selectUsers": "extend",
        "selectUserGroups": "extend",
        "screenids": "''' + str(zabbix_screen_id) + '''",
        "sortfield": "screenid"
    },
    "auth": "AUTH_KEY",
    "id": 1
}'''
get_graph = '''{
    "jsonrpc": "2.0",
    "method": "graph.get",
    "params": {
        "output": "extend",
        "graphids": GRAPH_ID,
        "sortfield": "name",
        "selectItems": "extend"
    },
    "auth": "AUTH_KEY",
    "id": 1
}'''
get_host = '''{
    "jsonrpc": "2.0",
    "method": "host.get",
    "params": {
        "output": "extend",
        "hostids": "HOST_ID",
        "selectGroups": "extend"
    },
    "auth": "AUTH_KEY",
    "id": 1
}'''
panel_tpl='''
{
                        "title": "_PANEL_TITLE_",
                        "id": PANEL_ID,
                        "legend": {
                            "alignAsTable": true,
                            "avg": false,
                            "current": false,
                            "max": false,
                            "min": false,
                            "show": true,
                            "total": false,
                            "values": false
                        },
                        "type": "graph",
                        "lines": true,
                        "linewidth": 1,
                        "nullPointMode": "null",
                        "percentage": false,
                        "pointradius": 5,
                        "points": false,
                        "renderer": "flot",
                        "seriesOverrides": [],
                        "span": 3,
                        "stack": false,
                        "steppedLine": false,
                        "targets": [
                            _TARGETS_TMP_HOST_
                        ],
                        "xaxis": {
                            "mode": "time",
                            "name": null,
                            "show": true,
                            "values": []
                        },
                        "yaxes": [
                            {
                                "format": "decbytes",
                                "label": null,
                                "logBase": 1,
                                "max": null,
                                "min": null,
                                "show": true    
                            },
                            {
                                "format": "short",
                                "label": null,
                                "logBase": 1,
                                "max": null,
                                "min": null,
                                "show": true
                            }
                        ]
                    _BRACKET_'''

target_tpl = '''
                            {
                                "application": {
                                    "filter": ""
                                },
                                "functions": [],
                                "group": {
                                    "filter": "HOST_GROUP"
                                },
                                "host": {
                                    "filter": "HOST_NAME"
                                },
                                "item": {
                                    "filter": "METRIC"
                                },
                                "mode": 0,
                                "options": {
                                    "showDisabledItems": false
                                },
                                "refId": "A"
                    _BRACKET_                            
'''
footer_tpl='''],
        "title": "Row"
            }
        ],
        "time": {
            "from": "now-1h",
            "to": "now"
        },
        "timepicker": {
            "refresh_intervals": [
            "5s",
            "10s",
            "30s",
            "1m",
            "5m",
            "15m",
            "30m",
            "1h",
            "2h",
            "1d"
        ],
        "time_options": [
            "5m",
            "15m",
            "1h",
            "6h",
            "12h",
            "24h",
            "2d",
            "7d",
            "30d"
        ]
        }
    }
}'''

