import json
import os

# 文件名
input_filename = "jobs.json"
output_filename = "jobs.txt"


def format_job(job):
    # 安全获取字段
    job_name = job.get("jobName", "未知岗位")
    salary = job.get("salaryDesc", "薪资未知")
    city = job.get("cityName", "城市未知")
    experience = job.get("jobExperience", "经验不限")
    education = job.get("jobDegree", "学历不限")
    company = job.get("brandName", "公司未知")
    boss = job.get("bossName", "")
    boss_title = job.get("bossTitle", "")
    description = job.get("skills", [])
    description_text = "、".join(description) if description else "岗位描述暂无"

    # 拼接文本格式
    formatted = (
        f"岗位名称：{job_name}\n"
        f"薪资范围：{salary}\n"
        f"工作地点：{city}\n"
        f"经验要求：{experience}\n"
        f"学历要求：{education}\n"
        f"岗位职责：{description_text}\n"
        f"所属公司：{company}（{boss}，{boss_title}）\n"
    )
    return formatted


def convert_json_to_txt():
    if not os.path.exists(input_filename):
        print(f"❌ 未找到 {input_filename} 文件")
        return

    with open(input_filename, "r", encoding="utf-8") as f:
        jobs_data = json.load(f)

    output_lines = []
    for job in jobs_data:
        output_lines.append(format_job(job))
        output_lines.append("-" * 50)  # 分隔线

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"✅ 成功生成岗位文本到 {output_filename}")


if __name__ == "__main__":
    convert_json_to_txt()
