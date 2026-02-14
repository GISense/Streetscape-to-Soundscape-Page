import os
from PIL import Image

def crop_images_to_256x256():
    """
    检查 ground_truth/sonicurban 文件夹下的所有图像，
    确保它们都被裁剪成 256x256 的尺寸。
    """
    # 定义路径
    ground_truth_dir = r'D:\Human Mobility+Urban Greenspace\StreetviewLiterature\HumanPerception\data\Mapillary Data\global-streetscapes\global-streetscapes\github\SounDiT-Page\static\user_study\Q2\ground_truth\sonicurban'
    
    # 确认目录存在
    if not os.path.exists(ground_truth_dir):
        print(f"错误: 目录 '{ground_truth_dir}' 不存在。")
        return
    
    # 图像文件的可能后缀
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    
    # 计数器
    processed_images = 0
    already_256x256 = 0
    
    # 扫描ground_truth目录中的所有图像文件
    for filename in os.listdir(ground_truth_dir):
        # 检查是否为图像文件
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            image_path = os.path.join(ground_truth_dir, filename)
            
            try:
                # 打开图像
                img = Image.open(image_path)
                
                # 获取原始图像尺寸
                width, height = img.size
                
                # 检查是否已经是256x256
                if width == 256 and height == 256:
                    already_256x256 += 1
                    print(f"图像 '{filename}' 已经是 256x256 的尺寸")
                    continue
                
                # 计算裁剪区域（中心裁剪）
                left = (width - 256) / 2
                top = (height - 256) / 2
                right = (width + 256) / 2
                bottom = (height + 256) / 2
                
                # 裁剪图像
                cropped_img = img.crop((left, top, right, bottom))
                
                # 检查裁剪后的尺寸
                if cropped_img.size != (256, 256):
                    print(f"警告: 裁剪后的图像 '{filename}' 尺寸不是 256x256，而是 {cropped_img.size}")
                    
                    # 如果原图小于256x256，则调整大小
                    if width < 256 or height < 256:
                        print(f"  原图尺寸 {img.size} 小于 256x256，将进行调整大小")
                        # 创建一个256x256的黑色背景
                        background = Image.new('RGB', (256, 256), (0, 0, 0))
                        # 计算粘贴位置（居中）
                        paste_x = (256 - width) // 2
                        paste_y = (256 - height) // 2
                        # 粘贴原图到背景上
                        background.paste(img, (paste_x, paste_y))
                        cropped_img = background
                
                # 保存裁剪后的图像（覆盖原图像）
                cropped_img.save(image_path)
                processed_images += 1
                print(f"已将图像 '{filename}' 裁剪为 256x256")
            except Exception as e:
                print(f"处理图像 '{filename}' 时出错: {e}")
    
    # 打印处理结果摘要
    print("\n处理完成:")
    print(f"- 已裁剪 {processed_images} 个图像文件")
    print(f"- 有 {already_256x256} 个图像已经是 256x256 尺寸")

if __name__ == "__main__":
    print("开始检查和裁剪图像...")
    crop_images_to_256x256()