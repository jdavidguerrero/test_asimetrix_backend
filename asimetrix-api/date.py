from datetime import datetime
'''


dt_obj = datetime.strptime('21.10.2021',
                           '%d.%m.%Y')
millisec = dt_obj.timestamp() * 1000

dt_obj = datetime.strptime('22.10.2021',
                           '%d.%m.%Y'
                           '''

dt_obj = datetime.strptime('22-10-2021',
                           '%d-%m-%Y')

millisec = dt_obj.timestamp() * 1000
print(millisec)