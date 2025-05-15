import numpy as np
import math

def compute_xyz_from_spectral_data(S, I, x_bar, y_bar, z_bar, delta_lambda):
    """
    Compute the XYZ values from spectral data.

    Parameters:
    S (numpy array): Spectral reflectance or transmittance of the sample.
    I (numpy array): Spectral power distribution of the reference illuminant.
    x_bar (numpy array): Color matching function for X.
    y_bar (numpy array): Color matching function for Y.
    z_bar (numpy array): Color matching function for Z.
    delta_lambda (float): The wavelength interval.

    Returns:
    tuple: A tuple containing the computed (X, Y, Z) values.
    """

    # Compute the normalization factor N
    N = np.sum(y_bar * I * delta_lambda)

    # Compute the X, Y, Z values
    X = (1 / N) * np.sum(x_bar * S * I * delta_lambda)
    Y = (1 / N) * np.sum(y_bar * S * I * delta_lambda)
    Z = (1 / N) * np.sum(z_bar * S * I * delta_lambda)

    return X, Y, Z


def get_user_input(prompt):
    """
    Get a list of floats from user input.

    Parameters:
    prompt (str): The prompt message to display to the user.

    Returns:
    numpy array: An array of floats entered by the user.
    """
    values = input(prompt)
    return np.array([float(value) for value in values.split()])

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

def XYZ_to_sRGB (XYZ):
    XYZ_d65_to_sRGB_linear = np.dot(XYZ_to_sRGB_matrices, XYZ)
    for i in range (0,3):
        if XYZ_d65_to_sRGB_linear[i] <= 0.0031308: # sRGB companding
            XYZ_d65_to_sRGB_linear[i] = 12.92 * XYZ_d65_to_sRGB_linear[i]
        else:
            XYZ_d65_to_sRGB_linear[i] = 1.055 * math.pow(XYZ_d65_to_sRGB_linear[i], 1/2.4) - 0.055 # sRGB companding
    XYZ_d65_to_sRGB_scale = XYZ_d65_to_sRGB_linear * 255 # scale to 0-255 range
    print("XYZ d65 to sRGB (0-255) is: ", XYZ_d65_to_sRGB_scale)

def XYZ_to_CIERGB(XYZ):
    XYZ_E_to_CIERGB = np.dot(XYZ_to_CIERGB_matrices, XYZ)
    for i in range (0,3):
        XYZ_E_to_CIERGB[i] = math.pow(XYZ_E_to_CIERGB[i], 1/2.2) # Gamma Companding
    XYZ_E_to_CIERGB = XYZ_E_to_CIERGB * 255
    print("XYZ E to CIERGB (0-255) is: ", XYZ_E_to_CIERGB)


# Example static data
I = np.array([
    49.30, 56.50, 60.00, 57.80, 74.80, 87.20, 90.60, 91.40, 95.20, 92.00,
    95.70, 96.60, 97.10, 102.10, 100.80, 102.30, 100.00, 97.70, 98.90, 93.50,
    97.70, 99.30, 99.00, 95.70, 98.80, 95.70, 98.20, 103.00, 99.10, 87.40, 91.60
])  # Spectral power distribution of the reference illuminant
x_bar = np.array([
    0.014310, 0.043510, 0.134380, 0.283900, 0.348280, 0.336200, 0.290800, 0.195360,
    0.095640, 0.032010, 0.004900, 0.009300, 0.063270, 0.165500, 0.290400, 0.433450,
    0.594500, 0.762100, 0.916300, 1.026300, 1.062200, 1.002600, 0.854450, 0.642400,
    0.447900, 0.283500, 0.164900, 0.087400, 0.046770, 0.022700, 0.011359
])  # Color matching function for X
y_bar = np.array([
    0.000396, 0.001210, 0.004000, 0.011600, 0.023000, 0.038000, 0.060000, 0.090980,
    0.139020, 0.208020, 0.323000, 0.503000, 0.710000, 0.862000, 0.954000, 0.994950,
    0.995000, 0.952000, 0.870000, 0.757000, 0.631000, 0.503000, 0.381000, 0.265000,
    0.175000, 0.107000, 0.061000, 0.032000, 0.017000, 0.008210, 0.004102
])  # Color matching function for Y
z_bar = np.array([
    0.067850, 0.207400, 0.645600, 1.385600, 1.747060, 1.772110, 1.669200, 1.287640,
    0.812950, 0.465180, 0.272000, 0.158200, 0.078250, 0.042160, 0.020300, 0.008750,
    0.003900, 0.002100, 0.001650, 0.001100, 0.000800, 0.000340, 0.000190, 0.000050,
    0.000020, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000
])  # Color matching function for Z
delta_lambda = 10  # Example wavelength interval in nanometers
D50_XYZ = np.array([0.96422, 1, 0.82521]) # Xr for illuminant D50 and 2 degree observer function
#NIST = [0.770800 0.804200 0.830400 0.846400 0.852800 0.860900 0.868700 0.873700 0.878500 0.884000 0.888900 0.891000 0.894000 0.896900 0.900400 0.901500 0.900700 0.902200 0.903000 0.904400 0.905400 0.904800 0.904800 0.904500 0.902700 0.901200 0.901200 0.906300 0.906900 0.907400 0.908100]

# Get user input for S
S = get_user_input("Enter the spectral reflectance or transmittance values separated by spaces: ")

# Compute XYZ values
X, Y, Z = compute_xyz_from_spectral_data(S, I, x_bar, y_bar, z_bar, delta_lambda)
#print(f"Computed XYZ values: X={X}, Y={Y}, Z={Z}")

L, a, b = XYZ_to_Lab(X, Y, Z)
#print("Lab value is: ", L, a, b)

bradford_adaption_E_d50 = [[0.9977545, -0.0041632, -0.0293713], # Not needed
                           [-0.0097677, 1.0183168, -0.0085490], # FYI only
                           [-0.0074169, 0.0134416, 0.8191853]]

bradford_adaption_d50_E = [[1.0025535, 0.0036238, 0.0359837], # translates XYZ under D50 to illuminant E before apply CIE RGB conversion
                           [0.0096914, 0.9819125, 0.0105947],
                           [0.0089181, -0.0160789, 1.2208770]]

bradford_adaption_d50_d65 = [[0.9555766, -0.0230393, 0.0631636],
                             [-0.0282895, 1.0099416, 0.0210077],
                             [0.0122982, -0.0204830, 1.3299098]]

XYZ_to_CIERGB_matrices = [[2.3706743, -0.9000405, -0.4706338], # translated XYZ to CIE RGB both under illuminant E white point
                          [-0.5138850, 1.4253036, 0.0885814],
                          [0.0052982, -0.0146949, 1.0093968]]

XYZ_to_sRGB_matrices = [[3.2404542, -1.5371385, -0.4985314],
                        [-0.9692660, 1.8760108, 0.0415560],
                        [0.0556434, -0.2040259, 1.0572252]]

XYZ_to_CIERGB_d50_matrices = [[2.3638081, -0.8676030, -0.4988161], # translate XYZ under D50 directly to CIE RGB under illuminant E white point
                              [-0.5005940, 1.3962369, 0.1047562],  # Not Needed FYI only
                              [0.0141712, -0.0306400, 1.2323842]]

XYZ = [[X],[Y],[Z]]
XYZ_1x3 = [X, Y, Z]
print("XYZ under d50 is: ", XYZ_1x3)
XYZ_E = np.dot(bradford_adaption_d50_E, XYZ_1x3) # Bradford Chromatic Adoption of XYZ from d50 to illuminant E
print("XYZ under E is: ", XYZ_E)
XYZ_d65 = np.dot(bradford_adaption_d50_d65, XYZ_1x3)
print("XYZ under d65 is: ", XYZ_d65)

XYZ_to_sRGB(XYZ_d65)
XYZ_to_CIERGB(XYZ_E)


#XYZ_E_to_CIERGB = np.dot(XYZ_to_CIERGB_matrices, XYZ_E)
#XYZ_d50_to_CIERGB = np.dot(XYZ_to_CIERGB_d50_matrices, XYZ)
#CIERGB_compand = XYZ_E_to_CIERGB * 255
#print("Linear CIE RGB from adopted XYZ is: ", XYZ_E_to_CIERGB)
#print("Linear CIE RGB from d50 XYZ is: ", XYZ_d50_to_CIERGB)
#print("Companded CIE RGB is: ", CIERGB_compand)

#XYZ_d65_feed = [0.8492, 0.8985, 0.9367]
#XYZ_d65_to_sRGB = np.dot(XYZ_to_sRGB_matrices, XYZ_d65)
#sRGB_compand = XYZ_d65_to_sRGB * 255
#print("Linear sRGB from adpoted XYZ is: ", XYZ_d65_to_sRGB)
#print("Companded sRGB is: ", sRGB_compand)