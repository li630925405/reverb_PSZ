import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 10, 0.1)
y = np.exp(x)
# plt.plot(x, y)


y_f = np.fft.fft(y)
print(y_f)
plt.plot(y_f)

y_t = np.fft.ifft(y_f)
# plt.plot(x, y_t)

plt.show()