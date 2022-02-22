#===========================================================
#
# Title:      Image Edge Detection
# Author:     Dan Ouellette
# Description:
#   This Python application performs edge detection on an
# Mach-E image.  It creates a gray-scale version of the
# image and then detects its edges.  It requires module 
# cImage to be downloaded and installed.  The application
# takes about five minutes to run on an image with
# dimensions 2,560 x 1,709.
#
#===========================================================
  
#-----------------------------------------------------------
# Imports
#-----------------------------------------------------------
import image
import math

#-----------------------------------------------------------
# analyzeImage
#-----------------------------------------------------------
def analyzeImage(inImage):

  # Create image object
  i = image.FileImage(inImage)
  
  # Analyze image
  print("Analyzing image '", inImage, "'...", sep="")
  w = i.getWidth()
  h = i.getHeight()
  print("Image width:", w)
  print("Image height:", h)
  print()
      
#-----------------------------------------------------------
# edgeImage
#   This function requires a grayscale image.
#-----------------------------------------------------------
def edgeImage(inImage, edgedImage):
  
  # Create convolution objects
  pxlBlack = image.Pixel(0, 0, 0)
  pxlWhite = image.Pixel(255, 255, 255)
  XMask = [ [-1,-2,-1],[0,0,0],[1,2,1] ]
  YMask = [ [1,0,-1],[2,0,-2],[1,0,-1] ]
  threshold = 175

  # Create image objects
  i = image.FileImage(inImage)
  w = i.getWidth()
  h = i.getHeight()
  o = image.EmptyImage(w, h)
  
  # Print source and target image names
  print("Edging image '", inImage, "' with ", h, \
    " rows ...", sep="")
  print("Source image:", inImage)
  print("Target:", edgedImage)
  print()
  
  # Loop to detect edges
  print("Edging started ...")
  for row in range(1, h - 1):
    if row % (h // 8) == 0: print("In image row", row, "...")
    for col in range(1, w - 1):

      # Convolve pixel
      distanceX = edgeImageConvolve(i, row, col, XMask)
      distanceY = edgeImageConvolve(i, row, col, YMask)
      distanceZ = math.sqrt(distanceX**2 + distanceY**2)

      # Test if edge detected
      if distanceZ > threshold:
        o.setPixel(col, row, pxlBlack)
      else:
        o.setPixel(col, row, pxlWhite)

  print("Edging ended.")
      
  # Save flipped image
  o.save(edgedImage)

#-----------------------------------------------------------
# edgeImageConvolve
#-----------------------------------------------------------
def edgeImageConvolve(img, imgRow, imgCol, kernel):

  # Set base for kernel in image
  kernelBaseCol = imgCol - 1
  kernelBaseRow = imgRow - 1
  
  # Loop to get convolution sum
  sum = 0
  for row in range(kernelBaseRow, kernelBaseRow + 3):
    for col in range(kernelBaseCol, kernelBaseCol + 3):
    
      # Get kernel indexes
      kernelIndexCol = col - kernelBaseCol
      kernelIndexRow = row - kernelBaseRow
      
      # Get image pixel intensity
      pxl = img.getPixel(col, row)
      intensity = pxl.getRed()
      
      # Multiply corresponding intensity and kernel value
      sum = sum + intensity * \
        kernel[kernelIndexRow][kernelIndexCol]
      
  return sum

#-----------------------------------------------------------
# grayscaleImage
#-----------------------------------------------------------
def grayscaleImage(inImage, grayedImage):

  # Create image objects
  i = image.FileImage(inImage)
  w = i.getWidth()
  h = i.getHeight()
  o = image.EmptyImage(w, h)
  
  # Print source and target image names
  print("Grayscaling image '", inImage, "' with ", h, \
    " rows ...", sep="")
  print("Source image:", inImage)
  print("Target:", grayedImage)
  print()
  
  # Loop to grayscale pixels
  print("Grayscaling started ...")
  for row in range(h):
    if row % (h // 4) == 0: print("In image row", row, "...")
    for col in range(w):
      pxlSource = i.getPixel(col, row)	
      newGray = (pxlSource.getRed() + pxlSource.getGreen() + \
        pxlSource.getBlue()) // 3
      pxlTarget = image.Pixel(newGray, newGray, newGray)
      o.setPixel(col, row, pxlTarget)
  print("Grayscaling ended.")
  print()
  
  # Save grayscale image
  o.save(grayedImage)

#-----------------------------------------------------------
# Main
#-----------------------------------------------------------

# Set variables
inImage = "MachE.jfif"
grayImage = "MachE-grayed.png"
edgedImage = "MachE-edged.png"

# Show application header
print ("Welcome to Image Edge Detection")
print ("-------------------------------\n")

# Analyze, grayscale, and edge image
analyzeImage (inImage)
grayscaleImage(inImage, grayImage)
edgeImage(inImage, edgedImage)

# Show application close
print ("\nEnd of Image Edge Detection")
