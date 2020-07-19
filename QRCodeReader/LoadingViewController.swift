//
//  LoadingViewController.swift
//  QRCodeReader
//
//  Created by Vishesh Dhawan on 6/15/20.
//  Copyright © 2020 AppCoda. All rights reserved.
//
/*
import UIKit
import SwiftGifOrigin
import ImageIO

let foundVC = UIStoryboard(name: "Main", bundle:nil).instantiateViewController(withIdentifier: "ScoreViewController") as UIViewController
let appDelegate = (UIApplication.shared.delegate as! AppDelegate)


extension UIApplication {
    class func topViewController(base: UIViewController? = UIApplication.shared.keyWindow?.rootViewController) -> UIViewController? {
        if let nav = base as? UINavigationController {
            return topViewController(base: nav.visibleViewController)
        }
        if let tab = base as? UITabBarController {
            if let selected = tab.selectedViewController {
                return topViewController(base: selected)
            }
        }
        if let presented = base?.presentedViewController {
            return topViewController(base: presented)
        }
        return base
    }
}


class LoadingViewController: UIViewController {
    

    
    let notFoundVC = mainBoard.instantiateViewController(withIdentifier:"BarcodeNotFoundViewController") as! BarcodeNotFoundViewController
    let foundVC = mainBoard.instantiateViewController(withIdentifier:"ScoreViewController") as! ScoreViewController
    //let loadingVC = mainBoard.instantiateViewController(withIdentifier:"LoadingViewController") as! LoadingViewController
    
    @IBOutlet weak var gifImage: UIImageView!
    
    /*func getTopMostViewController() -> UIViewController? {
       var topMostViewController = UIApplication.shared.keyWindow?.rootViewController

        while let presentedViewController = topMostViewController?.presentedViewController {
            topMostViewController = presentedViewController
        }

        return topMostViewController
    }*/
    
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view
        
        appDelegate.window?.rootViewController = UIApplication.topViewController()
        
        var foundBool = false
        
        gifImage.image = UIImage.gif(name: "giphy")
        
        if let url = URL(string: "http://34.201.212.152/scan/"+(barcode)) {
        URLSession.shared.dataTask(with: url) { data, response, error in
           if let data = data {
              if let jsonString = String(data: data, encoding: .utf8) {
                 json = jsonString
                 print(jsonString)
              }
            }
        }.resume()
            
        print("check before is Empty: " + json)
        while json.isEmpty{
                        print("checking if empty")
                        print(json)
                        if !(json.isEmpty){
                            let jsonParts = json.components(separatedBy: " ")
                            print(jsonParts)
                            if jsonParts.contains("found\"\n}\n") || jsonParts.contains("!DOCTYPE"){
                                print("so the if statement worked bc the data was not found but like why isnt it working doe")
                                //self.navigationController?.pushViewController(notFoundVC, animated: true)
                                //UIApplication.topViewController()?.present(self.notFoundVC, animated: true, completion: nil)
                               // self.performSegue(withIdentifier: "loadingToNFVC", sender: self)
                                UIApplication.topViewController()!.performSegue(withIdentifier: "loadingToNFVC", sender: self)
                                foundBool = false
                            }
                            else{
                                self.foundVC.text = json
                                //UIApplication.topViewController()?.present(self.foundVC, animated: true, completion: nil)
                                print("trying to go to score view controller")
                               // self.performSegue(withIdentifier: "loadingToSVC", sender: self)
                                self.dismiss(animated:false, completion: nil)
                                self.performSegue(withIdentifier: "loadingToSVC", sender: self)                                //UIApplication.topViewController()!.performSegue(withIdentifier: "loadingToSVC", sender: self)
                                foundBool = true
                            }
                        }
                }
        }
        
        /*if foundBool == true{
            print("foundBool is true")
            UIApplication.topViewController()!.performSegue(withIdentifier: "loadingToSVC", sender: self)
        }
        else{
            print("foundBool is fasle")
            UIApplication.topViewController()!.performSegue(withIdentifier: "loadingToNFVC", sender: self)
        }*/
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}

/*extension UIApplication {
    class func topViewController(base: UIViewController? = UIApplication.shared.keyWindow?.rootViewController) -> UIViewController? {
        if let nav = base as? UINavigationController {
            return topViewController(base: nav.visibleViewController)
        }
        if let tab = base as? UITabBarController {
            if let selected = tab.selectedViewController {
                return topViewController(base: selected)
            }
        }
        if let presented = base?.presentedViewController {
            return topViewController(base: presented)
        }
        return base
    }
}
*/
}
*/
