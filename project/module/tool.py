import cv2


def read_imgfile(path,width=None,height=None):
    val_image = cv2.imread(path,cv2.IMREAD_COLOR)
    if width is not None and height is not None:
        val_image = cv2.resize(val_image,(width,height))
    return val_image