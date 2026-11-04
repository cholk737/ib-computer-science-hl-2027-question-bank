import Foundation
import Vision
import AppKit
let args=CommandLine.arguments.dropFirst()
for path in args {
 guard let image=NSImage(contentsOfFile:path), let data=image.tiffRepresentation, let rep=NSBitmapImageRep(data:data), let cg=rep.cgImage else {continue}
 let req=VNRecognizeTextRequest()
 req.recognitionLevel = .accurate
 req.usesLanguageCorrection = false
 try VNImageRequestHandler(cgImage:cg).perform([req])
 let out=(req.results ?? []).sorted { a,b in
  if abs(a.boundingBox.midY-b.boundingBox.midY)>0.005{return a.boundingBox.midY>b.boundingBox.midY}
  return a.boundingBox.minX<b.boundingBox.minX
 }.map { $0.topCandidates(1).first?.string ?? "" }.joined(separator:"\n")
 try out.write(toFile:path+".txt", atomically:true, encoding:.utf8)
}
