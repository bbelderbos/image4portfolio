#!/usr/bin/python
# -*- coding: utf-8 -*- 
#
# Author: @bbelderbos
# Date: 25/10/2015
# Purpose: resize and watermark images for portfolio
# Script requirements: PIL (python2.7)
#
import glob
import os
import re
import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
 
class Portfolio:

  def __init__(self, directory="server/php/files"):
    self.directory = directory
    self.delimit = "__"
    self.doneStr = "resized"
    self.doneStrDimensions = self.delimit.join([self.doneStr, "XXX", "YYY"]) + self.delimit
    self.getBaseFname = re.compile(r'.*%s(.*)$'%self.delimit)
    self.font = 'Arial.ttf'
    if not os.path.isdir(self.directory):
      sys.exit("%s directory not found" % self.directory)
    self.imageQueue = self._get_images_to_process()

  def _get_images_to_process(self):
    images = []
    for im in glob.glob(os.path.join(self.directory, "*")):
      fname = os.path.basename(im)
      if fname.startswith(self.doneStr):
        continue
      if len(glob.glob(os.path.join(self.directory, "*"+self.getBaseFname.sub(r'\1', fname)))) > 1:
        continue
      images.append(fname)
    return images

  def resize_image(self, image, width):
    """ modified source from http://pythoncentral.io/resize-image-python-batch/ """
    try:
      width = int(width)
    except:
      raise ValueError("Provide width (%s) is not an integer value" % str(width))
    imagePath = os.path.join(self.directory, image)
    if not os.path.isfile(imagePath):
      raise IOError("Image path not found: %s" % imagePath)
    img = Image.open(imagePath)
    # Calculate the height using the same aspect ratio
    widthPercent = (width / float(img.size[0]))
    height = int((float(img.size[1]) * float(widthPercent)))
    img = img.resize((width, height), Image.BILINEAR)
    resultImg = os.path.join(self.directory, self.doneStrDimensions.replace("XXX", str(width)).replace("YYY", str(height)) + image)
    img.save(resultImg)
    return resultImg

  def watermark_image(self, image, text, angle=23, opacity=0.25):
    """ modified source from http://pythoncentral.io/watermark-images-python-2x/ """
    img = Image.open(image).convert('RGB')
    watermark = Image.new('RGBA', img.size, (0,0,0,0))
    size = 2
    n_font = ImageFont.truetype(self.font, size)
    n_width, n_height = n_font.getsize(text)
    while n_width+n_height < watermark.size[0]:
        size += 2
        n_font = ImageFont.truetype(self.font, size)
        n_width, n_height = n_font.getsize(text)
    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - n_width) / 2,
              (watermark.size[1] - n_height) / 2),
              text, font=n_font)
    watermark = watermark.rotate(angle,Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    Image.composite(watermark, img, watermark).save(image, 'JPEG') # if new file, change image var

  def _get_resized_images(self):
    """ returns list of images in directory ordered desc by modification time """
    imgs = []
    for im in reversed(sorted(glob.glob(os.path.join(self.directory, "%s*"%self.doneStr)), key=os.path.getmtime)):
      imgs.append(im)
    return imgs

  def list_images(self, html=False):
    out = ["<ul>"] if html else []
    imgs = self._get_resized_images()
    for i in imgs:
      if html: 
        out.append("<li><a target='_blank' href='%s'>%s</a></li>" % (i,i))
      else:
        out.append(i)
    if html: out.append("</ul>")
    print "\n".join(out)


if __name__ == "__main__":
  if len(sys.argv) < 4:
    sys.exit("%s thumbWidth fullWidth watermarkText" % sys.argv[0])
  p = Portfolio()
  thumbWidth = sys.argv[1]
  fullWidth = sys.argv[2]
  watermarkText = sys.argv[3]
  for im in p.imageQueue:
    thumbImg = p.resize_image(im, thumbWidth)
    zoomImg = p.resize_image(im, fullWidth)
    p.watermark_image(zoomImg, watermarkText)
    print thumbImg
    print zoomImg
