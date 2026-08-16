修改版增加了卷积层的数量。
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
from torchvision.models import vgg16
from torchvision.models.vgg import VGG16_Weights
from skimage.metrics import structural_similarity as ssim


# 1. 隐式正则 Retinex 分解模型
class RetinexDecomposition(nn.Module):
    def __init__(self):
        super(RetinexDecomposition, self).__init__()
        # 增加卷积层
        self.conv_block = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU()
        )
        # 分别输出照明分量和反射分量
        self.conv_illumination = nn.Conv2d(256, 3, kernel_size=3, padding=1)
        self.conv_reflectance = nn.Conv2d(256, 3, kernel_size=3, padding=1)

    def forward(self, x):
        x = self.conv_block(x)
        illumination = torch.sigmoid(self.conv_illumination(x))  # 照明分量约束在 [0, 1]
        reflectance = torch.sigmoid(self.conv_reflectance(x))    # 反射分量约束在 [0, 1]
        return illumination, reflectance


# 2. S 型曲线估计网络进行亮度增强
class SCurveEnhancement(nn.Module):
    def __init__(self):
        super(SCurveEnhancement, self).__init__()
        # 增加全连接层
        self.fc_block = nn.Sequential(
            nn.Linear(3, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 3)
        )

    def forward(self, illumination):
        # 提取照明分量的统计信息（例如均值）
        stats = torch.mean(illumination, dim=(2, 3))
        # 估计 S 型曲线参数
        params = torch.sigmoid(self.fc_block(stats))
        # 对参数进行限制，避免过大
        params = torch.clamp(params, min=0.1, max=1.0)
        # 应用 S 型曲线进行亮度增强
        enhanced_illumination = 1 / (1 + torch.exp(-params.unsqueeze(-1).unsqueeze(-1) * (illumination - 0.5)))
        return enhanced_illumination


# 3. 自监督反射估计网络  这里是无监督网络的设计
class SelfSupervisedReflectanceEstimation(nn.Module):
    def __init__(self):
        super(SelfSupervisedReflectanceEstimation, self).__init__()
        # 编码器
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.ReLU()
        )
        # 解码器部分
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2),
            nn.ReLU(),
            nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, kernel_size=2, stride=2),
            nn.ReLU(),
            nn.Conv2d(32, 3, kernel_size=3, padding=1),  # 修改这里，使用普通卷积层
            nn.Sigmoid()
        )

    def forward(self, reflectance):
        encoded = self.encoder(reflectance)
        decoded = self.decoder(encoded)
        return decoded


class CustomImageDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.image_files = []
        valid_extensions = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp')
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.lower().endswith(valid_extensions):
                    self.image_files.append(os.path.join(root, file))

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        image_path = self.image_files[idx]
        image = Image.open(image_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image


# 感知损失
class PerceptualLoss(nn.Module):
    def __init__(self):
        super(PerceptualLoss, self).__init__()
        # 修改这里，使用 weights 参数
        vgg = vgg16(weights=VGG16_Weights.DEFAULT)
        self.vgg_layers = vgg.features[:3]  # 选择前3层
        for param in self.vgg_layers.parameters():
            param.requires_grad = False

    def forward(self, x, y):
        x_features = self.vgg_layers(x)
        y_features = self.vgg_layers(y)
        return torch.mean((x_features - y_features) ** 2)


# 主函数，将三个模块组合起来进行训练和推理
def main():
    # 数据预处理
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ])

    # 数据集路径
    image_dir = 'E:/Pycharm/train_data'
    # 加载数据集
    dataset = CustomImageDataset(root_dir=image_dir, transform=transform)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

    # 初始化模型
    decomposition_model = RetinexDecomposition()
    enhancement_model = SCurveEnhancement()
    reflectance_estimation_model = SelfSupervisedReflectanceEstimation()

    # 定义优化器
    optimizer = optim.Adam(list(decomposition_model.parameters()) +
                           list(enhancement_model.parameters()) +
                           list(reflectance_estimation_model.parameters()), lr=0.001)

    # 定义损失函数
    mse_loss = nn.MSELoss()
    perceptual_loss = PerceptualLoss()

    # 训练循环
    num_epochs = 10
    for epoch in range(num_epochs):
        running_loss = 0.0
        for i, images in enumerate(dataloader):
            optimizer.zero_grad()

            # 1. Retinex 分解
            illumination, reflectance = decomposition_model(images)

            # 2. S 型曲线亮度增强
            enhanced_illumination = enhancement_model(illumination)

            # 3. 自监督反射估计
            refined_reflectance = reflectance_estimation_model(reflectance)

            # 重建增强后的图像
            enhanced_image = enhanced_illumination * refined_reflectance
            # 限制像素值范围在 [0, 1]
            enhanced_image = torch.clamp(enhanced_image, 0, 1)

            # 损失函数
            mse = mse_loss(enhanced_image, images)
            percep = perceptual_loss(enhanced_image, images)
            loss = mse + percep

            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {running_loss / len(dataloader)}')

    # 推理并展示结果
    with torch.no_grad():
        for i, images in enumerate(dataloader):
            # 1. Retinex 分解
            illumination, reflectance = decomposition_model(images)

            # 2. S 型曲线亮度增强
            enhanced_illumination = enhancement_model(illumination)

            # 3. 自监督反射估计
            refined_reflectance = reflectance_estimation_model(reflectance)

            # 重建增强后的图像
            enhanced_image = enhanced_illumination * refined_reflectance
            # 限制像素值范围在 [0, 1]
            enhanced_image = torch.clamp(enhanced_image, 0, 1)

            # 转换为 numpy 数组并调整维度
            original_image = images[0].permute(1, 2, 0).cpu().numpy()
            enhanced_image = enhanced_image[0].permute(1, 2, 0).cpu().numpy()

            # 确保数据类型为 float32
            original_image = original_image.astype('float32')
            enhanced_image = enhanced_image.astype('float32')

            # 计算 SSIM
            ssim_score = ssim(original_image, enhanced_image, win_size=3, channel_axis=2, data_range=1.0)
            print(f'SSIM: {ssim_score}')

            # 展示原始图像和增强后的图像
            plt.figure(figsize=(10, 5))
            plt.subplot(1, 2, 1)
            plt.imshow(original_image)
            plt.title('Original Image')
            plt.axis('off')

            plt.subplot(1, 2, 2)
            plt.imshow(enhanced_image)
            plt.title('Enhanced Image')
            plt.axis('off')

            plt.show()


if __name__ == "__main__":
    main()