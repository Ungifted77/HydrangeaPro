"""CLI主入口"""

import typer
from typing import Optional
from .core.metadata import MetadataManager

app = typer.Typer(help="Hydrangea CLI - 查询Hydrangea数据集")
metadata_manager = MetadataManager()


@app.command()
def apps(
    classification: Optional[str] = typer.Option(None, "--classification", help="按分类过滤应用"),
    llm: Optional[str] = typer.Option(None, "--llm", help="按LLM过滤应用"),
    llm_deployment: Optional[str] = typer.Option(None, "--llm-deployment", help="按LLM部署环境过滤应用"),
    vdb: Optional[str] = typer.Option(None, "--vdb", help="按向量数据库过滤应用"),
    vdb_deployment: Optional[str] = typer.Option(None, "--vdb-deployment", help="按向量数据库部署环境过滤应用"),
    langchain: Optional[str] = typer.Option(None, "--langchain", help="按LangChain过滤应用"),
    language: Optional[str] = typer.Option(None, "--language", help="按编程语言过滤应用")
):
    """列出所有应用"""
    apps_list = metadata_manager.get_apps_by_filters(
        classification=classification,
        llm=llm,
        llm_deployment=llm_deployment,
        vdb=vdb,
        vdb_deployment=vdb_deployment,
        langchain=langchain,
        language=language
    )
    
    if not apps_list:
        typer.echo("No applications found.")
        return
    
    for app_name in apps_list:
        typer.echo(app_name)


@app.command()
def bids(
    app: Optional[str] = typer.Option(None, "--app", help="按应用过滤缺陷ID")
):
    """列出所有缺陷ID"""
    defect_ids = metadata_manager.get_defect_ids(app=app)
    
    if not defect_ids:
        typer.echo("No defect IDs found.")
        return
    
    for defect_id in defect_ids:
        typer.echo(defect_id)


@app.command()
def info(
    app: str = typer.Argument(..., help="应用名称"),
    bid: str = typer.Argument(..., help="缺陷ID")
):
    """显示缺陷元数据"""
    defect_info = metadata_manager.get_defect_info(app, bid)
    
    if not defect_info:
        typer.echo(f"Defect not found: {app} - {bid}")
        return
    
    # 格式化输出
    typer.echo(f"app: {defect_info.get('app', 'N/A')}")
    typer.echo(f"repo: {defect_info.get('repo', 'N/A')}")
    typer.echo(f"commit: {defect_info.get('commit', 'N/A')}")
    typer.echo(f"defect_id: {defect_info.get('defect_id', 'N/A')}")
    typer.echo(f"type: {defect_info.get('type', 'N/A')}")
    typer.echo(f"case: {defect_info.get('case', 'N/A')}")
    
    # 输出consequence
    consequences = defect_info.get('consequence', [])
    if consequences:
        typer.echo("consequence:")
        for cons in consequences:
            typer.echo(f"  - {cons}")
    
    # 输出locations
    locations = defect_info.get('locations', [])
    if locations:
        typer.echo("locations:")
        for loc in locations:
            typer.echo(f"  - {loc}")


@app.command()
def test(
    app: str = typer.Argument(..., help="应用名称"),
    bid: str = typer.Argument(..., help="缺陷ID"),
    trigger: bool = typer.Option(False, "--trigger", help="显示触发测试")
):
    """显示测试信息（仅打印，不执行）"""
    # 获取特定缺陷的信息
    defect_info = metadata_manager.get_defect_info(app, bid)
    
    if not defect_info:
        typer.echo(f"Defect not found: {app} - {bid}")
        return
    
    if trigger:
        # 显示触发测试
        trigger_tests = defect_info.get('trigger_tests', [])
        if trigger_tests:
            typer.echo("trigger_tests:")
            for test in trigger_tests:
                if test.strip():
                    typer.echo(f"- {test}")
        else:
            typer.echo("No trigger tests available for this defect.")
    else:
        # 显示基本测试信息
        typer.echo(f"Test information for {app} - {bid}")
        typer.echo(f"Defect type: {defect_info.get('type', 'N/A')}")
        typer.echo(f"Case: {defect_info.get('case', 'N/A')}")
        typer.echo("Use --trigger to see detailed trigger tests")


def main():
    """主入口函数"""
    app()


if __name__ == "__main__":
    main()
