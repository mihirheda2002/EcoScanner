#!/usr/bin/env python
# coding: utf-8

import datetime
import time
from firebase import firebase
import datetime
#from selenium import webdriver
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import requests
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
import json
from flask import Flask, request, jsonify
import ssl

app = Flask(__name__)

@app.route("/scan_upc/<query>",methods=["GET"])
def eco_scanner(query):

    context = ssl._create_unverified_context()

    time_dict = {} 

    if not isinstance(query,str):
        query = str(query)
    all_product_values = {}

    fb_connect = firebase.FirebaseApplication("https://ecoscanner-cb66d.firebaseio.com/",None)

    sw = stopwords.words("english")

    #later = datetime.datetime.now()
    #duration = later- now
    #time_dict = {"imports":duration}


    # make sure "v2_organic_operations_dict.json" in directory : in git


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
            uClient = uReq(my_url, context=context)
        except:
            return None
        
        # grab page html, save as soup
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html,"html.parser")
        
        if "invalid" in page_soup.text:
            return None
        
        
        # find the table of item details, use first bc only 1
        container = page_soup.findAll("table",{"class":"detail-list"})[0]
        
        ## create blank dictionary
        info_dict={}
        
        ## find product name
        
        piece = page_soup.findAll("p",{"class":"detailtitle"})[0]
        
        product_name = piece.b.text

        
        def clean(x):
            x=x.replace("&amp","&")
            for char in x:
                if char.isnumeric():
                    tokens = x.split(char)
                    y = tokens[0]
            if not y:    
                return x.split(",")[0]
            else:
                return x.split(",")[0]

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



    now = datetime.datetime.now()
    upc_info_dict = lookup(query)
    later = datetime.datetime.now()
    duration = later-now
    time_dict["lookup upc"] = duration

    if upc_info_dict is None:
        return jsonify({"data":"not found"})
    brand = upc_info_dict["Brand"]
    all_product_values["brand"] = brand
    print(upc_info_dict)


    def clean_product(product,brand):
        sucky_chars = ["-",":",";","(",")","_","%","#","^","&","!","oz","Oz"]
        for char in sucky_chars:
            product = product.replace(char,"").strip()
        for brand_part in brand.split(","):
            product = product.replace(brand_part,"").strip()
        return product


    product_name = clean_product(upc_info_dict["product name"],upc_info_dict["Brand"])

    all_product_values["product name"] = product_name
    product = product_name

    def find_company(brand):
        
        result = fb_connect.get(f"/brand-comp/{brand}",None)
        if result!=None:
            return result

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
                    for item in intake:
                        output.append(item.replace("&amp;","&"))
                    return output
        full_tag = str(list_tag[0])
        splitted = full_tag.split(">")
        pre_company = splitted[1]
        post_company = pre_company.split("</")[0]
        answer = post_company.replace("&amp;","&")
        result = fb_connect.put("/brand-comp/",brand,answer)
        return answer


    now = datetime.datetime.now()
    owner_company = find_company(brand)
    later = datetime.datetime.now()
    duration = later-now
    time_dict["owner company"] = duration
    all_product_values["owner company"] = owner_company
    if type(owner_company)=="list":
        owner_company=owner_company[0]
        

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


    now = datetime.datetime.now()    
    opID_dict = create_dict()
    later = datetime.datetime.now()
    duration = later- now
    time_dict["creating opID_dict"] = duration
        
    def find_operation_id(brand,owner_company=owner_company,opID_dict=opID_dict):
        
        # first check firebase
        result = fb_connect.get(f"/brand-opID/{brand}",None)
        if result is not None:
            return result
        
        
        brand = brand.replace(",","")
        found_keys = list()
        dict_keys=opID_dict.keys()
        for key in dict_keys:
            if brand in key or key in brand:
                found_keys.insert(0,[key,opID_dict[key]["op_nopOpID"]]) #make first term in found_keys a list with key, and opID
        if len(found_keys)>1:
            
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
            if owner_company!="":
                found_keys = find_operation_id(owner_company,owner_company="")
        if len(found_keys)==0:
            opID = "None"
        elif isinstance(found_keys,list):
            if len(found_keys)>=1:
                opID = found_keys[0][1]
        else:
            opID = found_keys
        response = fb_connect.put("/brand-opID",brand,opID)
        return opID


    now = datetime.datetime.now()
    opID = find_operation_id(brand,owner_company)
    later = datetime.datetime.now()
    duration = later- now
    time_dict["find opID"] = duration

    all_product_values["organic operation ID"] = opID


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
            trash_list = ["Organic ",brand,"Super ","Green ","Ounce","ounce","count","Count"]
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


    if opID=="None":
        organic = 0
    else:
        
        organic = 1 # default for if the rest doesn't work
        
        ## come here and write the actual function to produce organic score
        now = datetime.datetime.now()
        organic_info_var = organic_info(opID,product,brand)
        later = datetime.datetime.now()
        duration = later- now
        time_dict["find organic info"] = duration
        all_product_values["organic info"] = organic_info_var
        try:
            if "true" == organic_info_var["organic100"]:
                organic = 3
        except:
            print("hit except 1")
            y=0
        try:
            if "true" == organic_info_var["organic"]:
                organic = 2
        except:
            print("hit except 2")
            y=0
        try:
            if "true" == organic_info_var["madewithorganic"]:
                print("worked where it was supposed to")
                organic = 1
        except:
            print("hit except 3")
            y=0

    all_product_values["organic"] = organic

        
    # ## Fair Trade Scraping

    def check_fair_trade(company,check_parts=True,fb_connect=fb_connect):
        
        # first check firebase
        result = fb_connect.get(f"/brand-Fair Trade/{company}",None)
        if result is not None:
            return int(result)

        company = company.replace(" ","+")
        fair_trade_url = f"https://www.fairtradecertified.org/search/fair-trade-products?product_type=All&name={company}"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
        company = company.replace("+"," ")
        
        headers = {"user-agent":user_agent}
        resp = requests.get(fair_trade_url, headers=headers)

        if resp.status_code==200:
            page_soup = soup(resp.content,"html.parser")

        companies = page_soup.findAll("h3")
        if len(companies)==0:
            if check_parts is False:
                z = 0
            else:
                z = max(check_fair_trade(x.strip(),check_parts=False) for x in company.split())
        else:
            z=1
        
        result = fb_connect.put("/brand-Fair Trade/",company,z)
        return z


    now = datetime.datetime.now()
    fair_trade = check_fair_trade(brand)
    all_product_values["fair trade"] = fair_trade
    later = datetime.datetime.now()
    duration = later- now
    time_dict["fair trade"] = duration


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


    now = datetime.datetime.now() #

    echo = ECHO_violations(brand)
    echo+= ECHO_violations(owner_company)

    later = datetime.datetime.now() #
    duration = later- now
    time_dict["ECHO"] = duration #

    echo = endpoints(echo,lower=0,upper=5)

    echo *= (0-1)

    all_product_values["echo"] = echo


    # ## Non-GMO Project Check 

    def nonGMO(product,brand,first_try=True):
        
        recurse = False # initialize value
        api_url = f"https://ws2.nongmoproject.org/api/v1/get_brands_products_by_keyword?keyword={product}&page=1"
        response = requests.get(api_url)
        if response.status_code==200:
            results_dict = json.loads(response.text)
            results_list = results_dict["data"]
        else:
            recurse = True
        
        if len(results_list)==0 or recurse is True:
            
            if first_try:
                if brand == "" and len(product.split())<=2:
                    for x in brand.split():
                        if nonGMO(x,"none",first_try=False)==1:
                            return 1
                elif brand!="":
                    return nonGMO(brand,"")
            else:
                return 0

        # default input to similarity function, only need to tokenize and find stopwords once
        X_list = word_tokenize(product) 

        for match in results_list:
            name = match["name"]
            similarity_score = check_nlp(name,X_list,product)
            if similarity_score >= 0.35:
                return 1


    now = datetime.datetime.now() #

    nGMO = nonGMO(product,brand)
    all_product_values["nonGMO"] = nGMO


    later = datetime.datetime.now() #
    duration = later - now
    time_dict["nonGMO"] = duration #


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


    now = datetime.datetime.now()


    cdpA = CDP_A(brand)
    cdpA+= CDP_A(owner_company)/2
    cdpA = endpoints(cdpA,lower=0,upper=3)
    all_product_values["cdpA"] = cdpA

    later = datetime.datetime.now()
    duration = later- now
    time_dict["cdpA"] = duration

    # # Rainforest Alliance


    def ra_check(brand,fb_connect=fb_connect):
        
        result = fb_connect.get(f"/brand-RA/{brand}",None)
        if result is not None:
            return result
        
        # request module and parsing
        ra_url = f"https://www.rainforest-alliance.org/find-certified?location=330&category=&keyword={brand}&op=submit"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"

        headers = {"user-agent":user_agent}
        resp = requests.get(ra_url, headers=headers)

        if resp.status_code!=200:
            return None
        else:
            page_soup = soup(resp.text,"html.parser")
            
        companies = page_soup.findAll("div",{"class":"cp-teaser-info-content"})
        
        if len(companies)==0:
            z = 0
        else:
            z = 1
        
        result2 = fb_connect.put("/brand-RA/",brand,z)
        return z


    now = datetime.datetime.now()

    RA = ra_check(brand)
    RA += ra_check(owner_company)/2
    all_product_values["rainforest alliance"] = RA


    later = datetime.datetime.now()
    duration = later- now
    time_dict["rainforest alliance"] = duration


    ## creating final score

    final_score = 5 # initialize

    used = 0 # num of keys that were not none
    keys = ["organic","fair trade","echo","nonGMO","cdpA","rainforest alliance"]
    #keys.append("ingredient score")
    for key in keys:
        temp_val = all_product_values[key]
        if temp_val != None:
            final_score+=temp_val
            used+=1
            
    final_score = final_score / (used/len(keys)) # scale up score to take into account to avoid punishing for None
            
    final_score = endpoints(final_score,lower=0,upper=10)

    all_product_values["pre-score"] = final_score

    all_product_values["Eco-Score"] = round(final_score)

    print(all_product_values)


    time_dict_2 = {}
    for key in time_dict.keys():
        time_dict_2[key] = str(time_dict[key])
    print(time_dict_2)

    return jsonify(all_product_values)


    # with open(f"v1_{query}_times.json","w") as file:
    #     string = json.dumps(time_dict_2)
    #     file.write(string)

if __name__ == '__main__':
    app.run(threaded=True,host="0.0.0.0",port=5000,debug=True)




