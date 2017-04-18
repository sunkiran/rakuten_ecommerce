"""
python process_data.py ../data/bag_desc/ ../data/bag_sales.txt
"""
import pandas as pd
import sys
import os
import math
import re


desc_dir = sys.argv[1]
desc_type = os.path.basename(os.path.normpath(desc_dir)).replace('_', '.') + '.'
category = desc_type.split('.')[0]
sales_filepath = sys.argv[2]

inputs = ''
outputs = ''

sales = pd.read_csv(sales_filepath, sep='\t')
skipped = 0
for item_id, sales in zip(sales.item_id, sales.unit_sales):
    description_file = os.path.join(desc_dir, desc_type + item_id)
    description = open(description_file).read().split('\t')
    if len(description) != 11: 
        skipped += 1
        continue
    [item_title, item_id, price, description1, description2, _, img_url, num_reviews, avg_rating, shop_name, category_id] = \
        description
    # todo - title and description as seperate inputs?
    item_description = re.sub('\s+', ' ', item_title + ' ' + description1 + ' ' + description2).strip()

    inputs += item_description + '\n'
    outputs += '%s|%s|%s|%s\n' % (str(math.log(float(sales + 0.00001))), shop_name, price, category)


with open(category + '.inputs', 'w') as f:
    f.write(inputs)
with open(category + '.outputs', 'w') as f:
    f.write(outputs)



