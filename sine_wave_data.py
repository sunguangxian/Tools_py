import numpy as np
import matplotlib.pyplot as plt

# 生成0到49的数组
x = np.arange(50)

# 计算正弦波数据，并映射到DAC的范围
sin_wave = np.sin(2 * np.pi * x / 48) * 4096

# 将数据转换为整数类型
sin_wave_int = sin_wave.astype(int)


# 绘制波形图
plt.plot(sin_wave_int)
plt.title('Sine Wave Data')
plt.xlabel('Sample Number')
plt.ylabel('DAC Value')
plt.grid(True)
plt.show()
