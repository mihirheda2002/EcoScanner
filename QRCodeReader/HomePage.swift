//
//  HomePage.swift
//  QRCodeReader
//
//  Created by Vishesh Dhawan on 2/29/20.
//  Copyright © 2020 AppCoda. All rights reserved.
//

import UIKit

class HomePage: UIViewController {
    @IBOutlet weak var backgroundImage: UIImageView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        backgroundImage.contentMode = .scaleAspectFill
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
