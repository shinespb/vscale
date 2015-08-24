#!/usr/bin/env python
#coding: utf-8

import requests
import json as json_module

API_ENDPOINT = 'https://api.vscale.io'

class DoError(RuntimeError):
    pass

class Vscale(object):

    def __init__(self, client_id, api_key, api_version=1):
        self.api_endpoint = API_ENDPOINT
        self.api_key = api_key
        self.api_version = int(api_version)
        self.api_endpoint += '/v1'

    def scalets_list(self):
        json = self.request('/scalets')
        return json

    def scalet_start(self, scalet_id):
        json = self.request('/scalets/%s/start' % scalet_id, method='PATCH')
        return json['status']

    def scalet_stop(self, scalet_id):
        json = self.request('/scalets/%s/stop' % scalet_id, method='PATCH')
        return json['status']


    def scalet_create(self, name, password, plan, image, location, keys=None, autostart=True,):
        params = {
            'name': str(name),
            'password': str(password),
            'rplan': str(plan),
            'make_from': str(image),
            'do_start': bool(autostart),
            'location': str(location),
        }
        if keys:
            if type(keys) == list:
                params['keys'] = keys

        json = self.request('/scalets', params, method='POST')

        return json

    def scalet_delete(self, scalet_id):
        json = self.request('/scalets/%s' % scalet_id, method='DELETE')
        return json
    # get locations list
    def location_list(self):
        json = self.request('/locations')
        return json

    # get list of images
    def images_list(self):
        json = self.request('/images')
        return json

    # get list of ssh keys
    def sshkey_list(self):
        json = self.request('/sshkeys')
        return json

    def sshkey_add(self, keyname, pubkey):
        params = {"name": keyname, "key": pubkey}
        json = self.request('/sshkeys', params, method='POST')
        return json

    def sshkey_delete(self, key_id):
        json = self.request('/sshkeys/%s' % key_id, method='DELETE')
        return json

    def request(self, path, params={}, method='GET'):
        headers={}
        if not path.startswith('/'):
            path = '/'+path
        url = self.api_endpoint+path

        headers['X-Token'] = self.api_key
        resp = self.request_v1(url, headers, params, method=method)

        return resp

    def request_v1(self, url, headers={}, params={}, method='GET'):
        headers['Content-Type'] = 'application/json'
        try:
            if method == 'POST':
                resp = requests.post(url, data=json_module.dumps(params), headers=headers, timeout=60)
                print('Headers: {}. Params: {}'.format(headers, json_module.dumps(params)))
                json = resp.json()
            elif method == 'DELETE':
                resp = requests.delete(url, headers=headers, timeout=60)
                json = {'status': resp.status_code}
            elif method == 'PUT':
                resp = requests.put(url, headers=headers, params=params, timeout=60)
                json = resp.json()
            elif method == 'PATCH':
                resp = requests.patch(url, headers=headers, params=params, timeout=60)
                json = resp.json()
            elif method == 'GET':
                resp = requests.get(url, headers=headers, params=params, timeout=60)
                json = resp.json()
            else:
                raise DoError('Unsupported method %s' % method)

        except ValueError:
            raise ValueError("The API server doesn't respond with a valid json")
        except requests.RequestException as e:
            raise RuntimeError(e)

        if resp.status_code != requests.codes.ok:
            if resp.headers:
                if 'vscale-error-message' in resp.headers:
                    raise DoError(resp.headers['vscale-error-message'])
            resp.raise_for_status()

        return json        

if __name__ == '__main__':
    import os
    api_token = os.environ['API_KEY']
    do = Vscale(None, api_token, 2)
    import sys
    fname = sys.argv[1]
    import pprint
    pprint.pprint(getattr(do, fname)(*sys.argv[2:]))
