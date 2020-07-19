import os
import psycopg2

def curse():
	DATABASE_URL = "postgres://ezghcmygmrbrop:7abb507396ab2deed0bf71385f603882588df832a37fd299a66ee920d63f1402@ec2-3-215-83-17.compute-1.amazonaws.com:5432/d6k2a3ik6vinao"
	conn = psycopg2.connect(DATABASE_URL,sslmode='require')

	cur = conn.cursor()
	conn.autocommit = True
	return (cur,conn)


def insert_ingred_info(in_dict,cur,conn):
	if type(in_dict) is not dict:
		raise TypeError

	column_names = ["ingred_name","ingred_source","score"]

	orig_keys = in_dict.keys()

	for col in column_names:
		if col not in orig_keys:
			in_dict[col]=None

	try:
		cur.execute("""INSERT INTO ingredients (ingred_name, ingred_source, score)
VALUES (%(ingred_name)s,%(ingred_source)s,%(score)s);""", in_dict)
	except psycopg2.errors.UniqueViolation:
		"boohooo"
	except psycopg2.errors.NotNullViolation:
		print(f"not null violation for brand_dict for brand {brand}")
	
	return 200

def insert_brand_info(in_dict,cur,conn):
	if type(in_dict) is not dict:
		raise TypeError

	column_names = ["brand_name","owner_company","echo","cdpA","fair_trade","nonGMO","RA","organic_operation_ID"]

	orig_keys = in_dict.keys()

	for col in column_names:
		if col not in orig_keys:
			in_dict[col]=None

	cur.execute("""INSERT INTO brands (brand_name, owner_company,
echo, cdpA , fair_trade , nonGMO , RA, organic_operation_ID)
VALUES (%(brand_name)s,%(owner_company)s,%(echo)s,%(cdpA)s,%(fair_trade)s,
%(nonGMO)s,%(RA)s,%(organic_operation_ID)s);""", in_dict)
	
	return 200

def brand_info(brand,cur,conn):

	class BrandRow:
		def __init__(self,row_list):
			self.row_dict = {}
			self.row_dict["brand_name"] = row_list[0]
			self.row_dict["owner_company"] = row_list[1]
			self.row_dict["echo"] = row_list[2]
			self.row_dict["cdpA"] = row_list[3]
			self.row_dict["fair_trade"] = row_list[4]
			self.row_dict["nonGMO"] = row_list[5]
			self.row_dict["RA"] = row_list[7]
			self.row_dict["rainforest alliance"] = row_list[7]
			self.row_dict["organic_operation_ID"] =row_list[6]

		def print_row(self):
			for key in self.row_dict.keys():
				print(key+" ----------- "+str(self.row_dict[key]))
	cur.execute(f"SELECT * FROM brands WHERE brand_name=%s",(brand,))
	all_rows = cur.fetchall()
	if len(all_rows)==0:
		return None
	return BrandRow(all_rows[0])



def ingred_info(ingred,cur,conn):

	class IngredRow:
		def __init__(self,row_list):
			self.row_dict = {}
			self.row_dict["ingred_name"] = row_list[0]
			self.row_dict["ingred_source"] = row_list[1]
			self.row_dict["score"] = row_list[2]
		def print_row(self):
			for key in self.row_dict.keys():
				print(key+" ----------- "+str(self.row_dict[key]))
	cur.execute("SELECT * FROM ingredients WHERE ingred_name=%s",(ingred,))
	all_rows = cur.fetchall()
	if len(all_rows)==0:
		return None
	return IngredRow(all_rows[0])

def delete_brand(brand,cur,conn):
	cur.execute("DELETE FROM brands WHERE brand_name=%s",(brand,))
	



"""
cur,conn = curse()
for key in result.keys():
	in_dict = {"ingred_name":key}
	value = result[key]
	if value=="N/A":
		insert_ingred_info(in_dict,cur,conn)
	else:
		parts = str(value).split(",")
		in_dict["score"] = parts[0].strip()
		in_dict["ingred_source"] = parts[1].strip()
		insert_ingred_info(in_dict,cur,conn)

"""

