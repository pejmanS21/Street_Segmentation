import torch
import torchvision.transforms as T
from .unet import UNet


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

stats = (0.5,), (0.5,)
h, w = 160, 240

transformer = T.Compose([
            T.Resize((h, w)),
            T.ToTensor(),
            T.Normalize(*stats),
])

model_path = './models/Udacity_Unet.pth'

model = UNet().to(device)
model.eval()
model.load_state_dict(torch.load(model_path, map_location=device))


setup = {
    'model': model,
    'transformer': transformer,
    'stats': stats,
    'device': device,

}