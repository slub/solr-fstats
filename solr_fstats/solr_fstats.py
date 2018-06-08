#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import csv
import json
import sys

import requests
from sortedcontainers import SortedList

FIELD_NAME = 'field_name'
EXISTING = 'existing'
EXISTING_PERCENTAGE = 'existing_percentage'
NOTEXISTING = 'notexisting'
NOTEXISTING_PERCENTAGE = 'notexisting_percentage'


def get_header():
    return [FIELD_NAME,
            EXISTING,
            EXISTING_PERCENTAGE,
            NOTEXISTING,
            NOTEXISTING_PERCENTAGE]


def solr_request(request, host, port, core):
    response = requests.get(request)

    if response.status_code != 200:
        solr_instance = "http://{:s}:{:d}/solr/".format(host, port)
        raise RuntimeError('Solr core "%s" at solr instance "%s" is not available' % (core, solr_instance))

    response_body = response.content.decode('utf-8')

    return json.loads(response_body)


def get_fields(host, port, core):
    # permutations of dynamic fields are not included in this requests
    # TODO: how to get them?
    schema_request = "http://{:s}:{:d}/solr/{:s}/schema?wt=json".format(host, port, core)

    schema = solr_request(schema_request, host, port, core)

    if "schema" not in schema and "fields" not in schema['schema']:
        raise RuntimeError('something went wrong, while requesting the schema from "%s", got response "%s"' % (
            schema_request, schema))

    fields = schema['schema']['fields']

    return [(field['name']) for field in fields]


def get_records_total(host, port, core):
    total_request = "http://{:s}:{:d}/solr/{:s}/select?q=*%3A*&rows=0&wt=json".format(host, port, core)

    response_json = solr_request(total_request, host, port, core)

    if "response" not in response_json and "numFound" not in response_json['response']:
        raise RuntimeError(
            'something went wrong, while requesting the total number of records from "%s", got response "%s"' % (
                total_request, response_json))

    return response_json['response']['numFound']


def get_field_total(field, host, port, core):
    total_request = "http://{:s}:{:d}/solr/{:s}/select?q=*%3A*&fq={:s}%3A%5B*+TO+*%5D&rows=0&wt=json".format(host, port,
                                                                                                             core,
                                                                                                             field)

    response_json = solr_request(total_request, host, port, core)

    if "response" not in response_json and "numFound" not in response_json['response']:
        raise RuntimeError(
            'something went wrong, while requesting the total number field "%s" existing in the records from "%s", got response "%s"' % (
                field, total_request, response_json))

    return response_json['response']['numFound']


def get_field_statistics(field, host, port, core, records_total):
    field_total = get_field_total(field, host, port, core)
    field_total_percentage = (float(field_total) / float(records_total)) * 100

    return (field_total,
            "{0:.2f}".format(field_total_percentage))


def get_all_field_statistics(field, host, port, core, records_total):
    field_stats = get_field_statistics(field, host, port, core, records_total)
    field_neg_stats = get_field_statistics("-{:s}".format(field), host, port, core, records_total)

    return {FIELD_NAME: field,
            EXISTING: field_stats[0],
            EXISTING_PERCENTAGE: field_stats[1],
            NOTEXISTING: field_neg_stats[0],
            NOTEXISTING_PERCENTAGE: field_neg_stats[1]}


def csv_print(field_statistics):
    header = get_header()
    with sys.stdout as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header, dialect='unix')

        writer.writeheader()
        for field_statistic in field_statistics:
            writer.writerow(field_statistic)


def run():
    parser = argparse.ArgumentParser(prog='solr-fstats',
                                     description='returns field statistics of a Solr index; prints the output as pure CSV data (all values are quoted) to stdout',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    optional_arguments = parser._action_groups.pop()

    required_arguments = parser.add_argument_group('required arguments')
    required_arguments.add_argument('-core', type=str, help='Solr core to use', required=True)

    optional_arguments.add_argument('-host', type=str, default='localhost',
                                    help='hostname or IP address of the Solr instance to use')
    optional_arguments.add_argument('-port', type=int, default=8983,
                                    help='port of the Solr instance to use')

    parser._action_groups.append(optional_arguments)

    args = parser.parse_args()

    fields = SortedList(get_fields(args.host, args.port, args.core))
    total = get_records_total(args.host, args.port, args.core)

    stats = [(get_all_field_statistics(field, args.host, args.port, args.core, total)) for field in fields]

    csv_print(stats)


if __name__ == "__main__":
    run()
