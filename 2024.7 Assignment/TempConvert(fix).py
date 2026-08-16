import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt


# 1. 隐式正则 Retinex 分解模型
class RetinexDecomposition(nn.Module):
    def __init__(self):
        super(RetinexDecomposition, self).__init__()
        # 简单的卷积层用于特征提取
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        # 分别输出照明分量和反射分量
        self.conv_illumination = nn.Conv2d(64, 3, kernel_size=3, padding=1)
        self.conv_reflectance = nn.Conv2d(64, 3, kernel_size=3, padding=1)

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        illumination = torch.sigmoid(self.conv_illumination(x))  # 照明分量约束在 [0, 1]
        reflectance = torch.sigmoid(self.conv_reflectance(x))    # 反射分量约束在 [0, 1]
        return illumination, reflectance


# 2. S 型曲线估计网络进行亮度增强
class SCurveEnhancement(nn.Module):
    def __init__(self):
        super(SCurveEnhancement, self).__init__()
        # 简单的全连接层用于估计 S 型曲线参数
        self.fc1 = nn.Linear(3, 16)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(16, 3)

    def forward(self, illumination):
        # 提取照明分量的统计信息（例如均值）
        stats = torch.mean(illumination, dim=(2, 3))
        # 估计 S 型曲线参数
        params = torch.sigmoid(self.fc2(self.relu(self.fc1(stats))))
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
        self.encoder = nn.Sequential( #nn.Sequential：这是一个 PyTorch 中的容器类，用于按顺序组合多个神经网络层。输入数据会按照定义的顺序依次通过这些层。
            nn.Conv2d(3, 32, kernel_size=3, padding=1), #一个二维卷积层
            nn.ReLU(), #这是一个激活函数层，使用的是修正线性单元（Rectified Linear Unit，ReLU），它的作用是将输入中所有小于 0 的值置为 0，增加模型的非线性表达能力。
            nn.MaxPool2d(2), #这是一个二维最大池化层，池化核大小为 2x2，步长默认为 2，它的作用是对输入的特征图进行下采样，将特征图的尺寸缩小一半，同时保留最重要的特征信息。
            nn.Conv2d(32, 64, kernel_size=3, padding=1),#将32位转变为64位
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        # 解码器部分
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(64, 32, kernel_size=2, stride=2), #二位转置卷积层，也称为反卷积层
            nn.ReLU(),
            nn.ConvTranspose2d(32, 3, kernel_size=2, stride=2), #将通道数从32变为3
            nn.Sigmoid() #nn.Sigmoid()：这是一个激活函数层，将输出的值压缩到 0 到 1 之间，常用于将模型的输出转换为概率值或像素值（在图像生成任务中）。
        )

    def forward(self, reflectance):
        encoded = self.encoder(reflectance)
        decoded = self.decoder(encoded)
        return decoded


class CustomImageDataset(DataLoader):
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
        return image, 0


# 主函数，将三个模块组合起来进行训练和推理
def main():
    # 数据预处理
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor()
    ])

    # 数据集路径
    image_dir = 'E:/Pycharm/low_light_image/low_light_image/processed_images'

    # 加载数据集
    dataset = CustomImageDataset(root_dir=image_dir, transform=transform)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

    # 初始化模型
    decomposition_model = RetinexDecomposition()
    enhancement_model = SCurveEnhancement()
    reflectance_estimation_model = SelfSupervisedReflectanceEstimation()

    # 定义优化器
    optimizer = optim.Adam(list(decomposition_model.parameters()) +
                           list(enhancement_model.parameters()) +
                           list(reflectance_estimation_model.parameters()), lr=0.001)

    # 训练循环
    num_epochs = 250
    for epoch in range(num_epochs):
        running_loss = 0.0
        for i, (images, _) in enumerate(dataloader):
            optimizer.zero_grad()

            # 1. Retinex 分解
            illumination, reflectance = decomposition_model(images)

            # 2. S 型曲线亮度增强
            enhanced_illumination = enhancement_model(illumination)

            # 3. 自监督反射估计
            refined_reflectance = reflectance_estimation_model(reflectance)

            # 重建增强后的图像
            enhanced_image = enhanced_illumination * refined_reflectance

            # 简单的损失函数（这里可以根据实际情况调整）
            loss = torch.mean((enhanced_image - images) ** 2)

            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {running_loss / len(dataloader)}')

    # 推理并展示结果
    with torch.no_grad():
        for i, (images, _) in enumerate(dataloader):
            # 1. Retinex 分解
            illumination, reflectance = decomposition_model(images)

            # 2. S 型曲线亮度增强
            enhanced_illumination = enhancement_model(illumination)

            # 3. 自监督反射估计
            refined_reflectance = reflectance_estimation_model(reflectance)

            # 重建增强后的图像
            enhanced_image = enhanced_illumination * refined_reflectance

            # 转换为 numpy 数组并调整维度
            original_image = images[0].permute(1, 2, 0).cpu().numpy()
            enhanced_image = enhanced_image[0].permute(1, 2, 0).cpu().numpy()

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
