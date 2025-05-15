import numpy as np
import math

def XYZ_to_Lab(X, Y, Z):
    e = 0.008856
    k = 903.3
    xr = X/D50_XYZ[0]
    yr = Y/D50_XYZ[1]
    zr = Z/D50_XYZ[2]
    #print("xr, yr, zr is: ", xr, yr, zr)
    if xr > e:
        fx = xr ** (1/3)
    else:
        fx = (k * xr + 16)/116
    if yr > e:
        fy = yr ** (1/3)
    else:
        fy = (k * yr + 16)/116
    if zr > e:
        fz = zr ** (1/3)
    else:
        fz = (k * zr + 16)/116
    #print("fx, fy, fz is: ", fx, fy, fz)

    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)
    return L, a, b

def sRGB_to_XYZ(RGB):
    # Normalize the sRGB values
    RGB = [x / 255.0 for x in RGB]

    RGB_inv = [0, 0, 0]
    # Inverse Companding for sRGB
    for i in range(3):
        if RGB[i] <= 0.04045:
            RGB_inv[i] = RGB[i] / 12.92
        else:
            RGB_inv[i] = math.pow(((RGB[i] + 0.055) / 1.055), 2.4)
    XYZ = np.dot(sRGB_to_XYZ_matrices, RGB_inv)
    return XYZ

def sRGB_to_Lab(sRGB):
    XYZ = sRGB_to_XYZ(sRGB)
    XYZ_D50 = np.dot(bradford_adaption_d65_d50, XYZ)
    Lab = XYZ_to_Lab(XYZ_D50[0], XYZ_D50[1], XYZ_D50[2])
    print("Converted Lab is: ", Lab[0], Lab[1], Lab[2])
    return Lab

D50_XYZ = np.array([0.96422, 1, 0.82521]) # Xr for illuminant D50 and 2 degree observer function
D65_XYZ = np.array([0.95047, 1, 1.08883])

sRGB_to_XYZ_matrices = [[0.4124564, 0.3575761, 0.1804375],
                        [0.2126729, 0.7151522, 0.0721750],
                        [0.0193339, 0.1191920, 0.9503041]]

bradford_adaption_d65_d50 = [[1.0478112, 0.0228866, -0.0501270],
                             [0.0295424, 0.9904844, -0.0170491],
                             [-0.0092345, 0.0150436, 0.7521316]]



# Run the code below
sRGB = [176.8792173, 165.8431174, 9.550607287]
sRGB_to_Lab(sRGB)
