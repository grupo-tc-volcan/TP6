import sympy
import numpy
import matplotlib.axes as axes
import matplotlib.pyplot as plt
import control

r3, r4, r_jfet, f0, s = sympy.symbols('R_3 R_4 R_\{jfet\} f_0 s') # To be printed in a latex style

num = sympy.Poly((r3 / (r4 + r_jfet) + 1) * (1 / (2 * numpy.pi * f0)) * s, s)
den = sympy.poly(s**(2) + 3 * (1 / (2 * numpy.pi * f0)) * s + 1, s)

num = num.subs({f0:77500, r3: 100000, r4:47000})
den = den.subs({f0:77500, r3: 100000, r4:47000})

poles = []
zeros = []

max_r_jfet = 10000
for i in range(0, max_r_jfet + 1000, 100):
    new_den = sympy.Poly(den.subs(r_jfet, i), s)
    new_num = sympy.Poly(num.subs(r_jfet, i), s)
    num_coeffs = list(new_num.coeffs())
    den_coeffs = list(new_den.coeffs())
    num_coeffs = [float(e) for e in num_coeffs]
    den_coeffs = [float(e) for e in den_coeffs]

    sys = control.tf(num_coeffs, den_coeffs)
    new_poles, new_zeros = control.pzmap(sys, Plot=False)
    poles.extend(new_poles)
    zeros.extend(new_zeros)

x_poles = [pole.real for pole in poles]
y_poles = [pole.imag for pole in poles]
x_zeros = [zero.real for zero in zeros]
y_zeros = [zero.imag for zero in zeros]

fig, (poles_plot, zeros_plot) = plt.subplots(1, 2)
fig.suptitle('Diagrama de polos y ceros')
poles_plot.scatter(x_poles, y_poles, marker='x', c='red')
zeros_plot.scatter(x_zeros, y_zeros, marker='o', c='blue')

poles_plot.set_xlabel('Parte real σ (Hz)')
poles_plot.set_ylabel('Parte imaginaria jω (Hz)')
poles_plot.set_title('Polos')
poles_plot.ticklabel_format(axis='both', scilimits=(-2,2))
poles_plot.grid()
poles_plot.autoscale()

zeros_plot.set_xlabel('Parte real σ (Hz)')
zeros_plot.set_ylabel('Parte imaginaria jω (Hz)')
zeros_plot.set_title('Ceros')
zeros_plot.ticklabel_format(axis='both', scilimits=(-2,2))
zeros_plot.grid()
zeros_plot.autoscale()

plt.show()