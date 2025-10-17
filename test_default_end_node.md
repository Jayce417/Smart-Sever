# 默认结束节点功能测试文档

## 功能描述

系统现在会智能管理一个默认的结束节点 `DEFAULT_END`。当用户创建决策树节点时，如果没有为分支指定目标节点，系统会自动将该分支连接到这个默认结束节点。该节点会在需要时自动创建，也可以被用户删除。

## 实现的修改

### 1. 添加默认结束节点常量和管理函数

```javascript
// 默认结束节点常量
const DEFAULT_END_NODE = "DEFAULT_END";

// 创建默认结束节点
const createDefaultEndNode = () => {
    const defaultNode = {
        name: DEFAULT_END_NODE,
        type: "terminal",
        maximize: true,
        branches: [],
        payoffFn: "default_payoff",
        isDefaultEndNode: true, // 标记为默认结束节点
    };
    return defaultNode;
};

// 确保默认结束节点存在
const ensureDefaultEndNode = () => {
    const hasDefaultNode = nodes.value.find((n) => n.name === DEFAULT_END_NODE);
    if (!hasDefaultNode) {
        nodes.value.unshift(createDefaultEndNode()); // 添加到列表开头
    }
};

// 检查是否为默认结束节点
const isDefaultEndNode = (nodeName) => {
    return nodeName === DEFAULT_END_NODE;
};
```

### 2. 智能创建和管理默认结束节点

系统采用按需创建的策略，仅在以下情况下自动创建默认结束节点：
- 当有分支需要连接到 `DEFAULT_END` 但该节点不存在时
- 创建新节点时，如果分支目标为空或指向 `DEFAULT_END`
- 保存编辑节点时，如果分支目标为空或指向 `DEFAULT_END`
- 加载示例数据时，如果数据中引用了 `DEFAULT_END`
- 导入数据后，如果数据中有分支指向 `DEFAULT_END`

检查逻辑：
```javascript
// 检查是否需要默认结束节点
const needsDefaultEndNode = () => {
    return nodes.value.some(
        (node) =>
            node.branches &&
            node.branches.some(
                (branch) =>
                    branch.target === DEFAULT_END_NODE || !branch.target,
            ),
    );
};
```

### 3. 分支默认目标设置

#### addBranch 和 addEditBranch 函数
- 决策节点分支默认目标设置为 `DEFAULT_END_NODE`
- 机会节点分支默认目标设置为 `DEFAULT_END_NODE`

### 4. UI 增强

#### 节点列表显示
- 默认结束节点显示为特殊标签 "默认结束节点"
- 使用 `info` 类型的标签样式以区分普通节点

#### 操作特性
- 默认结束节点可以正常编辑和删除
- 删除后如果有分支仍需要它，系统会自动重新创建
- 与普通节点享有相同的操作权限

### 5. 数据处理增强

#### 节点创建和编辑
- 自动处理空的分支目标，设置为默认结束节点
- 确保数据一致性和完整性

#### 导出导入
- 导入数据后自动确保默认结束节点存在
- 保持向后兼容性

### 6. 国际化支持

添加了新的国际化文本：
- 中文：`"defaultEndNode": "默认结束节点"`
- 英文：`"defaultEndNode": "Default End Node"`

## 测试场景

### 场景1：系统初始化
1. 启动应用
2. 验证：节点列表初始为空（默认结束节点按需创建）

### 场景2：创建决策节点
1. 创建一个新的决策节点
2. 添加分支但不填写目标节点
3. 保存节点
4. 验证：分支的目标自动设置为 `DEFAULT_END`
5. 验证：默认结束节点自动出现在节点列表中
6. 验证：默认结束节点显示为灰色的 `info` 标签

### 场景3：创建机会节点
1. 创建一个新的机会节点
2. 添加分支但不填写目标节点
3. 保存节点
4. 验证：分支的目标自动设置为 `DEFAULT_END`

### 场景4：编辑现有节点
1. 编辑一个现有节点
2. 添加新分支但不填写目标节点
3. 保存修改
4. 验证：新分支的目标自动设置为 `DEFAULT_END`

### 场景5：删除和重建测试
1. 删除默认结束节点
2. 验证：默认结束节点被成功删除
3. 创建一个新节点，分支目标留空
4. 保存节点
5. 验证：默认结束节点自动重新创建
6. 验证：新分支正确连接到重新创建的默认结束节点

### 场景6：完全删除测试
1. 删除默认结束节点
2. 删除所有引用 `DEFAULT_END` 的节点和分支
3. 验证：默认结束节点不会重新创建
4. 验证：系统正常运行，无错误

### 场景7：可视化展示
1. 创建包含默认结束节点的决策树
2. 生成可视化
3. 验证：`DEFAULT_END` 节点在树中正确显示为终端节点
4. 验证：其他节点的分支正确连接到默认结束节点

### 场景8：数据导入导出
1. 导出包含默认结束节点的数据
2. 清空所有节点
3. 导入之前导出的数据
4. 验证：默认结束节点被正确重建
5. 验证：所有分支连接正确

### 场景9：加载示例数据
1. 点击"加载示例"按钮
2. 验证：示例数据加载完成
3. 验证：默认结束节点存在且功能正常

## 代码关键点

### 默认结束节点的创建
```javascript
const createDefaultEndNode = () => {
    const defaultNode = {
        name: DEFAULT_END_NODE,
        type: "terminal",
        maximize: true,
        branches: [],
        payoffFn: "default_payoff",
        isDefaultEndNode: true, // 特殊标记
    };
    return defaultNode;
};
```

### 自动确保存在性
```javascript
const ensureDefaultEndNode = () => {
    const hasDefaultNode = nodes.value.find((n) => n.name === DEFAULT_END_NODE);
    if (!hasDefaultNode) {
        nodes.value.unshift(createDefaultEndNode()); // 添加到列表开头
    }
};
```

### UI 中的特殊处理
```javascript
// 节点类型显示
isDefaultEndNode(scope.row.name)
    ? $t("home.defaultEndNode")
    : getNodeTypeName(scope.row.type)
```

### 智能创建逻辑
```javascript
// 确保默认结束节点存在（仅在需要时）
const ensureDefaultEndNode = () => {
    const hasDefaultNode = nodes.value.find((n) => n.name === DEFAULT_END_NODE);
    const needsDefault = needsDefaultEndNode();

    if (needsDefault && !hasDefaultNode) {
        nodes.value.unshift(createDefaultEndNode()); // 添加到列表开头
    }
};
```

## 预期行为

### 用户体验
1. **自动化**：用户无需手动创建结束节点
2. **简化**：分支创建时自动有默认目标
3. **灵活性**：默认节点可以根据需要删除和重建
4. **视觉区分**：默认节点有特殊的视觉标识

### 数据完整性
1. **一致性**：所有分支都有明确的目标节点
2. **完整性**：决策树结构始终完整
3. **智能管理**：默认结束节点按需存在
4. **兼容性**：与现有功能完全兼容

### 技术特性
1. **按需创建**：系统仅在需要时创建默认节点
2. **智能检测**：自动检测是否需要默认结束节点
3. **标识清晰**：通过特殊标记区分默认节点
4. **完全可操作**：默认节点支持所有标准操作

## 注意事项

1. **智能节点**：`DEFAULT_END` 是系统按需管理的特殊节点
2. **完全可操作**：默认结束节点允许用户编辑和删除
3. **按需重建**：只有在有分支需要时才会自动重新创建
4. **位置固定**：默认结束节点创建时显示在节点列表的顶部
5. **标识明确**：通过 `isDefaultEndNode` 标记和特殊UI区分
6. **功能完整**：作为真实的终端节点参与决策树的所有操作
7. **清理机制**：不需要时不会强制存在，保持界面整洁

## 兼容性说明

- ✅ 向后兼容：现有的决策树数据不受影响
- ✅ 导入兼容：旧版本导出的数据可以正常导入
- ✅ 功能兼容：所有现有功能继续正常工作
- ✅ API兼容：与后端API的交互保持一致