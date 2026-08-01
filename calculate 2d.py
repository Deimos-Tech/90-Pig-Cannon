import numpy as np
from matplotlib import pyplot as plt

from scipy.optimize import minimize 
    
#def model(n, A, x0):
#    return np.dot(A, n) + x0
#A = np.asarray(((48, -50), (61, 52)))/64

def model(n, a, b, c, d, x0, y0):
    return n[0] * a + n[1] * c + x0, n[0] * b + n[1] * d + y0
    
def estimate_travel(x, z, popt):
    x0, z0 = popt[[4, 5]]
    
    delta = np.sqrt((x - x0)**2 + (z - z0)**2)      #Distance Travelled
    d = 0.91                                        #Drag Coefficient
    
    return - np.log(delta)/np.log(d)
    
def fit_xz(n, pos):
    
    def loss(args, n, pos):
        """
        Point-Wise Residuals for n = ((nx1, nx2, nx3, ...), (ny1, ny2, ny3, ...)) and pos = ((x1, x2, x3, ...), (y1, y2, y3, ...))
        Args has form (a, b, c, d, x0, y0) for matrix operation
        ╭x╮   ╭a c╮╭n1╮   ╭x0╮  
        ╰y╯ = ╰b d╯╰n2╯ + ╰y0╯  
        """
        a, b, c, d, x0, y0 = args
        #pred = model(n, np.asarray((a, c), (b, d)), np.asarray(x0, y0))
        pred = model(n, a, b, c, d, x0, y0)
        return (pos[0] - pred[0])**2 + (pos[1] - pred[1])**2 
        
    def sum_sqr(args, n, pos):
        return np.sum(loss(args, n, pos))
        
    p0 = (1, 1, -1, 1, pos[0][0], pos[1][0])
    result = minimize(sum_sqr, p0, args=(n, pos))
    popt = result.x
    pcov = result.hess_inv
    
    if result.status != 0:
        print(result.message)
    
    return popt, pcov
    
def visualize_fit(popt, pcov, n, m, pos_x, pos_z):
    fig, ax = plt.subplots()
    ax.scatter(pos_x, pos_z, marker = "x", color = "black")
    pred = model((n, m), *popt)
    ax.scatter(pred[0], pred[1], color = "black", alpha=.2)
    
    for i in range(len(pos_x)):
        ax.plot((pos_x[i], pred[0][i]), (pos_z[i], pred[1][i]), color = "black", alpha = .2)
    
    n_model = np.linspace(min(n), max(n))
    m_model = np.linspace(min(m), max(m))
    
    x, y = model((n_model, 0), *popt)
    ax.plot(x, y, color = "black", linestyle=":")
    
    x, y = model((0, m_model), *popt)
    ax.plot(x, y, color = "black", linestyle=":")
    
    
    x, y = model((n_model, m_model), *popt)
    ax.plot(x, y, color = "black", linestyle=":", alpha=.3)
    
    return ax
    
def calculate(x, y, popt):
    """
    Finds Optimal item counts for target position
    """
    
    #Linalg Solution
    A = np.asarray(((popt[0], popt[2]), (popt[1], popt[3])))
    x0 = np.asarray([popt[4], popt[5]]).T
    
    X = np.asarray([x, y]).T
    
    n = np.dot(np.linalg.inv(A), X-x0)
    
    #If Linalg Solution Fails Optimize with Lagrange Multiplier
    a11, a21, a12, a22, x0, y0 = popt
    if n[0] < 0:
        n[0] = 0
        n[1] = (a12*(x-x0) + a22*(y-y0))/(a12**2 + a22**2)
    elif n[1] < 0:
        n[1] = 0
        n[0] = (a11*(x-x0) + a21*(y-y0))/(a11**2 + a21**2)
        
    if n[0] < 0 or n[1] < 0:
        n[0] = 0
        n[1] = 0
    
    return n
    
def main():

    warning_threshold = 20
    
    n, m, pos_x, pos_z = np.genfromtxt("COORDINATES.txt", comments = "#", unpack=True)
    popt, pcov = fit_xz(np.asarray((n, m)), np.asarray((pos_x, pos_z)))
    perr = np.sqrt(pcov.diagonal())
    
    print(f"""
        ╭x╮   ╭{popt[0]: .2f} +- {perr[0]:.2f} {popt[2]: .2f} +- {perr[2]:.2f}╮ ╭n1╮   ╭{popt[4]: .1f} +- {perr[4]:.1f}╮  
        ╰y╯ = ╰{popt[1]: .2f} +- {perr[1]:.2f} {popt[3]: .2f} +- {perr[3]:.2f}╯ ╰n2╯ + ╰{popt[5]: .1f} +- {perr[5]:.1f}╯  
    """)
    
    
    print("Please enter Target Destination:")
    xt = float(input("x = "))
    zt = float(input("z = "))
    
    nt = np.round(calculate(xt, zt, popt))
    print("\nn1 =", nt[0])
    print("n2 =", nt[1], "\n")
    
    ax = visualize_fit(popt, pcov, n, m, pos_x, pos_z)
    
    #Visualize Landing position
    ax.scatter(xt, zt, color="red", marker="x")
    x, z = model(nt, *popt)
    distance = np.sqrt((x-xt)**2 + (z-zt)**2)
    
    if distance > warning_threshold:
        print(f"Warning: Calculated position is {distance:.0f}m from target position\n")
        
    t = estimate_travel(x, z, popt)
    print(f"Estimated Travel time is {t:.0f} Ticks = {t/20:.1f} Seconds")
    
    ax.scatter(x, z, color="red", alpha=.3)
    
    ax.grid(True, linestyle=":")
    ax.set_aspect('equal')
    plt.show()
    
if __name__ == "__main__":
    main()
