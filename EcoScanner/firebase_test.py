from firebase import firebase
#from testing_database import *

fb_connect = firebase.FirebaseApplication("https://ecoscanner-cb66d.firebaseio.com/",None)

result = fb_connect.get("/evaluated",None)

print(result)

"""del result["scan_log"]

brand_Fair_trade = result["brand-Fair Trade"]
brand_RA = result["brand-RA"]
brand_comp = result["brand-comp"]
brand_opID = result["brand-opID"]
ingredient_scores = result["ingredient scores"]

huge_list = [brand_Fair_trade,brand_RA,brand_comdp,brand_opID]

def is_in_all(brand):
	for dictionary in huge_list:
		if brand not in dictionary.keys():
			return False
	return True

def in_most(brand):
	count = 0
	for dictionary in huge_list:
		if brand in dictionary.keys():
			count+=1
	if count>=2:
		return True
	else:
		return False



ft_keys = brand_Fair_trade.keys()
count = 0
for key in ft_keys:
	if in_most(key):
		count+=1
		print(key)

cur,conn = curse()
conn.autocommit = True

index_to_key = {0:"fair_trade",1:"RA",2:"owner_company",3:"organic_operation_ID"}

done_brands = []

for dictionary in huge_list:
	for brand in dictionary.keys():
		if brand not in done_brands:
			brand_dict = {"brand_name":brand}
			done_brands.append(brand)
			print(brand.upper())
			for dictionary in huge_list:
				key_to_be = index_to_key[huge_list.index(dictionary)]
				try:
					brand_dict[key_to_be] = dictionary[brand]

				except KeyError:
					brand_dict[key_to_be] = None
					print(f"Key error on key_to_be {key_to_be} while creating brand_dict {brand}")
			try:
				insert_brand_info(brand_dict,cur,conn)
			except psycopg2.errors.NotNullViolation:
				print(f"not null violation for brand_dict for brand {brand}")
			except psycopg2.errors.UniqueViolation:
				print(f"Unique Violation for brand_dict for brand {brand}")


cur.close()
conn.close()


print(count/len(ft_keys))
"""

