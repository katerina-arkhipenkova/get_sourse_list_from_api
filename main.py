import csv
import requests
import json


def get_obi_url(offset, limit):
    url = f'https://test.net/plApi/hubs/api.list/{limit}/{offset}'
    return url


def get_content_from_api(url, params):
    resp = requests.get(url, params=params)
    return resp


def get_source_list_from_api_response(count, offset, limit, params):
    result_list = []
    for i in range(offset, count, limit):
        response = get_content_from_api(get_obi_url(i, limit), params)
        items = response.json().get('response').get('data').get('items')
        for key, val in items.items():
            print(val.get('hub__id'))
            result_list.append([val.get('hub__id'), val.get('ci'), val.get('domain'), val.get('last_message_at')])
    return result_list


def write_csv_file(filename, content, header):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(content)


if __name__ == '__main__':
    source_limit = 3000
    source_offset = 0
    request_params = "access_token="
    csv_header = ('hub__id', 'ci', 'domain', 'last_message_at')

    source_count = get_content_from_api(get_obi_url(source_offset, source_limit),
                                        request_params).json().get('response').get('data').get('info').get('count')

    source_list = get_source_list_from_api_response(source_count, source_offset, source_limit, request_params)

    write_csv_file('sources_list.csv', source_list, csv_header)
