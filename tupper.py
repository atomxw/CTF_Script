import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
 

def Tupper_self_referential_formula(k): 
    aa = np.zeros((17,106))
    def f(x, y):
        y += k
        a1 = 2**-(-17*x - y%17)
        a2 = (y // 17) // a1
        return 1 if a2 % 2 > 0.5 else 0
    for y in range(17):
        for x in range(106):
            aa[y, x] = f(x, y) 
    return aa[:,::-1]
 
k = 1594199391770250354455183081054802631580554590456781276981302978243348088576774816981145460077422136047780972200375212293357383685099969525103172039042888918139627966684645793042724447954308373948403404873262837470923601139156304668538304057819343713500158029312192443296076902692735780417298059011568971988619463802818660736654049870484193411780158317168232187100668526865378478661078082009408188033574841574337151898932291631715135266804518790328831268881702387643369637508117317249879868707531954723945940226278368605203277838681081840279552  #输入你要提取的k
aa = Tupper_self_referential_formula(k)
plt.figure(figsize=(15,10))
plt.imshow(aa,origin='lower')
plt.savefig("tupper.png")
img = Image.open('tupper.png')
#翻转
dst1 = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
plt.imshow(dst1)
plt.show()