import os
import psycopg2
import firebase

#fb_connect = firebase.FirebaseApplication("https://ecoscanner-cb66d.firebaseio.com/",None)

#fb_connect.get("brands")

def curse():
	DATABASE_URL = "postgres://kdjrttwrzylfcb:0634afc6c9ed6e34273cabdca2c5961d7c2520eff7e3983659b3d2dbe09ce1ad@ec2-52-70-15-120.compute-1.amazonaws.com:5432/d4pdg2cp43r897"
	conn = psycopg2.connect(DATABASE_URL,sslmode='require')

	cur = conn.cursor()
	conn.autocommit = True
	return (cur,conn)



#cur.execute("CREATE TABLE brands (brand_name varchar PRIMARY KEY, owner_company varchar, echo real , cdpA real, fair_trade real, nonGMO real, organic_operation_ID varchar);")
#cur.execute("INSERT INTO test (name,dob,address) VALUES (%s,%s,%s)",("Aman","05/09/2002","1084 Zamora Ct."))
#cur.execute("SELECT * FROM test;")
#cur.execute("CREATE TABLE ingredients (ingred_name varchar PRIMARY KEY, ingred_source varchar , score varchar);")
#cur.execute("CREATE TABLE barcodes (upc integer PRIMARY KEY, product_name varchar, brand_name varchar, organic_info varchar, pre_score real, ingredient_score real , dangerous_ingredients varchar, eco_score smallint);")

'''cur.execute("""INSERT INTO brands (brand_name, owner_company,
echo, cdpA , fair_trade , nonGMO , organic_operation_ID)
VALUES (%s,%s,%s,%s,%s,%s,%s);""" , ("trial","trialowner","-2.00","1","1","1","489349823094"))'''

#cur.execute("ALTER TABLE brands ADD RA real;")

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


#sample_in_dict = {"brand_name":"trial4","owner_company":"trial4_owner",
#"echo":-1.5,"cdpA":2,"fair_trade":0,"nonGMO":0,"RA":1,"organic_operation_ID":"43209240920"}

#insert_brand_info(sample_in_dict)

#cur,conn = curse()

#content_dict = {"brand_name":"Annie's","owner_company":"General Mills",
#"echo":None,"cdpA":None,"fair_trade":None,"nonGMO":None,"RA":None,"organic_operation_ID":"8150000067"}


#cur.execute("""INSERT INTO brands (brand_name,owner_company,organic_operation_ID)
#	VALUES (%(brand_name)s,%(owner_company)s,%(organic_operation_ID)s);""",content_dict)
#print("executed")
#print(y)

#insert_brand_info(content_dict)
#cur.close()
#conn.close()


