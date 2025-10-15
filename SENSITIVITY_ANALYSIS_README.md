# Probabilistic Sensitivity Analysis Feature

## 概述

这个功能允许用户对决策树进行概率敏感性分析，分析特定变量的变化如何影响决策结果。

## 功能特性

### 后端 (server.py)
- 新增 `/api/sensitivity-analysis` 接口
- 自动挂载 `output/` 目录为静态文件服务
- 支持决策节点和机会节点的敏感性分析
- 自动生成PNG格式的分析图表
- 返回图表文件的URL链接

### 前端 (HomeView.vue)
- 新增"Probabilistic Sensitivity Analysis"按钮
- 分割的可视化区域：
  - 左侧：决策树可视化
  - 右侧：敏感性分析结果
- 支持图表下载和结果清除
- 完整的错误处理和用户反馈

## 使用方法

### 1. 启动服务器
```bash
cd smart_server
python server.py
```

### 2. 构建决策树
- 在左侧控制面板创建节点
- 配置分支和概率
- 设置收益函数

### 3. 执行敏感性分析
- 点击"Probabilistic Sensitivity Analysis"按钮
- 输入要分析的变量名称
- 点击"Analyze"按钮
- 等待分析完成

### 4. 查看结果
- 右侧区域会显示敏感性分析图表
- 可以下载图表到本地
- 可以清除结果重新分析

## API接口

### 请求格式
```json
POST /api/sensitivity-analysis
{
    "json_data": {
        "nodes": [...]
    },
    "payoff_fn_code": "def payoff_fn(...): ...",
    "varname": "variable_name"
}
```

### 响应格式
```json
{
    "success": true,
    "message": "Sensitivity analysis completed for variable 'cost'",
    "node_type": "chance",
    "file_url": "http://localhost:8000/output/uuid.png"
}
```

## 文件结构

```
smart_server/
├── server.py                    # 后端服务器
├── output/                      # 图表输出目录
└── ...

src/
├── views/
│   └── HomeView.vue            # 前端主视图
├── locales/
│   ├── en.json                 # 英文翻译
│   └── zh.json                 # 中文翻译
└── ...
```

## 测试

运行测试脚本验证功能：
```bash
python test_sensitivity_analysis.py
```

## 注意事项

1. 确保 `output/` 目录存在且有写入权限
2. 敏感性分析只能对决策节点和机会节点执行
3. 图表文件使用UUID命名，避免冲突
4. 前端会自动处理图片加载错误

## 技术实现

- 使用 `smart_choice.probabilistic_sensitivity.ProbabilisticSensitivity` 类
- 支持 matplotlib 图表生成
- FastAPI 静态文件服务
- Vue.js 响应式界面
- Element Plus UI 组件库 