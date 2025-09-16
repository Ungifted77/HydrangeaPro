"""元数据管理模块"""

import os
import csv
import yaml
from typing import List, Dict, Optional, Any
from pathlib import Path


class MetadataManager:
    """元数据管理器"""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.apps_csv = self.base_dir / "application.csv"
        self.db_dir = self.base_dir / "db"
        
    def load_applications(self) -> List[Dict[str, Any]]:
        """加载应用程序数据"""
        apps = []
        if not self.apps_csv.exists():
            return apps
            
        with open(self.apps_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 清理数据
                app_data = {
                    'app': row.get('APP', '').strip(),
                    'url': row.get('url', '').strip(),
                    'classification': row.get('classification', '').strip(),
                    'commit_id': row.get('commit id', '').strip(),
                    'llm': row.get('LLM', '').strip(),
                    'llm_deployment': row.get('LLM_Deployment Environments', '').strip(),
                    'vectordb': row.get('vectordb', '').strip(),
                    'vectordb_deployment': row.get('VectorDB_Deployment Environments', '').strip(),
                    'langchain': row.get('langchain', '').strip(),
                    'language': row.get('language', '').strip()
                }
                if app_data['app']:  # 只添加非空应用
                    apps.append(app_data)
        return apps
    
    def load_defects(self) -> List[Dict[str, Any]]:
        """加载缺陷数据"""
        defects = []
        if not self.db_dir.exists():
            return defects
            
        for yaml_file in self.db_dir.glob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    defect_data = yaml.safe_load(f)
                    if defect_data:
                        defects.append(defect_data)
            except Exception as e:
                print(f"Warning: Failed to load {yaml_file}: {e}")
                continue
        return defects
    
    def get_apps_by_filters(self, 
                           classification: Optional[str] = None,
                           llm: Optional[str] = None,
                           llm_deployment: Optional[str] = None,
                           vdb: Optional[str] = None,
                           vdb_deployment: Optional[str] = None,
                           langchain: Optional[str] = None,
                           language: Optional[str] = None) -> List[str]:
        """根据多个条件过滤应用"""
        apps = self.load_applications()
        filtered_apps = []
        
        for app in apps:
            # 检查分类过滤条件
            if classification and classification.lower() not in app['classification'].lower():
                continue
                
            # 检查LLM过滤条件
            if llm and llm.lower() not in app['llm'].lower():
                continue
                
            # 检查LLM部署环境过滤条件
            if llm_deployment and llm_deployment.lower() not in app['llm_deployment'].lower():
                continue
                
            # 检查向量数据库过滤条件
            if vdb and vdb.lower() not in app['vectordb'].lower():
                continue
                
            # 检查向量数据库部署环境过滤条件
            if vdb_deployment and vdb_deployment.lower() not in app['vectordb_deployment'].lower():
                continue
                
            # 检查LangChain过滤条件
            if langchain and langchain.lower() not in app['langchain'].lower():
                continue
                
            # 检查编程语言过滤条件
            if language and language.lower() not in app['language'].lower():
                continue
                
            filtered_apps.append(app['app'])
        
        return sorted(list(set(filtered_apps)))  # 去重并排序
    
    def get_defect_ids(self, app: Optional[str] = None) -> List[str]:
        """获取缺陷ID列表"""
        defects = self.load_defects()
        defect_ids = []
        
        for defect in defects:
            if app and app.lower() not in defect.get('app', '').lower():
                continue
            defect_ids.append(defect.get('defect_id', ''))
        
        return sorted([did for did in defect_ids if did])  # 过滤空值并排序
    
    def get_defect_info(self, app: str, defect_id: str) -> Optional[Dict[str, Any]]:
        """获取特定缺陷的详细信息"""
        defects = self.load_defects()
        
        for defect in defects:
            if (defect.get('app', '').lower() == app.lower() and 
                defect.get('defect_id', '') == defect_id):
                return defect
        return None
