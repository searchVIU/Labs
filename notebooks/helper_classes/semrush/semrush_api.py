
import os, sys
import requests
import logging
import json
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
import csv
import io
import os.path

class SEMRushAPI():


    def __init__(self, api_key, api_url='http://api.semrush.com/'):
        self.api_key = api_key
        self.api_url = api_url
        self.cache_dir = './semrush_cache/'
        if self.api_key == '':
            print("Error: Valid SEMrush API Key needed.")
        pass


    def get_domain_overview(self, domain, count=1):
        rtype = 'domain_ranks'
        query_data = {'type': rtype,
                      'domain': domain,
                      'database': 'de',
                      'export_columns': 'Db,Dn,Rk,Or,Ot,Oc,Ad,At,Ac,Sv,Sh',
                      'export_escape': 1,
                      'display_limit': count}
        return self.sem_request(query_data)


    def get_domain_keywords(self, domain, result_type='organic', count=1):
        if result_type=='paid':
            rtype = 'domain_adwords'
        else:
            rtype = 'domain_organic'
        query_data = {'type': rtype,
                      'domain': domain,
                      'database': 'de',
                      'export_columns': 'Ph, Po, Pp, Pd, Nq, Cp, Ur, Tr, Tc, Co, Nr, Td	',
                      'export_escape': 1,
                      'display_limit': count}
        return self.sem_request(query_data)

    def get_keyword_data(self, keyword, count=1):
        rtype = 'phrase_this'
        query_data = {'type': rtype,
                      'phrase': keyword,
                      'database': 'de',
                      'export_columns': 'Ph,Nq,Cp,Co,Nr',
                      'export_escape': 1,
                      'display_limit': count}
        return self.sem_request(query_data)

    def get_results_for_keyword(self, keyword, result_type='organic', count=1):
        if result_type=='paid':
            rtype = 'phrase_adwords'
        else:
            rtype = 'phrase_organic'
        query_data = {'type': rtype,
                      'phrase': keyword,
                      'database': 'de',
                      'export_columns': 'Dn,Ur',
                      'export_escape': 1,
                      'display_limit': count}
        result = self.sem_request(query_data)
        pos = 1
        ret_arr = []
        for item in result:
            item["Position"] = pos
            pos += 1
            ret_arr.append(item)
        return ret_arr

    def sem_request(self, query_data=None):
        cres = self.get_request(query_data)
        if cres is None:
            url = "{}".format(self.api_url)
            query_data["key"] = self.api_key
            result = requests.get(url, params=query_data)
            if result.status_code != 200:
                print("Error reaching SEMrush API")
                return None
            if result.text.startswith("ERROR"):
                print("SEMrush API ERROR: {}".format(result.text))
                return None
            result_body = self.gen_obj_from_csv(result.text)
            self.save_request(query_data, result_body)
        else:
            result_body = cres
        return result_body

    def save_request(self, query_data, data_obj):
        file = self.get_cache_filename(query_data)
        if not os.path.exists(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file))
        with open(file, 'w') as outfile:
            json.dump(data_obj, outfile)
        return True

    def get_request(self, query_data):
        file = self.get_cache_filename(query_data)
        if os.path.isfile(file):
            #logging.info("Entry exists")
            with open(file) as data_file:
                data = json.load(data_file)
            return data
        else:
            #logging.info("Entry exists not")
            return None

    def gen_obj_from_csv(self, csv_content):
        reader_list = []
        reader = csv.DictReader(io.StringIO(csv_content), delimiter=';', quotechar='"')
        for row in reader:
            reader_list.append(dict(row))
        return reader_list

    def get_cache_filename(self, query_data):
        str_arr = []
        kw_val = ''
        type_val = ''
        for key,val in query_data.items():
            good_val = self.make_filename_str(val)
            if key == 'phrase':
                kw_val = good_val
            elif key == 'type':
                type_val = good_val
            elif key == 'key' or key == 'export_escape':
                pass
            else:
                str_arr.append(good_val)
        str_arr.sort()

        return "{}{}/{}/{}.json".format(self.cache_dir, type_val, "-".join(str_arr), kw_val)

    def make_filename_str(self, _unistr):
        remove_punctuation_map = dict((ord(char), None) for char in '\/*?:"<>|')
        return str(_unistr).translate(remove_punctuation_map)