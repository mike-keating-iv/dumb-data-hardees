###scrape_hardees.py - Scrape the web for addresses of every Hardees Location
###
# Import Modules
import bs4, requests, pandas as pd


#Hardee's All Locations Url (By State)
url = 'https://locations.hardees.com/'
res = requests.get(url)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')

#Initialize empty lists for street address, city, state, and zip
street_add_list = []
city_list = []
state_list = []
postal_code_list = []

stateElems = soup.select('.Directory-listLink')
for i in range(len(stateElems)):
    state_link = stateElems[i].get('href')
    # Make new request for each state link
    res2 = requests.get(state_link)
    res2.raise_for_status()
    soup2 = bs4.BeautifulSoup(res2.text, 'html.parser')
    print('Downloading from', state_link,'...')

    # Store each location link for each state
    locElems = soup2.select('.Directory-listLink')
    for j in range(len(locElems)):
        loc_link = locElems[j].get('href')
        print(loc_link)

        # Make new request for each location link
        res3 = requests.get(loc_link)
        res3.raise_for_status()
        soup3 = bs4.BeautifulSoup(res3.text, 'html.parser')
        # Extract and add to llist address, city, state, postal code of each location
        street_add = soup3.select('.c-address-street-1')
        city = soup3.select('.c-address-city')
        state = soup3.select('.c-address-state')
        postal_code = soup3.select('.c-address-postal-code')
        for i in range(len(street_add)):  
            street_add_list.append(street_add[i].get_text())
            city_list.append(city[i].get_text())
            state_list.append(state[i].get_text())
            postal_code_list.append(postal_code[i].get_text())
        
print('Hardees Extraction Complete')

##Create empty dataframe
hardees = pd.DataFrame(columns = ['location_id', 'street_address', 'city', 'state', 'postal_code', 'restaurant'])

# Assign data
hardees['street_address'] = street_add_list
hardees['city'] = city_list
hardees['state'] = state_list
hardees['postal_code'] = postal_code_list
hardees['restaurant'] = 'HD'

# Give each restaurant a unique id
n = 1
for i in range(len(street_add_list)):
    hardees['location_id'][i] = f'HD-{n}'
    n += 1

# Save csv    
hardees.to_csv('hardees.csv', index=False)



