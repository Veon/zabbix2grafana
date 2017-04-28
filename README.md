# zabbix2grafana
Migrate screens from zabbix to grafana

Take screen ID, create dashboard in grafana with zabbix screen name

The order of charts is not copied

Скрипт для переноса комплексных экранов из заббикса в графану

Принимает ID экрана, создает dashboard в графане с именем экрана.

Порядок графиков в экране не повторяется

Config example:

{
    "zabbix": {
        "url": "http://zabbix.example.com",
        "login": "LOGIN",
        "password": "PASSWORD"
    },
    "grafana": {
        "url": "http://zabbix.example.com:3000",
        "api_key": "GRAFANA_KEY"
    }
}
