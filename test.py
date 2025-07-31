def process_text_for_social_media(input_text):
    lines = input_text.splitlines(keepends=False)  # 分割为行列表，不保留换行符
    output_lines = []
    blank_count = 0  # 连续空行计数器

    for line in lines:
        stripped_line = line.strip()
        if stripped_line == "":  # 当前行为空
            blank_count += 1
            if blank_count >= 2:  # 连续两个空行时输出一个换行
                output_lines.append("\n")
                blank_count = 0  # 重置计数器
        else:  # 当前行非空
            output_lines.append(line)
            blank_count = 0  # 重置计数器

    return "\n".join(output_lines)  # 拼接所有行

# 示例用法
input_text = """经理，你好
我是新疆大学软件工程应届生赵宇跃，主攻Java后端开发。

在上海已式文化科技主导留学规划系统后端开发


基于Spring Boot+MyBatis-Plus实现院校信息CRUD与Excel导入导出，并优化多角色聊天系统的未读消息统计；
在新疆丝路融创开发校招系统时，设计职业推荐模块并结合MyBatis动态SQL优化分页性能。
技术博客：https://blog.csdn.net/m0_73884162?type=blog
对贵司的Java后端开发岗位非常感兴趣，期待进一步沟通技术细节！
"""
output_text = process_text_for_social_media(input_text)
print("处理后的内容：")
print(output_text)

# 可选：将结果保存到文件
with open("social_media_output.txt", "w", encoding="utf-8") as f:
    f.write(output_text)