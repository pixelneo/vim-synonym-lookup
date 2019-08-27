#!/usr/bin/env python3

def synoms():
    import vim, requests, json, os, builtins
    class mydict(dict):
        def set_from(self, key, dict2, key2):
            '''
                Sets a value from `dict2[key2]` to `key` if `key2` exists in dict2, otherwise does nothing.
            '''
            if k2 in dict2.keys():
                self[key] = dict2[key2]

        def set_from_string(self, key, dict2, key2):
            '''
                Sets a concatenation of values from `dict2[key2]` to `key` if `key2` exists in dict2, otherwise does nothing.
            '''
            if k2 in dict2.keys():
                self[key] = ', '.join(dict2[key2])

    builtins.dict = mydict

    def _get_my_key():
        plugin_root_dir = vim.eval('s:plugin_root_dir')
        file = os.path.normpath(os.path.join(plugin_root_dir, '..', 'data', 'my-key'))
        try:
            with open(file, 'r') as f:
                key = f.read()
        except FileNotFoundError as e:
            print('Synom ERROR: File with API key not found')
            exit()
        return str(key.strip())

    def _get_current_word():
        return vim.eval("expand(\"<cword>\")")

    def _get_data_from_server(word, what=''):
        headers = {}
        headers['x-rapidapi-host'] = 'wordsapiv1.p.rapidapi.com'
        headers['x-rapidapi-key'] = _get_my_key()
        url = 'https://wordsapiv1.p.rapidapi.com/words/{}/{}'.format(word, what)
        try:
            with requests.request('GET', url, headers=headers) as resp:
                data = resp.text
        except requests.exceptions.RequestException as e:
            print('Synom ERROR: Error occured when retrieving data from Words API server')
            exit()
        obj = json.loads(data)
        return obj 

    def _get_synoms(word):
        obj = _get_data_from_server(word, 'synonyms')
        if obj is not None and isinstance(obj, dict) and 'synonyms' in obj.keys():
            return ', '.join(obj['synonyms'])
        else:
            return '--- No synonyms ---'

    def _get_it_all(word):
        out_list = dict() 
        obj = _get_data_from_server(word)
        if obj is not None and isinstance(obj, dict) and isinstance(obj['results'], list):

            out_list['word'] = obj['word']      # add searched word
            out_list['meanings'] = []

            for meaning in obj['results']:
                x = dict() 
                x.set_from('def', meaning, 'definition')
                x.set_from('pos', meaning, 'partOfSpeech')
                x.set_from_string('synonyms', meaning, 'synonyms')
                x.set_from_string('derivation', meaning, 'derivation')
                x.set_from_string('examples', meaning, 'examples')
                out_list['meanings'].append(x)

            mns = '\n------------------------\n'.join([meaning for meaning in out_list['meanings'])
            result = '{}: {}\n{}'.format('Word', out_list['word'], mns)





        else:
            return '--- Error when parsin response ---'
            

    # print(_get_synoms(_get_current_word()))
    vim.command("set buftype=nofile")
    vim.command("pedit! /tmp/Synom-temp-file")
