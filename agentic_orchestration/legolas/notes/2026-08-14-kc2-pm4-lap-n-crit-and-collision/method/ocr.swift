import Foundation
import Vision
import AppKit

// Reads image paths from argv, emits TSV: path \t text \t conf \t x \t y \t w \t h
let args = Array(CommandLine.arguments.dropFirst())
for path in args {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        FileHandle.standardError.write("ERR load \(path)\n".data(using: .utf8)!)
        continue
    }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.usesLanguageCorrection = false
    req.recognitionLanguages = ["en-US"]
    req.minimumTextHeight = 0.004
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    do { try handler.perform([req]) } catch {
        FileHandle.standardError.write("ERR perform \(path)\n".data(using: .utf8)!)
        continue
    }
    guard let obs = req.results else { continue }
    for o in obs {
        guard let c = o.topCandidates(1).first else { continue }
        let b = o.boundingBox
        let line = "\(path)\t\(c.string)\t\(c.confidence)\t\(b.origin.x)\t\(b.origin.y)\t\(b.size.width)\t\(b.size.height)\n"
        FileHandle.standardOutput.write(line.data(using: .utf8)!)
    }
}
