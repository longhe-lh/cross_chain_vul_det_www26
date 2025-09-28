# test_deepspeed_cuda.py
import torch
import deepspeed

print("Deepspeed available:", deepspeed.__version__)
print("CUDA available:", torch.cuda.is_available())
print("CUDA device name:", torch.cuda.get_device_name(0))