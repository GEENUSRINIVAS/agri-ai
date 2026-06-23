import json, os
langs = ['en', 'te', 'hi', 'ta', 'kn']
required = ['overview_title', 'overview_stat_model', 'overview_quick_title',
            'topbar_overview', 'topbar_prediction', 'sidebar_main_menu', 'mkt_btn']
for lang in langs:
    path = os.path.join('static', 'lang', lang + '.json')
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    missing = [k for k in required if k not in data]
    status = 'OK (' + str(len(data)) + ' keys)' if not missing else 'MISSING: ' + str(missing)
    print(lang + '.json: ' + status)
