import requests
import json

# owner, database = 'dolthub', 'ip-to-country'
# res = requests.get('https://dolthub.com/api/v1alpha1/{}/{}'.format(owner, database))
# print(str(res.json()))


# query = '''SELECT * FROM IPv4ToCountry WHERE CountryCode2Letter = "AU"'''
# res = requests.get(
#   'https://www.dolthub.com/api/v1alpha1/{}/{}'.format(owner, database),
#   params={'q': query},
#   )
# r = res.json()
# print(str(r))

# SELECT league, `date`, day, `time`, home_team, road_team, location 
query = '''
SELECT * 
FROM `combined-schedule`
WHERE home_state IN ("NJ")
AND `date` >= CURDATE() AND `date` <= DATE_ADD(CURDATE(), INTERVAL 2 DAY)
ORDER BY `date`, `time` ASC
'''

owner, database = 'gmichnikov', 'sports-schedules'
res = requests.get(
  'https://www.dolthub.com/api/v1alpha1/{}/{}'.format(owner, database),
  params={'q': query},
  )
json_result = res.json()
print(json_result.keys())

formatted_json = json.dumps(json_result["rows"], indent=4)
print(formatted_json)

# https://www.dolthub.com/api/v1alpha1/gmichnikov/sports-schedules/main?q=SELECT+league%2C+%60date%60%2C+day%2C+%60time%60%2C+home_team%2C+road_team%2C+location+%0AFROM+%60combined-schedule%60%0AWHERE+home_state+IN+%28%22NY%22%2C+%22NJ%22%29%0AAND+%60date%60+%3E%3D+CURDATE%28%29+AND+%60date%60+%3C%3D+DATE_ADD%28CURDATE%28%29%2C+INTERVAL+7+DAY%29%0AORDER+BY+%60date%60%2C+%60time%60+ASC%0A