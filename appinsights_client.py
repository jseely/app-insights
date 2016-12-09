#!/usr/bin/env python
import requests
import urlparse
import urllib

AI_URLBASE = "https://api.applicationinsights.io/{version}/apps/{appId}/{operation}"

class AppInsightsClient:
    def __init__(self, config):
        if not 'api-key' in config:
            raise Exception('Config missing "api-key" property')
        if not 'app-id' in config:
            raise Exception('Config missing "app-id" property')
        self.apiKey = config['api-key']
        self.appId = config['app-id']

    def metrics(self, metricPath, query):
        url = urlparse.urljoin(AI_URLBASE.format(version='beta', appId=self.appId, operation='metrics'), metricPath, '?' + urllib.quote_plus(query))
        return requests.get(url, headers={"X-Api-Key": self.apiKey}).text

    def query(self, query):
        url = urlparse.urljoin(AI_URLBASE.format(version='beta', appId=self.appId, operation='query'), '?query='+urllib.quote_plus(query))
        return requests.get(url, headers={"X-Api-Key": self.apiKey}).text

    def events(self, eventPath, query):
        url = urlparse.urljoin(AI_URLBASE.format(version='beta', appId=self.appId, operation='events'), eventPath, '?'+urllib.quote_plus(query))
        return requests.get(url, headers={"X-Api-Key": self.apiKey}).text

def main():
    import argparse
    import json
    import os
    import sys

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand_name', help='sub-command help')

    parser_query = subparsers.add_parser('query', help='Query application insights')
    parser_query.add_argument('query_string', help='The query to execute')

    parser_events = subparsers.add_parser('events', help='List events from application insights')
    parser_events.add_argument('event_path', help='The path of the event')
    parser_events.add_argument('query_string', help='The query to filter events')

    parser_metrics = subparsers.add_parser('metrics', help='Get a metric from application insights')
    parser_metrics.add_argument('metric_path', help='The path of the metric')
    parser_metrics.add_argument('query_string', help='The query to filter metrics')
    
    args = parser.parse_args()

    secretsFilepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'secrets.json')
    with open(secretsFilepath) as secretsFile:
        secrets = json.load(secretsFile)

    aic = AppInsightsClient(secrets)
    if args.subcommand_name == 'query':
        print(aic.query(args.query_string))
        sys.exit(0)
    if args.subcommand_name == 'metrics':
        print(aic.metrics(args.metric_path, args.query_string))
        sys.exit(0)
    if args.subcommand_name == 'events':
        print(aic.events(args.event_path, args.query_string))
        sys.exit(0)
    sys.exit(1)

if __name__ == "__main__":
    main()
