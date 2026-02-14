import os
from PIL import Image

def crop_images_to_256x256_recursive(root_dir):
    """
    递归检查指定路径下的所有文件夹，
    对发现的所有图像文件进行处理，确保它们都被裁剪成 256x256 的尺寸。
    
    参数：
        root_dir: 要递归处理的根目录路径
    """
    # 图像文件的可能后缀
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    
    # 计数器
    processed_images = 0
    already_256x256 = 0
    error_images = 0
    
    # 确认根目录存在
    if not os.path.exists(root_dir):
        print(f"错误: 根目录 '{root_dir}' 不存在。")
        return processed_images, already_256x256, error_images
    
    # 递归处理所有文件夹
    for dirpath, dirnames, filenames in os.walk(root_dir):
        print(f"正在处理目录: {dirpath}")
        
        # 处理当前文件夹中的所有图像文件
        for filename in filenames:
            # 检查是否为图像文件
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                image_path = os.path.join(dirpath, filename)
                
                try:
                    # 打开图像
                    img = Image.open(image_path)
                    
                    # 获取原始图像尺寸
                    width, height = img.size
                    
                    # 检查是否已经是256x256
                    if width == 256 and height == 256:
                        already_256x256 += 1
                        print(f"图像 '{image_path}' 已经是 256x256 的尺寸")
                        continue
                    
                    # 计算裁剪区域（中心裁剪）
                    left = (width - 256) / 2
                    top = (height - 256) / 2
                    right = (width + 256) / 2
                    bottom = (height + 256) / 2
                    
                    # 裁剪图像
                    if width >= 256 and height >= 256:
                        # 如果图像足够大，进行中心裁剪
                        cropped_img = img.crop((left, top, right, bottom))
                    else:
                        # 如果原图小于256x256，则调整大小
                        print(f"  原图尺寸 {img.size} 小于 256x256，将进行调整大小")
                        # 创建一个256x256的黑色背景
                        background = Image.new('RGB', (256, 256), (0, 0, 0))
                        # 计算粘贴位置（居中）
                        paste_x = max(0, (256 - width) // 2)
                        paste_y = max(0, (256 - height) // 2)
                        # 粘贴原图到背景上
                        background.paste(img, (paste_x, paste_y))
                        cropped_img = background
                    
                    # 确认裁剪后的尺寸正确
                    if cropped_img.size != (256, 256):
                        print(f"警告: 裁剪后的图像 '{image_path}' 尺寸异常: {cropped_img.size}")
                        # 强制调整大小
                        cropped_img = cropped_img.resize((256, 256), Image.LANCZOS)
                    
                    # 保存裁剪后的图像（覆盖原图像）
                    cropped_img.save(image_path)
                    processed_images += 1
                    print(f"已将图像 '{image_path}' 裁剪为 256x256")
                except Exception as e:
                    error_images += 1
                    print(f"处理图像 '{image_path}' 时出错: {e}")
    
    return processed_images, already_256x256, error_images

def main():
    """主函数"""
    # 定义要处理的根目录
    root_dir = r'D:\Human Mobility+Urban Greenspace\StreetviewLiterature\HumanPerception\data\Mapillary Data\global-streetscapes\global-streetscapes\github\SounDiT-Page\static\user_study\Q1\sonicurban'
    
    print(f"开始递归检查和裁剪图像，根目录: {root_dir}")
    
    # 递归处理所有图像
    processed, already_sized, errors = crop_images_to_256x256_recursive(root_dir)
    
    # 打印处理结果摘要
    print("\n处理完成:")
    print(f"- 已裁剪 {processed} 个图像文件")
    print(f"- 有 {already_sized} 个图像已经是 256x256 尺寸")
    print(f"- 处理失败 {errors} 个图像文件")

if __name__ == "__main__":
    main()