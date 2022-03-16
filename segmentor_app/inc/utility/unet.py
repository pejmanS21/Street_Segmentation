import torch
import torch.nn as nn
import torchvision.models as models
from torchsummary import summary


class ConvLayer(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(ConvLayer, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, 1, 1, bias=False), 
            nn.BatchNorm2d(out_channels), 
            nn.ReLU(inplace=True), 
            nn.Conv2d(out_channels, out_channels, 3, 1, 1, bias=False), 
            nn.BatchNorm2d(out_channels), 
            nn.ReLU(inplace=True))

    def forward(self, x):
        return self.conv(x)


class TConvLayer(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(TConvLayer, self).__init__()
        self.tconv = nn.ConvTranspose2d(in_channels, out_channels, kernel_size=2, stride=2)
    
    def forward(self, x):
        return self.tconv(x)


class UNet(nn.Module):
    def __init__(self, out_channels=23, features=[64, 128, 256, 512]):
        super(UNet, self).__init__()
        self.pool = nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2))
        
        self.conv1 = ConvLayer(3,features[0])
        self.conv2 = ConvLayer(features[0], features[1])
        self.conv3 = ConvLayer(features[1], features[2])
        self.conv4 = ConvLayer(features[2], features[3])
        self.conv5 = ConvLayer(features[3] * 2,features[3])
        self.conv6 = ConvLayer(features[3], features[2])
        self.conv7 = ConvLayer(features[2], features[1])
        self.conv8 = ConvLayer(features[1], features[0])        
        
        self.tconv1 = TConvLayer(features[-1] * 2, features[-1])
        self.tconv2 = TConvLayer(features[-1], features[-2])
        self.tconv3 = TConvLayer(features[-2], features[-3])
        self.tconv4 = TConvLayer(features[-3], features[-4])        
        
        self.bottleneck = ConvLayer(features[3], features[3] * 2)
        self.final_layer = nn.Conv2d(features[0], out_channels, kernel_size=1)
    
    def forward(self, x):
        skip_connections = []
        x = self.conv1(x)
        
        skip_connections.append(x)
        x = self.pool(x)
        x = self.conv2(x)
        
        skip_connections.append(x)
        x = self.pool(x)
        x = self.conv3(x)
        
        skip_connections.append(x)
        x = self.pool(x)
        x = self.conv4(x)
        
        skip_connections.append(x)
        x = self.pool(x)
        x = self.bottleneck(x)
        
        skip_connections = skip_connections[::-1]
        x = self.tconv1(x)
        x = torch.cat((skip_connections[0], x), dim=1)
        
        x = self.conv5(x)
        x = self.tconv2(x)
        
        x = torch.cat((skip_connections[1], x), dim=1)
        x = self.conv6(x)
        x = self.tconv3(x)
        
        x = torch.cat((skip_connections[2], x), dim=1)
        x = self.conv7(x)        
        x = self.tconv4(x)
        
        x = torch.cat((skip_connections[3], x), dim=1)
        x = self.conv8(x)
        x = self.final_layer(x)
        
        return x
    
    def _summary_(self, input_size=(3, 160, 240)):
        return summary(self, input_size)



if __name__ == "__main__":
    model = UNet()
    model.summary()