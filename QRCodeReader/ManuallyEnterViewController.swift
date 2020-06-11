//
//  ManuallyEnterViewController.swift
//  QRCodeReader
//
//  Created by Vishesh Dhawan on 6/8/20.
//  Copyright © 2020 AppCoda. All rights reserved.
//

import UIKit

let mainBoard : UIStoryboard = UIStoryboard(name: "Main", bundle:nil)

class ManuallyEnterViewController: UIViewController, UITextFieldDelegate{
    
    let notFoundVC = mainBoard.instantiateViewController(withIdentifier:"BarcodeNotFoundViewController") as! BarcodeNotFoundViewController
    let foundVC = mainBoard.instantiateViewController(withIdentifier:"ScoreViewController") as! ScoreViewController
   // let notFoundVC = BarcodeNotFoundViewController(nibName: "BarcodeNotFoundViewController", bundle: nil)
   // let foundVC = ScoreViewController(nibName: "ScoreViewController", bundle: nil)
    


    
    @IBOutlet var manualBarcode: UITextField!
    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    
    @IBAction func getScore(_ sender: Any) {
        
        json = ""
        
        if let url = URL(string: "http://100.24.206.109/scan_upc/"+(manualBarcode.text!)) {
           URLSession.shared.dataTask(with: url) { data, response, error in
              if let data = data {
                 if let jsonString = String(data: data, encoding: .utf8) {
                    json = jsonString
                    print(jsonString)
                 }
               }
           }.resume()
            
            while json.isEmpty{
                print("checking if empty")
                print(json)
                if !(json.isEmpty){
                    let jsonParts = json.components(separatedBy: " ")
                    print(jsonParts)
                    if jsonParts.contains("found\"\n}\n"){
                        print("so the if statement worked bc the data was not found but like why isnt it working doe")
                        //self.navigationController?.pushViewController(notFoundVC, animated: true)
                        present(notFoundVC, animated: true, completion: nil)
                        //self.present(notFoundVC, animated: true, completion: nil)
                    }
                    else{
                    
                            foundVC.text = json
                        //self.navigationController?.pushViewController(foundVC, animated: true)
                        //.parse()
                        present(foundVC, animated: true, completion: nil)
                    }
                }
            }
        }
    }
}
