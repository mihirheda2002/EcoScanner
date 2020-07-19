//
//  QRScannerController.swift
//  QRCodeReader
//
//  Created by Simon Ng on 13/10/2016.
//  Copyright © 2016 AppCoda. All rights reserved.
//

import UIKit
import AVFoundation

var barcode = ""
var json = ""
var name = ""
var price = ""
var description = ""

class QRScannerController: UIViewController {
    
    let notFoundVC = mainBoard.instantiateViewController(withIdentifier:"BarcodeNotFoundViewController") as! BarcodeNotFoundViewController
    let foundVC = mainBoard.instantiateViewController(withIdentifier:"ScoreViewController") as! ScoreViewController

    @IBOutlet var messageLabel:UILabel!
    @IBOutlet var topbar: UIView!
    
    var captureSession = AVCaptureSession()
    
    var videoPreviewLayer: AVCaptureVideoPreviewLayer?
    var qrCodeFrameView: UIView?

    private let supportedCodeTypes = [AVMetadataObject.ObjectType.upce,
                                      AVMetadataObject.ObjectType.code39,
                                      AVMetadataObject.ObjectType.code39Mod43,
                                      AVMetadataObject.ObjectType.code93,
                                      AVMetadataObject.ObjectType.code128,
                                      AVMetadataObject.ObjectType.ean8,
                                      AVMetadataObject.ObjectType.ean13,
                                      AVMetadataObject.ObjectType.aztec,
                                      AVMetadataObject.ObjectType.pdf417,
                                      AVMetadataObject.ObjectType.itf14,
                                      AVMetadataObject.ObjectType.dataMatrix,
                                      AVMetadataObject.ObjectType.interleaved2of5,
                                      AVMetadataObject.ObjectType.qr]
   
    override func viewDidLoad() {
        super.viewDidLoad()

        // Get the back-facing camera for capturing videos
        barcode = ""
        json = ""
        name = ""
        price = ""
        
        print("scanner view did load")
        guard let captureDevice = AVCaptureDevice.default(for: AVMediaType.video) else {
            print("Failed to get the camera device")
            return
        }
        
        do {
            print("do func in view did load")
            // Get an instance of the AVCaptureDeviceInput class using the previous device object.
            let input = try AVCaptureDeviceInput(device: captureDevice)
            
            // Set the input device on the capture session.
            captureSession.addInput(input)
            
            // Initialize a AVCaptureMetadataOutput object and set it as the output device to the capture session.
            let captureMetadataOutput = AVCaptureMetadataOutput()
            captureSession.addOutput(captureMetadataOutput)
            
            // Set delegate and use the default dispatch queue to execute the call back
            captureMetadataOutput.setMetadataObjectsDelegate(self, queue: DispatchQueue.main)
            captureMetadataOutput.metadataObjectTypes = supportedCodeTypes
//            captureMetadataOutput.metadataObjectTypes = [AVMetadataObject.ObjectType.qr]
            
        } catch {
            // If any error occurs, simply print it out and don't continue any more.
            print(error)
            return
        }
        
        // Initialize the video preview layer and add it as a sublayer to the viewPreview view's layer.
        videoPreviewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
        videoPreviewLayer?.videoGravity = AVLayerVideoGravity.resizeAspectFill
        videoPreviewLayer?.frame = view.layer.bounds
        view.layer.addSublayer(videoPreviewLayer!)
        
        // Start video capture.
        captureSession.startRunning()
        
        // Move the message label and top bar to the front
        view.bringSubviewToFront(messageLabel)
        view.bringSubviewToFront(topbar)
        
        // Initialize QR Code Frame to highlight the QR code
        qrCodeFrameView = UIView()
        
        if let qrCodeFrameView = qrCodeFrameView {
            qrCodeFrameView.layer.borderColor = UIColor.green.cgColor
            qrCodeFrameView.layer.borderWidth = 2
            view.addSubview(qrCodeFrameView)
            view.bringSubviewToFront(qrCodeFrameView)
        }
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    // MARK: - Helper methods

    func launchApp(decodedURL: String) {
        print("launching app")
        json = ""
        
        if presentedViewController != nil {
            return
        }
        
        let alertPrompt = UIAlertController(title: "Open App", message: "You're going to open \(decodedURL)", preferredStyle: .actionSheet)
        let confirmAction = UIAlertAction(title: "Confirm", style: UIAlertAction.Style.default, handler: { (action) -> Void in
            
           /*if let url = URL(string: decodedURL) {
                if UIApplication.shared.canOpenURL(url) {
                    UIApplication.shared.open(url)
                }
            }
 */
           
            //self.performSegue(withIdentifier: "showSVC", sender: self)
            
            let link = "http://35.153.34.57/scan/"+barcode
                print(link)
            
           /*     if let url = URL(string: link) {
                URLSession.shared.dataTask(with: url) { data, response, error in
                   if let data = data {
                      if let jsonString = String(data: data, encoding: .utf8) {
                         json = jsonString
                         print("printing jsonString")
                         print(jsonString)
                      }
                    }
                }.resume()
                
                self.performSegue(withIdentifier: "scannerToLoading", sender: self)
                 
                 /*while json.isEmpty{
                     print("checking if empty" + barcode)
                     //print(json)
                     if !(json.isEmpty){
                         let jsonParts = json.components(separatedBy: " ")
                         print(jsonParts)
                         if jsonParts.contains("found\"\n}\n") || jsonParts.contains("!DOCTYPE"){
                            print("so the if statement worked bc the data was not found but like why isnt it working doe")
                            //self.navigationController?.pushViewController(notFoundVC, animated: true)
                            //self.present(self.notFoundVC, animated: true, completion: nil)
                            //self.present(notFoundVC, animated: true, completion: nil)
                            self.performSegue(withIdentifier: "showNFVC", sender: self)
                         }
                         else{
                            self.foundVC.text = json
                            //self.present(self.foundVC, animated: true, completion: nil)
                            self.performSegue(withIdentifier: "showSVC", sender: self)
                         }
                     }
                 }*/
                
            }*/
        })
        
        let cancelAction = UIAlertAction(title: "Cancel", style: UIAlertAction.Style.cancel, handler: nil)
        
        alertPrompt.addAction(confirmAction)
        alertPrompt.addAction(cancelAction)
        
        present(alertPrompt, animated: true, completion: nil)
    }
  private func updatePreviewLayer(layer: AVCaptureConnection, orientation: AVCaptureVideoOrientation) {
    layer.videoOrientation = orientation
    videoPreviewLayer?.frame = self.view.bounds
  }
  
  override func viewDidLayoutSubviews() {
    super.viewDidLayoutSubviews()
    
    if let connection =  self.videoPreviewLayer?.connection  {
      let currentDevice: UIDevice = UIDevice.current
      let orientation: UIDeviceOrientation = currentDevice.orientation
      let previewLayerConnection : AVCaptureConnection = connection
      
      if previewLayerConnection.isVideoOrientationSupported {
        switch (orientation) {
        case .portrait:
          updatePreviewLayer(layer: previewLayerConnection, orientation: .portrait)
          break
        case .landscapeRight:
          updatePreviewLayer(layer: previewLayerConnection, orientation: .landscapeLeft)
          break
        case .landscapeLeft:
          updatePreviewLayer(layer: previewLayerConnection, orientation: .landscapeRight)
          break
        case .portraitUpsideDown:
          updatePreviewLayer(layer: previewLayerConnection, orientation: .portraitUpsideDown)
          break
        default:
          updatePreviewLayer(layer: previewLayerConnection, orientation: .portrait)
          break
        }
      }
    }
  }

}

extension QRScannerController: AVCaptureMetadataOutputObjectsDelegate {
    
    func metadataOutput(_ output: AVCaptureMetadataOutput, didOutput metadataObjects: [AVMetadataObject], from connection: AVCaptureConnection) {
        // Check if the metadataObjects array is not nil and it contains at least one object.
        if metadataObjects.count == 0 {
            qrCodeFrameView?.frame = CGRect.zero
            messageLabel.text = "No QR code is detected"
            return
        }
        
        if barcode == "" {
            // Get the metadata object.
            let metadataObj = metadataObjects[0] as! AVMetadataMachineReadableCodeObject
            
            barcode = metadataObj.stringValue ?? "0"
            print(barcode)
            print(barcode.count)
            if barcode.count == 13 {
                let range = barcode.index(after: barcode.startIndex)..<barcode.endIndex
                let tempBarcode = barcode[range]
                barcode = String(tempBarcode)
            }
            
            if supportedCodeTypes.contains(metadataObj.type) {
                // If the found metadata is equal to the QR code metadata (or barcode) then update the status label's text and set the bounds
                let barCodeObject = videoPreviewLayer?.transformedMetadataObject(for: metadataObj)
                qrCodeFrameView?.frame = barCodeObject!.bounds
                
                if metadataObj.stringValue != nil {
                    launchApp(decodedURL: barcode)
                    messageLabel.text = barcode
                    
                    
                   /* let link = "http://34.201.212.152/scan/"+barcode
                    print(link)
                    if let url = URL(string: link) {
                    URLSession.shared.dataTask(with: url) { data, response, error in
                       if let data = data {
                          if let jsonString = String(data: data, encoding: .utf8) {
                             json = jsonString
                             print("printing jsonString")
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
                                present(foundVC, animated: true, completion: nil)
                             }
                         }
                     }
                    
                }
 */
            }
        }
    }
    }
}
