import sympy
import numpy
import matplotlib.axes as axes
import matplotlib.pyplot as plt
import control

r, r3, r4, r_jfet, c, s = sympy.symbols('R R_3 R_4 R_\{jfet\} C s') # To be printed in a latex style

num = sympy.Poly((r3 / (r4 + r_jfet) + 1) * c**2 * r**2 * s**(2) + (r3 / (r4 + r_jfet) + 1) * 3 * c * r * s + 1, s)
den = sympy.poly(c**2 * r**2 * s**(2) + (r3 / (r4 + r_jfet) + 4) * 3 * c * r * s + 1, s)

num = num.subs({r:2050, c:10e-9, r3: 100000, r4:47000})
den = den.subs({r:2050, c:10e-9, r3: 100000, r4:47000})

poles = []
zeros = []

max_r_jfet = 100000
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