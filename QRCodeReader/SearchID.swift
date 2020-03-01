//
//  SearchID.swift
//  QRCodeReader
//
//  Created by Vishesh Dhawan on 2/29/20.
//  Copyright © 2020 AppCoda. All rights reserved.
//

import UIKit
import AVFoundation
import AVKit

class ViewController: UIViewController {

    //override func viewDidLoad() {
        //super.viewDidLoad()

        // Do any additional setup after loading the view.
    @IBAction func onGetTapped(_ sender: Any) {
        guard let url = URL(string:"https://api.upcitemdb.com/prod/trial/lookup?upc\(barcode)") else {
            return }
        let _ = URLSession.shared
        URLSession.shared.dataTask(with: url) { (data, response, error) in
            if let response = response {
                print(response)
            }
            if let data = data {
                print(data)
            }
        }.resume()
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


