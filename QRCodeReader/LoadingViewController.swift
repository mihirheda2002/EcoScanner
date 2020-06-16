//
//  LoadingViewController.swift
//  QRCodeReader
//
//  Created by Vishesh Dhawan on 6/15/20.
//  Copyright © 2020 AppCoda. All rights reserved.
//

import UIKit
import SwiftGifOrigin
import ImageIO


class LoadingViewController: UIViewController {

    @IBOutlet var loadingEarth: UIImageView!
    
   
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let tempGif = UIImage.gif(name: "giphy")
        loadingEarth.image = tempGif
        

        // Do any additional setup after loading the view.
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
