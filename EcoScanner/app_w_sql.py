# app.py
from flask import Flask, request, jsonify

#!/usr/bin/env python
# coding: utf-8

import datetime
import time
#from firebase import firebase
#from selenium import webdriver
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json
import ssl
import eco_sql_lib

app = Flask(__name__)

@app.route('/scan/<query>',methods=["GET"])
    
def eco_scanner(query):

    print('in route')
        
    response = {}
    

    time_dict = {}

    if not isinstance(query,str):
        query = str(query)
        
    all_product_values = {}

    #fb_connect = firebase.FirebaseApplication("https://ecoscanner-cb66d.firebaseio.com/",None)

    sw = stopwords.words("english")

    # make sure "v2_organic_operations_dict.json" in directory / in git


    def endpoints(x,lower=0,upper=10):
        if x<lower:
            return lower
        elif x>upper:
            return upper
        else:
            return x



    ## NLP filtration method for products
    def check_nlp(itemvarieties,X_list,product,sw=sw):

        # if cosine function doesn't work, use own alternative
        def own_similarity_function(product,itemvarieties):


            if product in itemvarieties:
                return endpoints((len(product)*2/len(itemvarieties)))
            elif itemvarieties in product:
                return endpoints((len(itemvarieties)*2/len(product)))
            else:
                return 0


        l1 =[];l2 =[]

        # tokenization

        Y_list = word_tokenize(itemvarieties)

        # sw contains the list of stopwords


        # remove stop words from string
        X_set = {w for w in X_list if not w in sw}
        Y_set = {w for w in Y_list if not w in sw}

        # form a set containing keywords of both strings
        rvector = X_set.union(Y_set)
        for w in rvector:
            if w in X_set:
                l1.append(1) # create a vector
            else:
                l1.append(0)
            if w in Y_set:
                l2.append(1)
            else:
                l2.append(0)

        c = 0

        # cosine formula
        for i in range(len(rvector)):
            c+= l1[i]*l2[i]
        
        try:
            cosine = c / float((sum(l1)*sum(l2))**0.5)
        except ZeroDivisionError:
            return own_similarity_function(product,itemvarieties)
        
        if cosine ==0:
            return own_similarity_function(product,itemvarieties)
        
        return cosine


    ## creates a dictionary with all known info from upcitemdb.com

    def lookup(query):
        ## append search UPC to the database website
        my_url = "https://www.upcitemdb.com/upc/"+query
        
        #open urllib client, accounting for page not-existing
        try:
            uClient = uReq(my_url)
        except:
            context = ssl._create_unverified_context()
            try:
                uClient = uReq(my_url,context=context)
            except:
                print("Uclient not working")
                return None
        
        # grab page html, save as soup
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html,"html.parser")
        
        if "invalid" in page_soup.text:
            print("invalid")
            return None
        
        
        # find the table of item details, use first bc only 1
        try:
            container = page_soup.findAll("table",{"class":"detail-list"})[0]
        except:
            print("the correct table is not found")
            return None
        
        ## create blank dictionary
        info_dict={}
        
        ## find product name
        
        piece = page_soup.findAll("p",{"class":"detailtitle"})[0]
        
        product_name = piece.b.text

        
        def clean(x):
            y = "default"
            x=x.replace("&amp","&")
            for char in x:
                if char.isnumeric():
                    tokens = x.split(char)
                    y = tokens[0]
            if y == "default":
                return x.split(",")[0]
            else:
                return y.split(",")[0]

        product_name = clean(product_name)

        
        ## find all other info
        trs = container.findAll("tr")
        
        ## loop through info things
        for tr in trs:
            
            # make list, containing key line and value line
            tds = tr.findAll("td")
            
            ## parse out key and value, save to info dict
            key = str(tds[0]).strip("<td>").strip("</").strip(":")
            value = str(tds[1]).strip("<td>").strip("</").strip().strip("\t")
            # don't care ab last-scanned
            if key != "Last Scanned":
                if key=="Brand":
                    for part in value.split():
                        for part2 in part.split(','):
                            product_name = product_name.replace(part2,"")
                    
                    info_dict["product name"] = product_name.strip()
                info_dict[key]=value
        return info_dict



    #now = datetime.datetime.now()
    upc_info_dict = lookup(query)
    """later = datetime.datetime.now()
    duration = later-now
    time_dict["lookup upc"] = duration"""

    if upc_info_dict is None:
        return jsonify({"data":"not found"})
    try:
        brand = upc_info_dict["Brand"]
    except KeyError:
        return jsonify({"data":"not found"})
    all_product_values["brand"] = brand
    print(upc_info_dict)


    def clean_product(product,brand):
        sucky_chars = ["-",":",";","(",")","_","%","#","^","&","!","oz","Oz","Cups","cups","pack","Pack","cans","Cans"]
        for char in sucky_chars:
            product = product.replace(char,"").strip()
        #for brand_part in brand.split(","):
         #   product = product.replace(brand_part+" ","").strip()
        product = product.replace(brand+" ","").strip()

        while "  " in product:
            product = product.replace("  "," ")

        for word in product.split():
            if word.replace(".","").isnumeric():
                product = product.replace(word,"").strip()


        return product


    product_name = clean_product(upc_info_dict["product name"],upc_info_dict["Brand"])

    all_product_values["product name"] = product_name
    product = product_name

    def shared_by_brand(brand,product,cur,conn):

        in_dict = {"brand_name":brand}

        def find_company(brand):

            def side_box_check(brand,page_soup):
                parents = []
                side_box_list = page_soup.findAll("div",{"class":"zloOqf PZPZlf"})
                for item in side_box_list:
                    if "Parent" in str(item):
                        mini_set = item.findAll("span",{"class":"LrzXr kno-fv"})
                        mini_set = str(mini_set[0]).split(",")
                        for f1 in mini_set:
                            for snippet in str(f1).split(">"):
                                if "</a" in snippet:
                                    parents.append(snippet.strip("</a").replace("&amp;","&"))
                if len(parents)!=0:
                    return parents
                else:
                    return table_check(brand,page_soup)
                
            def table_check(brand,page_soup):
                try:
                    table = page_soup.findAll("div",{"class":"webanswers-webanswers_table__webanswers-table"})[0]
                except:
                    return lame_box_check(brand,page_soup)
                rows = table.findAll("tr")
                for tr in rows:
                    if "Owner" in str(tr):
                        owner_line = str(tr.findAll("td")[1])
                        trim1 = owner_line.split(">")[1]
                        trim2 = trim1.strip("</td>")
                        return trim2.split(",")
            
            def lame_box_check(brand,page_soup):
                output = []
                not_comp = ["company",brand,"parent"]
                try:
                    info = page_soup.findAll("span",{"class":"e24Kjd"})[0]
                except IndexError:
                    return brand
                bolded = info.findAll("b")
                for bold in bolded:
                    bold = str(bold).strip("<b>").strip("</b>")
                    if bold not in not_comp:
                        output.append(bold)
                for option in output:
                    if option in brand or brand in option:
                        output.pop(output.index(option))
                return output

            
            my_url = f"https://www.google.com/search?q={brand}+parent+company"
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"

            headers = {"user-agent":user_agent}
            resp = requests.get(my_url, headers=headers)

            if resp.status_code == 200:
                page_soup = soup(resp.content, "html.parser")
            else:
                return brand
            
            list_tag = page_soup.findAll("a",{"class":"FLP8od"})
            if len(list_tag)==0:
                list_tag = page_soup.findAll("div",{"class":"Z0LcW AZCkJd"})
                if len(list_tag)==0:
                    list_tag = page_soup.findAll("div",{"class":"Z0LcW"})
                    if len(list_tag)==0:
                        output = []
                        intake = side_box_check(brand,page_soup)
                        if isinstance(intake,str):
                            return intake
                        elif intake is None:
                            return brand
                        for item in intake:
                            output.append(item.replace("&amp;","&"))
                        return output
            full_tag = str(list_tag[0])
            splitted = full_tag.split(">")
            pre_company = splitted[1]
            post_company = pre_company.split("</")[0]
            answer = post_company.replace("&amp;","&")
            #result = fb_connect.put("/brand-comp/",brand,answer)
            return answer

        owner_company = find_company(brand)
        if type(owner_company)=="list":
            owner_company=owner_company[0]
        all_product_values["owner company"] = owner_company
        in_dict["owner_company"] = owner_company
        

        def multi_splits(lst1,splitters_list):
            def split_single(lst2,splitter):
                out = []
                for thing in lst2:
                    out.extend([x.strip() for x in thing.split(splitter)])
                return out
            
            for splitter in splitters_list:

                lst1 = split_single(lst1,splitter)
            
            return lst1
                
            
        #Creating MegaDict

        def create_dict(filename="v2_organic_operations_dict.json"):
            with open(filename,"r") as json_file:
                mega_dict = json.load(json_file)
                if type(mega_dict)=="str":
                    print("oops string error")
                else:
                    return mega_dict


        #now = datetime.datetime.now()
        opID_dict = create_dict()
        """later = datetime.datetime.now()
        duration = later- now
        time_dict["creating opID_dict"] = duration"""
        
        def find_operation_id(brand,owner_company=owner_company,opID_dict=opID_dict):
            
            """first check firebase
            result = fb_connect.get(f"/brand-opID/{brand}",None)
            if result is not None:
                return result"""
            
            
            brand = brand.replace(",","")
            found_keys = list()
            dict_keys=opID_dict.keys()
            for key in dict_keys:
                if brand in key or key in brand:
                    found_keys.insert(0,[key,opID_dict[key]["op_nopOpID"]]) #make first term in found_keys a list with key, and opID
            

            if len(found_keys)==1:
                print("from 1")
                return found_keys[0][1]

            elif len(found_keys)>1:
                
                # default input to similarity function, only need to tokenize and find stopwords once
                X_list = word_tokenize(brand)

                for hit in found_keys:
                    sim_dict = {}
                    name = hit[0]
                    similarity_score = check_nlp(name,X_list,brand)
                    sim_dict[similarity_score] = hit
                max_sim = max(sim_dict.keys())
                found_keys = sim_dict[max_sim]

            else:
                if owner_company=="":
                    return None
                else:
                    opID = find_operation_id(owner_company,owner_company="")
                    if found_keys is None:
                        return None
                    else:
                        return opID
            print("found 2")
            return found_keys[1]

        """now = datetime.datetime.now()
        opID = find_operation_id(brand,owner_company)
        later = datetime.datetime.now()
        duration = later- now
        time_dict["find opID"] = duration

        all_product_values["organic operation ID"] = opID"""

        opID = find_operation_id(brand,owner_company)
        print(f"opID is {opID}")
        all_product_values["organic operation ID"] = opID
        in_dict["organic_operation_ID"] = opID
            
        # ## Fair Trade Scraping

        def check_fair_trade(brand,company):
            
            brand = brand.replace(" ","+")
            fair_trade_url = f"https://www.fairtradecertified.org/search/fair-trade-products?product_type=All&name={brand}"
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
            brand = brand.replace("+"," ")
            
            headers = {"user-agent":user_agent}
            resp = requests.get(fair_trade_url, headers=headers)

            if resp.status_code==200:
                page_soup = soup(resp.content,"html.parser")

            companies = page_soup.findAll("h3")
            if len(companies)==0:
                if company=="":
                    z = 0
                else:
                    z = check_fair_trade(company,"")
            else:
                z=1
            
            #result = fb_connect.put("/brand-Fair Trade/",company,z)
            return z


        """now = datetime.datetime.now()
        fair_trade = check_fair_trade(brand)
        all_product_values["fair trade"] = fair_trade
        later = datetime.datetime.now()
        duration = later- now
        time_dict["fair trade"] = duration"""

        fair_trade = check_fair_trade(brand,owner_company)
        all_product_values["fair trade"] = fair_trade
        in_dict["fair_trade"] = fair_trade

        # # ECHO API

        def evaluate_facility(mini_dict):
            status = mini_dict["CURR_COMP_STATUS"]
            if "serious" in status:
                return 2
            elif "(s)" in status:
                return 1
            else:
                return 0
            
        def violation_score(return_list):
            score=0
            for mini_dict in return_list:
                score+=evaluate_facility(mini_dict)
            return score

        def ECHO_violations(brand):
            brand = brand.upper()
            api_url = f"https://enviro.epa.gov/enviro/efservice/t_compliance_echo/NAME/CONTAINING/{brand}/JSON"
            response = requests.get(api_url)
            if response.status_code == 200:
                return_list = json.loads(response.text)
                if len(return_list)==0:
                    return 0
                else:
                    vio_ratio = violation_score(return_list)/len(return_list)
                    return vio_ratio*10
            else:
                return None


        #now = datetime.datetime.now() #

        echo = ECHO_violations(brand)
        echo+= ECHO_violations(owner_company)

        """later = datetime.datetime.now() #
        duration = later- now
        time_dict["ECHO"] = duration #"""

        echo = endpoints(echo,lower=0,upper=3)

        echo *= (0-1)

        all_product_values["echo"] = echo
        in_dict["echo"] = echo


        # ## Non-GMO Project Check

        def nonGMO(product,brand,first_try=True):
            
            #recurse = False # initialize value
            combo = brand + ' ' + product
            print(combo)
            api_url = f"https://ws2.nongmoproject.org/api/v1/get_brands_products_by_keyword?keyword={combo}&page=1"
            response = requests.get(api_url)
            if response.status_code==200:
                results_dict = json.loads(response.text)
                results_list = results_dict["data"]
            else:
                results_list = []
            
            if len(results_list)==0:
                
                if brand != "":
                    return nonGMO(brand,"")
                    """if brand == "" and len(product.split())<=2:
                        for x in brand.split():
                            if nonGMO(x,"none",first_try=False)==1:
                                return 1
                elif brand!="":
                        return nonGMO(brand,"")"""
                else:
                    return 0
            else:
                return 1

            # default input to similarity function, only need to tokenize and find stopwords once
            """X_list = word_tokenize(product)

            for match in results_list:
                name = match["name"]
                similarity_score = check_nlp(name,X_list,product)
                if similarity_score >= 0.35:
                    return 1"""


        #now = datetime.datetime.now()

        nGMO = nonGMO(product,brand)
        all_product_values["nonGMO"] = nGMO
        in_dict["nonGMO"] = nGMO


        """later = datetime.datetime.now() #
        duration = later - now
        time_dict["nonGMO"] = duration #"""


        # ## CDP A-List


        def CDP_A(company):

            with open("cdp_dict.json","r") as json_file:
                cdp_dict = json.loads(json_file.readline())
            
            possible = []
            company = company.lower()
            
            for key in cdp_dict.keys():
                if company in key.lower() or key.lower() in company:
                    possible.append([key,cdp_dict[key]])
            if len(possible)==0:
                return 0
            elif len(possible)==1:
                return possible[0][1]
            else:
                # default input to similarity function, only need to tokenize and find stopwords once
                X_list = word_tokenize(company)


                round2_dict = {}
                for option in possible:
                    sim_score = check_nlp(option[0],X_list,company)
                    round2_dict[sim_score] = option
                best_list = round2_dict[max(round2_dict.keys())]
                return best_list[1]


        #now = datetime.datetime.now()


        cdpA = CDP_A(brand)
        cdpA+= CDP_A(owner_company)/2
        cdpA = endpoints(cdpA,lower=0,upper=3)
        all_product_values["cdpA"] = cdpA
        in_dict["cdpA"] = cdpA

        """later = datetime.datetime.now()
        duration = later- now
        time_dict["cdpA"] = duration"""

        # # Rainforest Alliance


        def ra_check(brand):
            
            """result = fb_connect.get(f"/brand-RA/{brand}",None)
            if result is not None:
                return result"""
            
            # request module and parsing
            ra_url = f"https://www.rainforest-alliance.org/find-certified?location=330&category=&keyword={brand}&op=submit"
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"

            headers = {"user-agent":user_agent}
            resp = requests.get(ra_url, headers=headers)

            if resp.status_code!=200:
                print("huge freaking error")
                return None
            else:
                page_soup = soup(resp.text,"html.parser")
                
            companies = page_soup.findAll("div",{"class":"cp-teaser-info-content"})
            
            if len(companies)==0:
                z = 0
            else:
                z = 1
            
            #result2 = fb_connect.put("/brand-RA/",brand,z)
            return z


        #now = datetime.datetime.now()

        RA = ra_check(brand)
        print(f"RA is {RA}")
        try:
            RA += ra_check(owner_company)/2
        except:
            "hi"
        all_product_values["rainforest alliance"] = RA
        in_dict["RA"] = RA

        eco_sql_lib.insert_brand_info(in_dict,cur,conn)

        return in_dict


    ## save all vals in dictionary
    ## push it to the SQL database



    """later = datetime.datetime.now()
    duration = later- now
    time_dict["rainforest alliance"] = duration"""

## Receiving Operation Products based on op_code

    def find_itemvarieties(item,tag="itemvarieties"):
        deets = item.split("</")
        for deet in deets:
            if f"<a:{tag}>" in deet:
                itemvarieties = deet.split(">")[-1]
                return itemvarieties
            
    def organic_info(op_id,product,brand):
            
        
        do_trash=True
        if do_trash:
            # get rid of common words that are clutter, this list should grow with testing
            trash_list = ["Organic ",brand,"Super ","Green ","Ounce","ounce","count","Count","pack"]
            for stink in trash_list:
                product = product.replace(stink,"").strip()
            if " " in product:
                for word in product.split():
                    for stink in trash_list:
                        if stink in word or word.isnumeric():
                            product = product.replace(word,"").strip()
            product = product.split(",")[0]
            product = product.replace(brand,"").strip()
        
        # default input to similarity function, only need to tokenize and find stopwords once
        X_list = word_tokenize(product)

        ## API request
        my_api_key = "9ZTbuCeX9dP5keqlGJZyWNdg1c1xCu3p9pLhJ1MS"
        json = {"startIdx":"1","count":"100","operationId":op_id}
        response = requests.post(f"https://organicapi.ams.usda.gov/IntegrityPubDataServices/OidPublicDataService.svc/rest/Items?api_key={my_api_key}",json=json)

        # parsing into a list of items
        all_text = response.text
        page_soup = soup(all_text,"lxml")
        page2 = soup(str(page_soup),"html.parser")
        items = page2.findAll("a:item")

        if len(items)==0:
            return None

        # create list of API response terms we care about
        concerns = ["itemname","itemvarieties","madewithorganic","organic","organic100","otheritems"]
        
        possible_matches = []
        best_choice = {"similarity score":0.2} # initial threshold for any match
        for item in items:
            cont = True
            item = str(item)
            if "status>Certified<" in item:
                #try:
                itemvarieties = find_itemvarieties(item)
                if itemvarieties=="":
                    itemvarieties = find_itemvarieties(item,tag="otheritems")
                if itemvarieties =="":
                    itemvarieties = find_itemvarieties(item,tag="itemname")

                similarity_score = check_nlp(itemvarieties,X_list,product)
                    
                if similarity_score>best_choice["similarity score"]:
                    best_choice = {"similarity score":similarity_score}
                    deets = item.split("</")
                    for deet in deets:
                        for concern in concerns:
                            inclusion_str = "<a:"+concern
                            exclusion_str = "OASNFOIAJDFOAJFDOINOANEFADUB"
                            if concern=="organic":
                                exclusion_str = "organic100"
                            if inclusion_str in deet and exclusion_str not in deet:
                                best_choice[concern]=deet.split(concern)[-1].strip(">").replace("&amp;","&")
        return best_choice

    cur,conn = eco_sql_lib.curse()
    sql_response = eco_sql_lib.brand_info(brand,cur,conn)
    print("sql response is about to print")
    print(sql_response)
    if sql_response is None:
        shared_dict = shared_by_brand(brand,product_name,cur,conn)
    else:
        shared_dict = sql_response.row_dict

    conn.close()
    print("printing shared_dict")
    print(shared_dict)

    for key in shared_dict:
        all_product_values[key] = shared_dict[key]

    print(shared_dict)

    opID = shared_dict["organic_operation_ID"]

    if opID is None:
        organic = 0
    else:
        
        organic = 1 # default for if the rest doesn't work
        
        ## come here and write the actual function to produce organic score
        #now = datetime.datetime.now()
        organic_info_var = organic_info(opID,product,brand)
        #later = datetime.datetime.now()
        #duration = later- now
        #time_dict["find organic info"] = duration
        all_product_values["organic info"] = organic_info_var
        try:
            if "true" == organic_info_var["organic100"]:
                organic = 3
        except:
            #print("hit except 1")
            y=0
        try:
            if "true" == organic_info_var["organic"]:
                organic = 2
        except:
            #print("hit except 2")
            y=0
        try:
            if "true" == organic_info_var["madewithorganic"]:
                #print("worked where it was supposed to")
                organic = 1
        except:
            #print("hit except 3")
            y=0

    all_product_values["organic"] = organic

    ## creating final score

    final_score = 5 # initialize

    print("printing all_product_values")
    print(all_product_values)

    used = 0 # num of keys that were not none
    keys = ["organic","fair_trade","echo","nonGMO","cdpA","RA"]
    #keys.append("ingredient score")
    for key in keys:
        temp_val = all_product_values[key]
        print(temp_val,type(temp_val))
        if temp_val != None:
            final_score+=temp_val
            used+=1
            
    final_score = final_score / (used/len(keys)) # scale up score to take into account to avoid punishing for None
            
    final_score = endpoints(final_score,lower=0,upper=10)

    all_product_values["pre-score"] = final_score

    all_product_values["Eco-Score"] = round(final_score)

    print(all_product_values)

    for key in all_product_values.keys():
        val = all_product_values[key]
        if isinstance(val,str): 
            all_product_values[key] = val.replace(",","").replace(":","")



    """time_dict_2 = {}
    for key in time_dict.keys():
        time_dict_2[key] = str(time_dict[key])
    print(time_dict_2)"""

    return jsonify(all_product_values)


    # with open(f"v1_{query}_times.json","w") as file:
    #     string = json.dumps(time_dict_2)
    #     file.write(string)

    #response["MESSAGE"] = f"query: {query} response: {all_product_values}"
    
    #return jsonify(all_product_values)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    #app.run(threaded=True,port=5000,debug=True)
    app.run(threaded=True, port=80,host="0.0.0.0")
