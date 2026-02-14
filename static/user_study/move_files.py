import os
import shutil
import json
import re

# 源目录
source_dir = r"D:\Sound2Image\Soundscape-to-ImageDiT-main\Soundscape-to-ImageDiT-main\DiT\SounDiT_results\SoundiT_generated_images_48epoch_4_4_30\generated_images_48epoch_4_4_30"

# 目标根目录（假设在相同的磁盘），如果需要可以修改
target_root = r"D:\Sound2Image\Soundscape-to-ImageDiT-main\Soundscape-to-ImageDiT-main\DiT\static\user_study\Q1"

# 读取粘贴文本并解析
with open('D:\Human Mobility+Urban Greenspace\StreetviewLiterature\HumanPerception\data\Mapillary Data\global-streetscapes\global-streetscapes\github\SounDiT-Page\config\use_study_src.js', 'r') as f:
    # 添加花括号使其成为有效的JSON
    content = "{" + f.read() + "}"
    # 移除尾部的逗号，如果存在
    content = re.sub(r',(\s*})', r'\1', content)
    data = json.loads(content)

# 处理每个子集中的图像
for sub_key, sub_data in data.items():
    # 处理生成的景观图像
    for img_key, img_path in sub_data.get('generated', {}).items():
        # 跳过sonicurban路径
        if 'sonicurban' in img_path:
            print(f"跳过sonicurban路径: {img_path}")
            continue
        
        # 提取文件名和路径信息
        img_name = os.path.basename(img_path)
        target_dir = os.path.dirname(img_path)
        
        # 在源目录中查找文件
        source_file = os.path.join(source_dir, img_name)
        
        # 创建目标目录（如果不存在）
        full_target_dir = os.path.join(target_root, *target_dir.split('/')[2:])  # 排除"static/user_study/Q1"
        os.makedirs(full_target_dir, exist_ok=True)
        
        # 目标文件路径
        target_file = os.path.join(full_target_dir, img_name)
        
        # 如果源文件存在，则复制
        if os.path.exists(source_file):
            print(f"复制文件: {source_file} 到 {target_file}")
            shutil.copy2(source_file, target_file)
        else:
            print(f"错误: 源文件不存在: {source_file}")

    # 同样处理真实图像（如果需要）
    for img_key, img_path in sub_data.get('ground_truth', {}).items():
        # 跳过sonicurban路径
        if 'sonicurban' in img_path:
            print(f"跳过sonicurban路径: {img_path}")
            continue
        
        # 提取文件名和路径信息
        img_name = os.path.basename(img_path)
        target_dir = os.path.dirname(img_path)
        
        # 在源目录中查找文件
        source_file = os.path.join(source_dir, img_name)
        
        # 创建目标目录（如果不存在）
        full_target_dir = os.path.join(target_root, *target_dir.split('/')[2:])  # 排除"static/user_study/Q1"
        os.makedirs(full_target_dir, exist_ok=True)
        
        # 目标文件路径
        target_file = os.path.join(full_target_dir, img_name)
        
        # 如果源文件存在，则复制
        if os.path.exists(source_file):
            print(f"复制文件: {source_file} 到 {target_file}")
            shutil.copy2(source_file, target_file)
        else:
            print(f"错误: 源文件不存在: {source_file}")

print("处理完成！")