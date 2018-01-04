import json
import webbrowser


offers_html = open('offers.html', 'w')
content = '<html><head></head><body><table>'
data = json.load(open('offers.json'))

content += """
   <tr>
       <th>Dealer name</th>
       <th>Offer url</th>
       <th>Car name</th>
       <th>Price</th>
   </tr>
"""

for dealer in data['dealers']:
    for i, offer in enumerate(dealer['offers']):
        if i == 0:
            offer_rows = '<tr><td>{dealer}</td>'.format(
                dealer=dealer['dealer_name'].encode('utf-8'))
        else:
            offer_rows = '<tr><td></td>'
        offer_rows += '<td>' + offer['offer_url'].encode('utf-8') + '</td>'
        offer_rows += '<td>' + offer['car_name'].encode('utf-8') + '</td>'
        offer_rows += '<td>' + offer['price'].encode('utf-8') + '</td>'
        content += '{offer}</tr>'.format(offer=offer_rows)


content += '</table></body></html>'

offers_html.write(content)
offers_html.close()

webbrowser.open_new_tab('offers.html')
