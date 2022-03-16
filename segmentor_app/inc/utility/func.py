import torch
import torch.nn as nn
import cv2
from torchvision.utils import save_image
import torchvision.transforms as T
import matplotlib
matplotlib.use('Agg')   # if get any error check matplotlib gui error
import matplotlib.pyplot as plt
from PIL import Image
from .settings import setup


stats = setup['stats']
transformer = setup['transformer']
loaded_model = setup['model']
device = setup['device']


def denormal(pil_image, img_stats=stats):
    """denormalize  pil image

    Args:
        pil_image (PIL Image)
        img_stats (Tuple, optional). Defaults to ((0.5, ), (0.5, )).

    Returns:
        pil_image (PIL Image)
    """
    return pil_image * img_stats[1][0] + img_stats[0][0]


def pil_preparation(path, transform=transformer):
    """get numpy image convert to PIL and apply transform

    Args:
        frame (numpy array): 
        transform (optional): Defaults to transformer.

    Returns:
        Tensor Image: Ready to go to Torch model
    """
    pil_frame = Image.open(path).convert('RGB')
    pil_frame = transform(pil_frame)
    return pil_frame


def get_pred(image, model=loaded_model, device=device):
    save_path = './media/images/results.png'
    if type(image) == str:
        name = image.split('/')[-1]
        name = name.split('.')[0]
        save_path = f'./media/images/results_{name}.png'
        image = pil_preparation(image)
    
    if len(image) == 3:
        image = image.unsqueeze(0)
    softmax = nn.Softmax(dim=1)
    preds = torch.argmax(softmax(model(image.to(device))), axis=1).cpu()
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))
    ax[0].imshow(denormal(image[0]).permute(1, 2, 0))
    ax[1].imshow(preds[0].cpu())
    
    ax[0].set_title('Image')
    ax[1].set_title('Prediction')
    
    ax[0].axis('off')
    ax[1].axis('off')
    fig.savefig(save_path)

