//
//  ScoreViewController.swift
//  QRCodeReader
//
//  Created by Vishesh Dhawan on 6/8/20.
//  Copyright © 2020 AppCoda. All rights reserved.
//

import UIKit
import Firebase
import Foundation

extension StringProtocol {
    subscript(offset: Int) -> Character {
        self[index(startIndex, offsetBy: offset)]
    }
}

//let mainBoard : UIStoryboard = UIStoryboard(name: "Main", bundle:nil)
//let notFoundView  = mainBoard.instantiateViewController(withIdentifier: "BarcodeNotFoundViewController.swift") as! BarcodeNotFoundViewController

//let storyBoard : UIStoryboard = UIStoryboard(name: "Main", bundle:nil)

//let notFoundVC = storyBoard.instantiateViewController(withIdentifier: "BarcodeNotFoundViewController") as! BarcodeNotFoundViewController



class ScoreViewController: UIViewController {
    
    var text:String = ""
    
    @IBOutlet weak var textLabel:UILabel?
   /* let notFoundVC = mainBoard.instantiateViewController(withIdentifier:"BarcodeNotFoundViewController") as! BarcodeNotFoundViewController
    */
    @IBOutlet weak var scoreLabel: UILabel!
    
    @IBOutlet var dialView: UIImageView!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        //textLabel?.text = text
        
        parse(inJson:json)
        
        var ref: DatabaseReference!
        ref = Database.database().reference()
        ref.child("evaluated").child("6666666666666").observeSingleEvent(of: .value, with: { (snapshot) in
            //Get User Value
            let value  = snapshot.value as? NSDictionary
            print(value!)
        })
        
        /*
        while json.isEmpty{
            print("checking if empty")
            print(json)
            if !(json.isEmpty){
                let jsonParts = json.components(separatedBy: " ")
                print(jsonParts)
                if jsonParts.contains("found\"\n}\n"){
                    print("so the if statement worked bc the data was not found but like why isnt it working doe")
                    self.navigationController?.pushViewController(notFoundVC, animated: true)
                    //self.present(notFoundView, animated: true, completion: nil)
                    //self.present(notFoundVC, animated: true, completion: nil)
                }
                else{
                    parse()
                }
            }
            
        }
 */
    
    }
    
    public func parse(inJson:String) -> Dictionary<String, String>{
        
        let dialDictionary: [String: String] = ["1": "dial1.jpg", "2": "dial2.jpg", "3": "dial3.jpg", "4": "dial4.jpg", "5": "dial5.jpg", "6": "dial6.jpg", "7": "dial7.jpg", "8": "dial8.jpg", "9": "dial9.jpg", "10": "dial10.jpg"]
        
        var jsonDictionary: [String: String] = [:]
        
        let removedChar = ["{", "}", "\n", "  ", "   ", "\t", "\""]
        
        for item in removedChar{
             json = json.replacingOccurrences(of: item, with: "")
        }
        print("printing json")
        print(json)
        
        let jsonPairs = json.components(separatedBy: ",")
        print("printing json pairs")
        print(jsonPairs)
        
        
        
        for pair in jsonPairs{
            var miniArray = pair.components(separatedBy: ":")
            var curStr: String = miniArray[0]
            if curStr[0] == " "{
                let index = curStr.index(curStr.startIndex, offsetBy: 0)
                curStr.remove(at: index)
                miniArray[0] = curStr
            }
            
            var valueStr: String = miniArray[1]
            if valueStr[0] == " "{
                let index = valueStr.index(valueStr.startIndex, offsetBy: 0)
                valueStr.remove(at: index)
                miniArray[1] = valueStr
            }
            
            jsonDictionary[miniArray[0]] = miniArray[1]
            print(miniArray)
        }
        
        
        print("printing json dictionary")
        print(jsonDictionary)
        
        scoreLabel.text = "Eco Score: " + (jsonDictionary["Eco-Score"]!)
        
        print(dialDictionary[jsonDictionary["Eco-Score"]!]!)
       
        dialView.image = UIImage(named: dialDictionary[jsonDictionary["Eco-Score"]!]!)
        
        return jsonDictionary
    }
    
    var documentsUrl: URL {
        return FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
    }
    
    func load(fileName: String) -> UIImage? {
        let fileURL = documentsUrl.appendingPathComponent(fileName)
        do {
            let imageData = try Data(contentsOf: fileURL)
            return UIImage(data: imageData)
        } catch {
            print("Error loading image : \(error)")
        }
        return nil
    }
    
    func getScore(key: String) -> String {
           //let x = key+":"
        let x = json.components(separatedBy: ",")[0] //(separatedBy: ",")
        print("new json")
        print(x)
        print("post new json")
           
        let z = x.components(separatedBy: ":")[1]
        print("printing score...")
        print(z)
        return z
    }
    
}
