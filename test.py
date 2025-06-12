import torch

def check_gpu_availability():
    print("="*50)
    print("GPU Detection Report")
    print("="*50)
    
    # Check if CUDA is available
    cuda_available = torch.cuda.is_available()
    print(f"CUDA Available: {'✅ YES' if cuda_available else '❌ NO'}")
    
    if not cuda_available:
        print("\nNo GPU detected. Possible reasons:")
        print("- No NVIDIA GPU installed")
        print("- CUDA drivers not installed")
        print("- PyTorch not installed with CUDA support")
        return
    
    # Get GPU information
    device_count = torch.cuda.device_count()
    print(f"\nNumber of GPUs detected: {device_count}")
    
    for i in range(device_count):
        print(f"\nGPU {i} Details:")
        print(f"  Name: {torch.cuda.get_device_name(i)}")
        print(f"  Compute Capability: {torch.cuda.get_device_capability(i)}")
        print(f"  Total Memory: {torch.cuda.get_device_properties(i).total_memory / 1024**3:.2f} GB")
    
    # Check current device
    current_device = torch.cuda.current_device()
    print(f"\nCurrent device: GPU {current_device} ({torch.cuda.get_device_name(current_device)})")