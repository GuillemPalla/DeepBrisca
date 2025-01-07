import time
import torch
import torch_directml

# CPU
cpu_start = time.time()
a_cpu = torch.randn(1000, 1000)
b_cpu = torch.randn(1000, 1000)
c_cpu = torch.matmul(a_cpu, b_cpu)
cpu_end = time.time()

# GPU (DirectML)
device = torch_directml.device()
gpu_start = time.time()
a_gpu = torch.randn(1000, 1000, device=device)
b_gpu = torch.randn(1000, 1000, device=device)
c_gpu = torch.matmul(a_gpu, b_gpu)
gpu_end = time.time()

print("CPU time:", cpu_end - cpu_start)
print("GPU time:", gpu_end - gpu_start)
