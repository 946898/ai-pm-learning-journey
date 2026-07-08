# tools/supplier_risk_check.py

def check_supplier_risk(supplier_name: str) -> dict:
    """
    查询供应商的履约风险数据（Mock 版本，模拟数据库查询）
    
    Args:
        supplier_name: 供应商全称，如 "鑫达物流"
    
    Returns:
        dict: 包含延迟率、合格率、资质到期日、风险等级、建议
    """
    # ---------- Mock 数据库（模拟真实数据源） ----------
    # 正常应该接入业务系统的供应商主数据
    mock_db = {
        "华诚供应链": {
            "delay_rate": 0.05,          # 历史交货延迟率 5%
            "quality_pass_rate": 0.98,   # 质量合格率 98%
            "cert_expire": "2027-12-31", # 资质到期日
        },
        "鑫达物流": {
            "delay_rate": 0.23,          # 历史交货延迟率 23% ⚠️
            "quality_pass_rate": 0.87,   # 质量合格率 87%
            "cert_expire": "2026-09-15",
        },
        "宏远电子": {
            "delay_rate": 0.02,
            "quality_pass_rate": 0.99,
            "cert_expire": "2026-11-01",
        },
        "默认": {                        # 如果传入未知供应商，用这个默认值
            "delay_rate": 0.10,
            "quality_pass_rate": 0.90,
            "cert_expire": "2027-06-30",
        },
    }

    # ---------- 获取数据（不存在则用默认值） ----------
    data = mock_db.get(supplier_name, mock_db["默认"])

    # ---------- 风险评级逻辑 ----------
    delay = data["delay_rate"]
    quality = data["quality_pass_rate"]

    if delay > 0.20 or quality < 0.90:
        risk_level = "高风险"
    elif delay > 0.10 or quality < 0.95:
        risk_level = "中风险"
    else:
        risk_level = "低风险"

    # ---------- 合作建议 ----------
    if risk_level in ["低风险", "中风险"]:
        recommendation = "建议合作，可适当放宽账期"
    else:
        recommendation = "建议暂停合作，启动备选供应商排查"

    # ---------- 返回结果 ----------
    return {
        "supplier_name": supplier_name,
        "delay_rate": data["delay_rate"],
        "quality_pass_rate": data["quality_pass_rate"],
        "cert_expire": data["cert_expire"],
        "risk_level": risk_level,
        "recommendation": recommendation,
        "data_source": "Mock DB (模拟数据，非真实查询)"
    }


# ---------- 直接运行本文件时可测试 ----------
if __name__ == "__main__":
    # 测试几个供应商
    test_suppliers = ["鑫达物流", "华诚供应链", "未知供应商"]
    for name in test_suppliers:
        print(f"\n--- 查询结果: {name} ---")
        result = check_supplier_risk(name)
        for key, value in result.items():
            print(f"  {key}: {value}")