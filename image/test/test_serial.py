# -*- python -*-
#
#       image: image manipulation GUI
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
Test frame manipulator
"""

__license__= "Cecill-C"
__revision__ = " $Id: __init__.py 2245 2010-02-08 17:11:34Z cokelaer $ "

from numpy import array
from openalea.image import save,load,SpatialImage,rainbow

#create image
data = array(range(30000) ).reshape( (100,300) )

pal = rainbow(30000)

img = pal[data]

sp = SpatialImage(img,(0.5,0.6),vdim = 3)

#save
save("00_data",data)
save("00_img",img)
save("00_sp",sp)

#load
rdata = load("00_data.npy")
rimg = load("00_img.npy")
rsp = load("00_sp.npy")

assert (rdata == data).all()
assert (rimg == img).all()
assert (rsp == sp).all()

assert hasattr(rsp,"resolution")
assert rsp.resolution == sp.resolution
assert hasattr(rsp,"info")


