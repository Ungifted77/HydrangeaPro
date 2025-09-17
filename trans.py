import os
import re
import pandas as pd
import yaml

# 输入 Excel 文件
INPUT_FILE = "defect.xlsx"
SHEET_NAME = "defect"
OUTPUT_DIR = "db"

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 读取 Excel，注意 header=1 才是真正的表头
df = pd.read_excel(INPUT_FILE, sheet_name=SHEET_NAME, header=1)

last_type_display = ""

for _, row in df.iterrows():
    app_full = str(row.get("APP", "")).strip()  # e.g. cpacker/MemGPT
    repo_url_raw = str(row.get("commit url", "")).strip()
    # 读取并前向填充 type：若为空则复用上一非空类型
    raw_type_value = row.get("types")
    if pd.notna(raw_type_value) and str(raw_type_value).strip():
        defect_type_display = str(raw_type_value).strip()
        last_type_display = defect_type_display
    else:
        defect_type_display = last_type_display
    case = str(row.get("cases", "")).strip()

    if not app_full or not repo_url_raw:
        continue  # 跳过无效行

    # 提取 app 名称（去掉前缀作者）
    app_name = app_full.split("/")[-1]

    # 处理 defect_type（用于 defect_id/文件名：小写+下划线；显示字段保留原样/前向填充）
    # 规范化：将任意连续空白压缩为一个下划线，并去重下划线、去两端下划线
    if defect_type_display:
        tmp = defect_type_display.strip().lower()
        tmp = re.sub(r"\s+", "_", tmp)
        tmp = re.sub(r"_+", "_", tmp).strip("_")
        defect_type_norm = tmp if tmp else "unknown"
    else:
        defect_type_norm = "unknown"

    # 规范化 case：优先数字化，空则 "/"
    case_value = row.get("cases")
    if pd.notna(case_value):
        if isinstance(case_value, (int, float)):
            try:
                case_int_like = int(case_value)
                case = str(case_int_like)
            except Exception:
                case = str(case_value).strip() or "/"
        else:
            raw_case = str(case_value).strip()
            # 支持形如 "case1" / "Case 1" / "CASE-1"
            m = re.match(r"(?i)^case\s*[-_]?\s*(\d+)$", raw_case)
            if m:
                case = m.group(1)
            else:
                case = raw_case or "/"
    else:
        case = "/"

    # 构造 defect_id（包含作者名）
    author_name = app_full.split("/")[0] if "/" in app_full else app_name
    defect_id = (
        f"{author_name}-{app_name}-{defect_type_norm}-case{case}"
        if case != "/"
        else f"{author_name}-{app_name}-{defect_type_norm}-/"
    )

    # 构造输出文件名：包含作者/项目，case 为 "/" 时不加 case 段
    app_full_for_name = app_full  # e.g. imartinez/privateGPT
    case_segment = f"-case{case}" if case != "/" else ""
    file_stem = f"{app_full_for_name}-{defect_type_norm}{case_segment}"
    # 兼容 Windows：替换 "/" 为 "-"，统一使用连字符
    sanitized_stem = file_stem.replace("/", "-")
    file_name = sanitized_stem + ".yaml"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    # 若同名已存在，追加数字后缀确保不覆盖
    if os.path.exists(file_path):
        suffix = 2
        while True:
            candidate_name = f"{sanitized_stem}-{suffix}.yaml"
            candidate_path = os.path.join(OUTPUT_DIR, candidate_name)
            if not os.path.exists(candidate_path):
                file_name = candidate_name
                file_path = candidate_path
                break
            suffix += 1

    # 从 commit url 中拆分 repo 与 commit（形如 .../tree/<commit>）
    if "/tree/" in repo_url_raw:
        parts = repo_url_raw.split("/tree/")
        repo = parts[0]
        commit = parts[1].split("/")[0]
    else:
        repo = repo_url_raw
        commit = ""

    # consequence / locations / trigger_tests
    consequences = (
        [c.strip() for c in str(row.get("consequences", "")).split(",") if c.strip()]
        if pd.notna(row.get("consequences"))
        else []
    )
    locations = []
    if pd.notna(row.get("source-code locations")):
        for loc in str(row.get("source-code locations", "")).split("\n"):
            loc_clean = loc.strip()
            if loc_clean:
                locations.append(loc_clean)
    trigger_tests = (
        [str(row.get("defect-triggering tests", "")).strip()]
        if pd.notna(row.get("defect-triggering tests"))
        else []
    )

    # YAML 内容
    data = {
        "app": app_name,
        "repo": repo,
        "commit": commit,
        "defect_id": defect_id,
        "type": defect_type_display if defect_type_display else "unknown",
        "case": case,
        "consequence": consequences,
        "locations": locations,
        "trigger_tests": trigger_tests,
    }

    # 写入 YAML
    with open(file_path, "w", encoding="utf-8") as out:
        yaml.dump(data, out, allow_unicode=True, sort_keys=False)

    print(f"Wrote {file_path}")
