// Run from the repository root: swift scripts/render_social_card.swift
import AppKit
let size = NSSize(width: 1200, height: 630)
let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: 1200, pixelsHigh: 630, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
NSColor(calibratedRed: 0.965, green: 0.972, blue: 0.99, alpha: 1).setFill()
NSBezierPath(rect: NSRect(origin: .zero, size: size)).fill()
func text(_ string: String, _ x: CGFloat, _ y: CGFloat, _ size: CGFloat, _ weight: NSFont.Weight, _ color: NSColor) {
    (string as NSString).draw(at: NSPoint(x: x, y: y), withAttributes: [.font: NSFont.systemFont(ofSize: size, weight: weight), .foregroundColor: color])
}
let ink = NSColor(calibratedRed: 0.08, green: 0.1, blue: 0.18, alpha: 1)
let purple = NSColor(calibratedRed: 0.32, green: 0.28, blue: 0.8, alpha: 1)
NSImage(contentsOfFile: "app-icon.png")!.draw(in: NSRect(x: 70, y: 481, width: 64, height: 64))
text("iPerf Falcon", 151, 493, 32, .bold, ink)
text("Your network.", 70, 333, 76, .bold, ink)
text("In clear view.", 70, 243, 76, .bold, purple)
text("Native iPerf3 + iPerf2 throughput testing", 74, 157, 27, .regular, ink)
text("iPhone  ·  iPad  ·  Mac  ·  Android", 74, 88, 23, .medium, purple)
let path = NSBezierPath()
path.lineWidth = 15
path.lineCapStyle = .round
path.move(to: NSPoint(x: 828, y: 240))
path.curve(to: NSPoint(x: 1120, y: 426), controlPoint1: NSPoint(x: 730, y: 550), controlPoint2: NSPoint(x: 1090, y: 600))
purple.setStroke(); path.stroke()
let signal = NSBezierPath()
signal.lineWidth = 8; signal.lineCapStyle = .round
signal.move(to: NSPoint(x: 875, y: 300)); signal.line(to: NSPoint(x: 925, y: 355)); signal.line(to: NSPoint(x: 970, y: 334)); signal.line(to: NSPoint(x: 1040, y: 420))
NSColor(calibratedRed: 0, green: 0.49, blue: 0.55, alpha: 1).setStroke(); signal.stroke()
NSGraphicsContext.restoreGraphicsState()
try bitmap.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: "assets/social-card.png"))
