# --------------------------------------------------------
# Faster R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick and Sean Bell
# --------------------------------------------------------

import numpy as np

# Verify that we compute the same anchors as Shaoqing's matlab implementation:
#
#    >> load output/rpn_cachedir/faster_rcnn_VOC2007_ZF_stage1_rpn/anchors.mat
#    >> anchors
#
#    anchors =
#
#       -83   -39   100    56
#      -175   -87   192   104
#      -359  -183   376   200
#       -55   -55    72    72
#      -119  -119   136   136
#      -247  -247   264   264
#       -35   -79    52    96
#       -79  -167    96   184
#      -167  -343   184   360

#array([[ -83.,  -39.,  100.,   56.],
#       [-175.,  -87.,  192.,  104.],
#       [-359., -183.,  376.,  200.],
#       [ -55.,  -55.,   72.,   72.],
#       [-119., -119.,  136.,  136.],
#       [-247., -247.,  264.,  264.],
#       [ -35.,  -79.,   52.,   96.],
#       [ -79., -167.,   96.,  184.],
#       [-167., -343.,  184.,  360.]])

def generate_anchors(base_size=16, ratios=[0.5, 1, 2],
                     scales=2**np.arange(3, 6)): #2^[3 4 5] = 8 16 32. base window = 16x16 --> anchors = (16x16)*[8 16 32] = (128x128), (256x256), (512x512)
    """
    ratios la ti le giua heigh and width
    Generate anchor (reference) windows by enumerating aspect ratios X
    scales wrt a reference (0, 0, 15, 15) = 16x16 window.
    """

    base_anchor = np.array([1, 1, base_size, base_size]) - 1
    #print base_anchor -->[ 0  0 15 15]
    ratio_anchors = _ratio_enum(base_anchor, ratios) # = _ratio_enum(base_anchor = [ 0  0 15 15], ratios=[0.5, 1, 2])
    anchors = np.vstack([_scale_enum(ratio_anchors[i, :], scales)
                         for i in range(ratio_anchors.shape[0])])
    return anchors

def _whctrs(anchor):
    """
    Return width, height, x center, and y center for an anchor (window).
    """

    w = anchor[2] - anchor[0] + 1
    h = anchor[3] - anchor[1] + 1
    x_ctr = anchor[0] + 0.5 * (w - 1)
    y_ctr = anchor[1] + 0.5 * (h - 1)
    return w, h, x_ctr, y_ctr

def _mkanchors(ws, hs, x_ctr, y_ctr):
    """
    Given a vector of widths (ws) and heights (hs) around a center
    (x_ctr, y_ctr), output a set of anchors (windows).
    """

    ws = ws[:, np.newaxis]
    hs = hs[:, np.newaxis]
    anchors = np.hstack((x_ctr - 0.5 * (ws - 1),
                         y_ctr - 0.5 * (hs - 1),
                         x_ctr + 0.5 * (ws - 1),
                         y_ctr + 0.5 * (hs - 1)))
    return anchors

def _ratio_enum(anchor, ratios):

    """
    ratios=[0.5, 1, 2] ti le 
    Enumerate a set of anchors for each aspect ratio wrt an anchor.
    """
    w, h, x_ctr, y_ctr = _whctrs(anchor) # = _whctrs([ 0  0 15 15])  = 16 16 7.5 7.5 center la 7.5, 7.5, w = 16, h = 16
    #print w, h, x_ctr, y_ctr ==> 16 16 7.5 7.5
    size = w * h # = 16*16 = 256: area of reference window
    size_ratios = size / ratios # 256 / [0.5, 1, 2] = [ 512.  256.  128.]

    ws = np.round(np.sqrt(size_ratios)) # = round(sqrt([512.  256.  128.])) = [ 23.  16.  11.] ==> de co dien tich 512 thi tuong ung hinh vuong canh la 23*23. sau khi co canh nay roi thi fix canh nay, tinh canh con lai
    hs = np.round(ws * ratios) # =  round([ 23.  16.  11.] * [0.5, 1, 2]) =   [ 12.  16.  22.]

    anchors = _mkanchors(ws, hs, x_ctr, y_ctr)
    #print  anchors
    '''
        [[ -3.5   2.   18.5  13. ] #ws = 18.5 -- 3.5 + 1= 23. hs = 13-2+1 = 12 
        [  0.    0.   15.   15. ]  #ws = 15-0+1 = 16. hs = 15-0+1 = 16
        [  2.5  -3.   12.5  18. ]] #ws = 12.5-2.5+1 = 11. hs = 18--3+1 = 22
    '''
    return anchors

def _scale_enum(anchor, scales):
    """
    Enumerate a set of anchors for each scale wrt an anchor.
    """

    w, h, x_ctr, y_ctr = _whctrs(anchor)
    ws = w * scales
    hs = h * scales
    anchors = _mkanchors(ws, hs, x_ctr, y_ctr)
    return anchors

if __name__ == '__main__':
    import time
    t = time.time()
    a = generate_anchors()
    print((time.time() - t))
    print(a)
    from IPython import embed; embed()
