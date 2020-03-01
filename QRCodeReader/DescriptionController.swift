//
//  DescriptionController.swift
//  QRCodeReader
//
//  Created by Vishesh Dhawan on 2/29/20.
//  Copyright © 2020 AppCoda. All rights reserved.
//

import Foundation
import UIKit

class DescriptionController: UIViewController {
    
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var priceLabel: UILabel!
    @IBOutlet weak var descriptionLabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        barcode = ""
        nameLabel.text = getString(key: "title")
        priceLabel.text = "$\(getPrice(key: "price"))"
        descriptionLabel.text = getString(key: "description")
    }
}

func getString(key: String) -> String {
    let x = "\(key)\":\""
    let y = json.components(separatedBy: x)[1]
    let z = y.components(separatedBy: "\"")[0]
    return z
}

func getPrice(key: String) -> String {
    let x = "\"\(key)\":"
    let y = json.components(separatedBy: x)[1]
    let z = y.components(separatedBy: ",")[0]
    return z
}

//{"code":"OK","total":1,"offset":0,"items":[{"ean":"0049000031652","title":"Dasani Purified Water 16.9 oz 24 ct","description":"DASANI has been designed to be a great tasting water. It is filtered by reverse osmosis to remove impurities, then enhanced with a special blend of minerals for the pure, crisp, fresh taste that's delightfully DASANI. DASANI offers a wide variety of water products that range from purified water, sparkling water, water flavor drops, and flavored water.","upc":"049000031652","brand":"DASANI","model":"00049000031652","color":"Stainless steel","size":"","dimension":"16 X 10.5 X 9 inches","weight":"28.2 Pounds","category":"Food, Beverages & Tobacco > Beverages > Water","currency":"","lowest_recorded_price":0,"highest_recorded_price":43.48,"images":["https://pics.drugstore.com/prodimg/418324/450.jpg","https://officedepot.scene7.com/is/image/officedepot/516125_p?$Enlarge$#_lg.jpg","https://i5.walmartimages.com/asr/39e0ad61-2028-40de-80e6-1a77133fb75b_1.8352ce4d5d4cd6fc209ac17a7e38528f.jpeg?odnHeight=450&odnWidth=450&odnBg=ffffff","https://target.scene7.com/is/image/Target/GUEST_de1adfcf-8972-4234-b019-da4646c8bb50?wid=1000&hei=1000","http://c.shld.net/rpx/i/s/i/spin/10127449/prod_ec_1570367702","http://ct.mywebgrocer.com/legacy/productimagesroot/DJ/6/251046.jpg","https://www.staples-3p.com/s7/is/image/Staples/sp43802041_sc7?$enl$","https://tshop.r10s.com/79a/e84/dd59/b6a4/a058/d601/c43c/119ae89b632c600c73735e.jpg?_ex=512x512","http://images10.newegg.com/ProductImageCompressAll200/A1FS_1_20130405141201487.jpg","https://jetimages.jetcdn.net/md5/791d8b678c53883d258fb76bdc4bbfc2.500"],"offers":[{"merchant":"Staples","domain":"staples.com","title":"\"Dasani Water, 16.9 Oz., 24/Carton (00049000031652)\"","currency":"","list_price":"","price":16.69,"shipping":"","condition":"New","availability":"","link":"https://www.upcitemdb.com/norob/alink/?id=x2x243x2w2y2e484w2&tid=1&seq=1583033589&plt=f6924d8eac4e830a4a7940bbd003386e","updated_t":1580287174},{"merchant":"Walgreens","domain":"walgreens.com","title":"Dasani Purified Water - 16.9 oz. x 24 pack","currency":"","list_price":"","price":5.99,"shipping":"US:::0.00 USD","condition":"New","availability":"","link":"https://www.upcitemdb.com/norob/alink/?id=x2x253t213y2f4d4v2&tid=1&seq=1583033589&plt=2c3c25dea3eed3e7f52cfae5c52e3569","updated_t":1579874407},{"merchant":"Kmart","domain":"kmart.com","title":"Purified .5 L Water 24 PK PLASTIC BOTTLES","currency":"","list_price":"","price":5.99,"shipping":"","condition":"New","availability":"","link":"https://www.upcitemdb.com/norob/alink/?id=u2r26323z2636464t2&tid=1&seq=1583033589&plt=a037db06bbf97ace0161043d05a80cb2","updated_t":1471911680},{"merchant":"Office Depot","domain":"officedepot.com","title":"Dasani Water, 16.9 Oz, Pack Of 24 Bottles","currency":"","list_price":"","price":15.79,"shipping":"US:::9.95 USD","condition":"New","availability":"","link":"https://www.upcitemdb.com/norob/alink/?id=v2w203z22303e444&tid=1&seq=1583033589&plt=839871828c64c0b57476870fc773af8d","updated_t":1582874295},{"merchant":"Rakuten(Buy.com)","domain":"rakuten.com","title":"Dasani Purified Water - 24/16.9 oz. (.5L) Bottles","currency":"","list_price":"","price":20.79,"shipping":"","condition":"New","availability":"","link":"https://www.upcitemdb.com/norob/alink/?id=v2q243u2v2539484s2&tid=1&seq=1583033589&plt=0dd701de8dc5a493528dacd7405bb183","updated_t":1558193388},{"merchant":"Wal-Mart.com","domain":"walmart.com","title":"Dasani Purified Water, .5 l, 24 pack","currency":"","list_price":"","price":4.48,"shipping":"5.99","condition":"New","availability":"","link":"https://www.upcitemdb.com/norob/alink/?id=u2u233u2w2x274a4w2&tid=1&seq=1583033589&plt=1d599f8de8c470f62712e1f07176a79c","updated_t":1570201695},{"merchant":"Target","domain":"target.com","title":"Dasani Purified Water 16.9 oz 24 ct","currency":"","list_price":"","price":4.99,"shipping":"","condition":"New","availability":"","link":"https://www.upcitemdb.com/norob/alink/?id=23p23323w223f444&tid=1&seq=1583033589&plt=fece4ca5b1ce76385212885c03908e63","updated_t":1573350709},{"merchant":"Newegg Business","domain":"neweggbusiness.com","title":"Dasani Purified Water - 24/16.9 oz. (.5L) Bottles","currency":"","list_price":"","price":31.57,"shipping":"Free Shipping","condition":"New","availability":"","link":"https://www.upcitemdb.com/norob/alink/?id=v2u2231323z28454t2&tid=1&seq=1583033589&plt=1389f5b62157a0bbce32c1d38bed50d4","updated_t":1526485717},{"merchant":"Albertsons","domain":"albertsons.com","title":"DASANI - Purified Water - 24 Pack Bottles 405.60 fl oz","currency":"","list_price":"","price":0,"shipping":"","condition":"New","availability":"","link":"https://www.upcitemdb.com/norob/alink/?id=v2q23303z2x264d4q2&tid=1&seq=1583033589&plt=29349c223df31d88cce718ec1adb963d","updated_t":1484640858},{"merchant":"Jet.com","domain":"jet.com","title":"Dasani Purified Water, 16.9 Fl Oz","currency":"","list_price":"","price":10.6,"shipping":"","condition":"New","availability":"","link":"https://www.upcitemdb.com/norob/alink/?id=w2v2z2z2w2x26484z2&tid=1&seq=1583033589&plt=149572ebe8912b5169548adfb387ac62","updated_t":1561999083}],"asin":"B000T9SZOU","elid":"193193063697"}]}
