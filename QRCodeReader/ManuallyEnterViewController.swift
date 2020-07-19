//
//  ManuallyEnterViewController.swift
//  QRCodeReader
//
//  Created by Vishesh Dhawan on 6/8/20.
//  Copyright © 2020 AppCoda. All rights reserved.
//


import UIKit

let mainBoard : UIStoryboard = UIStoryboard(name: "Main", bundle:nil)

var vSpinner : UIView?
 
extension UIViewController {
    func showSpinner(onView : UIView) {
        let spinnerView = UIView.init(frame: onView.bounds)
        spinnerView.backgroundColor = UIColor.init(red: 0.5, green: 0.5, blue: 0.5, alpha: 0.5)
        let ai = UIActivityIndicatorView.init(style: .whiteLarge)
        ai.startAnimating()
        ai.center = spinnerView.center
        
        DispatchQueue.main.async {
            spinnerView.addSubview(ai)
            onView.addSubview(spinnerView)
        }
        
        vSpinner = spinnerView
    }
    
    func removeSpinner() {
        DispatchQueue.main.async {
            vSpinner?.removeFromSuperview()
            vSpinner = nil
        }
    }
}

class ManuallyEnterViewController: UIViewController, UITextFieldDelegate{
    
    var activityIndicator:UIActivityIndicatorView = UIActivityIndicatorView()
    
    let notFoundVC = BarcodeNotFoundViewController(nibName: "BarcodeNotFoundViewController", bundle: nil)
    let foundVC = ScoreViewController(nibName: "ScoreViewController", bundle: nil)
    
    
    @IBOutlet var validLabel: UILabel!
    
    
    @IBOutlet var manualBarcode: UITextField!
    
    //let alert = UIAlertController(title: nil, message: "Please wait...", preferredStyle: .alert)
    override func viewDidLoad() {
        super.viewDidLoad()
        
        validLabel.isHidden = true
        //alert.dismiss(animated: true, completion: nil)
        
        
        // Do any additional setup after loading the view.
    }
    
    
    @IBAction func getScore(_ sender: Any) {
        
        self.showSpinner(onView: self.view)
        
        //dismiss(animated: false, completion: nil)
        //activityIndicator.center = self.view.center
        //activityIndicator.hidesWhenStopped = true
        //activityIndicator.style = UIActivityIndicatorView.Style.gray
        //view.addSubview(activityIndicator)
        
        //activityIndicator.startAnimating()
        
        json = ""
        
        let loadingIndicator = UIActivityIndicatorView(frame: CGRect(x: 10, y: 5, width: 50, height: 50))
        loadingIndicator.hidesWhenStopped = true
        loadingIndicator.style = UIActivityIndicatorView.Style.medium
        loadingIndicator.startAnimating();
        //alert.view.addSubview(loadingIndicator)
        //present(alert, animated: true, completion: nil)
        
        
        if !(manualBarcode.text?.count == 12) || (CharacterSet.letters.isSuperset(of: CharacterSet(charactersIn: manualBarcode.text!))) {
            validLabel.isHidden = false
        }
        else{
            validLabel.isHidden = true
            barcode = manualBarcode.text!
            print("printing barcode in manuallyenterviewcontroller after assigning barcode to manualBarcode.text!")
            print(barcode)
            
            //self.performSegue(withIdentifier: "manualToLoading", sender: self)
            
            if let url = URL(string: "http://35.153.34.57/scan/"+(manualBarcode.text!)) {
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
                        if jsonParts.contains("found\"\n}\n") || jsonParts.contains("!DOCTYPE"){
                            print("so the if statement worked bc the data was not found but like why isnt it working doe")
                            //self.navigationController?.pushViewController(notFoundVC, animated: true)
                            //self.present(notFoundVC, animated: true, completion: nil)
                            //self.present(notFoundVC, animated: true, completion: nil)
                            //alert.dismiss(animated: true, completion: nil)
                            
                            self.removeSpinner()
                            self.performSegue(withIdentifier: "manualToNFVC", sender: self)
                            //break
                            //activityIndicator.stopAnimating()
                            
                        }
                        else{
                            foundVC.text = json
                            print("trying to segue to score view controller")
                            //self.navigationController?.pushViewController(foundVC, animated: true)
                            //.parse()
                            //self.present(foundVC, animated: true, completion: nil)
                            //alert.dismiss(animated: true, completion: nil)
                            self.removeSpinner()
                            self.performSegue(withIdentifier: "manualToSVC", sender: self)
                            //break
                            //activityIndicator.stopAnimating()
                        }
                    }
                }
            }
            
        }
    }
}

