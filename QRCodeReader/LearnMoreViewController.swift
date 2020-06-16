//
//  LearnMoreViewController.swift
//  QRCodeReader
//
//  Created by Vishesh Dhawan on 6/10/20.
//  Copyright © 2020 AppCoda. All rights reserved.
//

import UIKit



class LearnMoreViewController: UIViewController {
    
    
    @IBOutlet var cdpaImg: UIImageView!
    
    @IBOutlet var organicImg: UIImageView!
    
    @IBOutlet var echoImg: UIImageView!
    
    @IBOutlet var fairTradeImg: UIImageView!
    
    @IBOutlet var nonGMOImg: UIImageView!
    
    @IBOutlet var rainForestImg: UIImageView!
    
    let checkDic: [String: String] = ["0.0": "xmark.seal.fill", "0": "xmark.seal.fill", "1.0": "checkmark.seal.fill", "1": "checkmark.seal.fill", "null": "xmark.seal.fill"]
    
   // let checkDic: [String: String] = ["0.0": "dial1.jpg", "0": "dial1.jpg", "1.0": "dial10.jpg", "1": "dial10.jpg", "null": "dial1.jpg"]
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        var echoNum: String = ""
        if Float(scoreDic["echo"]!)! < -1{
            echoNum = "1.0"
        }
        else{
            echoNum = "0.0"
        }
        var cdpaNum: String = ""
        if Float(scoreDic["cdpA"]!)! > 0{
            cdpaNum = "1.0"
        }
        else{
            cdpaNum = "0.0"
        }
        print("printing socreDic")
        print(scoreDic)
        
        if #available(iOS 13.0, *) {
        
            cdpaImg.image = UIImage(systemName: checkDic[cdpaNum]!)
            if (checkDic[cdpaNum]!) == ("xmark.seal.fill"){
                cdpaImg.tintColor = UIColor.red
            }
            else{
                cdpaImg.tintColor = UIColor.green
            }
            organicImg.image = UIImage(systemName: checkDic[scoreDic["organic"]!]!)
            if (checkDic[scoreDic["organic"]!]!) == ("xmark.seal.fill"){
                organicImg.tintColor = UIColor.red
            }
            else{
                organicImg.tintColor = UIColor.green
            }
            echoImg.image = UIImage(systemName: checkDic[echoNum]!)
            if (checkDic[echoNum]!) == ("xmark.seal.fill"){
                echoImg.tintColor = UIColor.red
            }
            else{
                echoImg.tintColor = UIColor.green
            }
            fairTradeImg.image = UIImage(systemName: checkDic[scoreDic["fair trade"]!]!)
            if (checkDic[scoreDic["fair trade"]!]!) == ("xmark.seal.fill"){
                fairTradeImg.tintColor = UIColor.red
            }
            else{
                fairTradeImg.tintColor = UIColor.green
            }
            nonGMOImg.image = UIImage(systemName: checkDic[scoreDic["nonGMO"]!]!)
            if (checkDic[scoreDic["nonGMO"]!]!) == ("xmark.seal.fill"){
                nonGMOImg.tintColor = UIColor.red
            }
            else{
                nonGMOImg.tintColor = UIColor.green
            }
            rainForestImg.image = UIImage(systemName: checkDic[scoreDic["rainforest alliance"]!]!)
            if (checkDic[scoreDic["rainforest alliance"]!]!) == ("xmark.seal.fill"){
                rainForestImg.tintColor = UIColor.red
            }
            else{
                rainForestImg.tintColor = UIColor.green
            }
         
            
        } else{
            // Fallback on earlier versions
        }
        
       
        
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}


