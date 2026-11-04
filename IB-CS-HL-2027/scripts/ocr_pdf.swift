// Local Apple Vision OCR aid. Originals are never changed. Visual review required.
import Foundation
import PDFKit
import Vision
import AppKit

let args = CommandLine.arguments
guard args.count == 3, let pdf = PDFDocument(url: URL(fileURLWithPath: args[1])) else {
    fatalError("Usage: ocr_pdf.swift input.pdf output-directory")
}
let out = URL(fileURLWithPath: args[2], isDirectory: true)
try FileManager.default.createDirectory(at: out, withIntermediateDirectories: true)
for i in 0..<pdf.pageCount {
    guard let page = pdf.page(at: i) else { continue }
    let box = page.bounds(for: .mediaBox)
    let thumb = page.thumbnail(of: NSSize(width: box.width * 3, height: box.height * 3), for: .mediaBox)
    var rect = CGRect(origin: .zero, size: thumb.size)
    guard let cg = thumb.cgImage(forProposedRect: &rect, context: nil, hints: nil) else { continue }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    req.recognitionLanguages = ["en-US"]
    try VNImageRequestHandler(cgImage: cg).perform([req])
    let observations = (req.results ?? []).sorted {
        abs($0.boundingBox.midY - $1.boundingBox.midY) > 0.006
          ? $0.boundingBox.midY > $1.boundingBox.midY : $0.boundingBox.minX < $1.boundingBox.minX
    }
    let lines: [[String: Any]] = observations.compactMap { o in
        guard let t = o.topCandidates(1).first else { return nil }
        return ["text": t.string, "confidence": t.confidence,
                "bbox": [o.boundingBox.minX, o.boundingBox.minY, o.boundingBox.width, o.boundingBox.height]]
    }
    let data = try JSONSerialization.data(withJSONObject: ["pdf_page": i+1, "lines": lines], options: [.prettyPrinted, .sortedKeys])
    let stem = String(format: "page-%03d", i+1)
    try data.write(to: out.appendingPathComponent(stem + ".json"))
    try lines.map { $0["text"] as! String }.joined(separator: "\n").write(to: out.appendingPathComponent(stem + ".txt"), atomically: true, encoding: .utf8)
    print("OCR aid saved PDF page \(i+1)/\(pdf.pageCount)")
}
