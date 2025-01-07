import torch
from pytorch_classes.DQN2 import DQN

# Load your PyTorch model
model_path = "models3/dqn_greedy-100_000-800KMem-1e_4LR-128BS-NNv2.pth"
n_observations = 54
n_actions = 3
checkpoint = torch.load(model_path)
model = DQN(n_observations, n_actions)
model.load_state_dict(checkpoint["model_state_dict"]) if "model_state_dict" in checkpoint \
                else model.load_state_dict(checkpoint)
model.eval()

# Export the model to ONNX
dummy_input = torch.randn(1, n_observations)  # Adjust input shape as needed
onnx_path = "exported_models/dqn_greedy-100_000-800KMem-1e_4LR-128BS-NNv2.onnx"
torch.onnx.export(
    model,
    dummy_input,
    onnx_path,
    export_params=True,
    opset_version=11,
    input_names=["input"],
    output_names=["output"],
    dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
)
print(f"Model exported to {onnx_path}")
