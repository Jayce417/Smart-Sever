<template>
    <div class="decision-tree-container">
        <el-container>
            <el-header height="60px">
                <div class="header-content">
                    <h1 class="main-title">{{ $t("home.title") }}</h1>
                    <div class="header-controls">
                        <el-select
                            v-model="$i18n.locale"
                            size="small"
                            class="language-selector"
                        >
                            <el-option label="English" value="en" />
                            <!-- <el-option label="中文" value="zh" /> -->
                        </el-select>
                    </div>
                </div>
            </el-header>

            <el-main>
                <el-row :gutter="20">
                    <!-- 左侧控制面板 -->
                    <el-col :span="8">
                        <el-card class="control-panel" shadow="hover">
                            <template #header>
                                <div class="card-header">
                                    <span class="card-title">{{
                                        $t("home.nodeManagement")
                                    }}</span>
                                    <el-button
                                        type="primary"
                                        size="small"
                                        @click="showCreateNodeDialog = true"
                                    >
                                        <el-icon>
                                            <Plus />
                                        </el-icon>
                                        {{ $t("home.createNode") }}
                                    </el-button>
                                </div>
                            </template>

                            <!-- 节点列表 -->
                            <div class="node-list">
                                <h3 class="section-title">
                                    {{ $t("home.createdNodes") }}
                                </h3>
                                <el-table
                                    :data="nodes"
                                    style="width: 100%"
                                    :header-cell-style="{
                                        background: '#f5f7fa',
                                        color: '#606266',
                                    }"
                                    stripe
                                    size="small"
                                >
                                    <el-table-column
                                        prop="name"
                                        :label="$t('home.nodeName')"
                                    />
                                    <el-table-column
                                        prop="type"
                                        :label="$t('home.type')"
                                        width="120"
                                    >
                                        <template #default="scope">
                                            <el-tag
                                                :type="
                                                    isDefaultEndNode(
                                                        scope.row.name,
                                                    )
                                                        ? 'info'
                                                        : getNodeTypeColor(
                                                              scope.row.type,
                                                          )
                                                "
                                                size="small"
                                            >
                                                {{
                                                    isDefaultEndNode(
                                                        scope.row.name,
                                                    )
                                                        ? $t(
                                                              "home.defaultEndNode",
                                                          )
                                                        : getNodeTypeName(
                                                              scope.row.type,
                                                          )
                                                }}
                                            </el-tag>
                                        </template>
                                    </el-table-column>
                                    <el-table-column
                                        :label="$t('home.actions')"
                                        width="150"
                                    >
                                        <template #default="scope">
                                            <el-button
                                                size="small"
                                                @click="editNode(scope.row)"
                                            >
                                                <el-icon>
                                                    <Edit />
                                                </el-icon>
                                                {{ $t("home.edit") }}
                                            </el-button>
                                            <el-button
                                                size="small"
                                                type="danger"
                                                @click="deleteNode(scope.row)"
                                            >
                                                <el-icon>
                                                    <Delete />
                                                </el-icon>
                                                {{ $t("home.delete") }}
                                            </el-button>
                                        </template>
                                    </el-table-column>
                                </el-table>
                            </div>

                            <!-- 可视化控制 -->
                            <div
                                class="visualization-controls"
                                style="margin-top: 20px"
                            >
                                <div class="control-section">
                                    <h5 class="section-title">
                                        {{ $t("home.dataManagement") }}
                                    </h5>
                                    <div class="button-group">
                                        <el-button
                                            type="info"
                                            size="small"
                                            @click="loadExample"
                                        >
                                            <el-icon>
                                                <Document />
                                            </el-icon>
                                            {{ $t("home.loadExample") }}
                                        </el-button>
                                        <el-button
                                            type="info"
                                            size="small"
                                            @click="loadExample2"
                                        >
                                            <el-icon>
                                                <Document />
                                            </el-icon>
                                            Example 2
                                        </el-button>
                                        <el-button
                                            type="warning"
                                            size="small"
                                            @click="exportData"
                                            :disabled="nodes.length === 0"
                                        >
                                            <el-icon>
                                                <Download />
                                            </el-icon>
                                            {{ $t("home.exportData") }}
                                        </el-button>
                                        <el-button
                                            type="primary"
                                            size="small"
                                            @click="importData"
                                        >
                                            <el-icon>
                                                <Upload />
                                            </el-icon>
                                            {{ $t("home.importData") }}
                                        </el-button>
                                    </div>
                                </div>

                                <div class="control-section">
                                    <h5 class="section-title">
                                        {{ $t("home.analysis") }}
                                    </h5>
                                    <div class="button-group">
                                        <el-button
                                            type="danger"
                                            size="small"
                                            @click="generateTree"
                                            :disabled="nodes.length === 0"
                                        >
                                            <el-icon>
                                                <Share />
                                            </el-icon>
                                            {{
                                                $t("home.generateDecisionTree")
                                            }}
                                        </el-button>
                                        <el-button
                                            type="success"
                                            size="small"
                                            @click="
                                                showSensitivityAnalysisDialog = true
                                            "
                                            :disabled="nodes.length === 0"
                                        >
                                            <el-icon>
                                                <TrendCharts />
                                            </el-icon>
                                            {{
                                                $t(
                                                    "home.probabilisticSensitivityAnalysis",
                                                )
                                            }}
                                        </el-button>
                                        <el-button
                                            type="info"
                                            size="small"
                                            @click="
                                                showRiskProfileDialog = true
                                            "
                                            :disabled="nodes.length === 0"
                                        >
                                            <el-icon>
                                                <DataAnalysis />
                                            </el-icon>
                                            {{ $t("home.riskProfile") }}
                                        </el-button>
                                    </div>
                                </div>
                            </div>

                            <!-- Payoff函数配置 -->
                            <div class="payoff-config" style="margin-top: 20px">
                                <h4 class="section-title">
                                    Terminal Node Calculation Function
                                </h4>

                                <div class="code-editor-container">
                                    <el-input
                                        v-model="payoffFunction"
                                        type="textarea"
                                        :rows="12"
                                        class="code-editor"
                                        :placeholder="
                                            $t('home.enterPayoffFunction')
                                        "
                                    />
                                </div>

                                <div class="function-actions">
                                    <el-button
                                        type="success"
                                        size="small"
                                        @click="savePayoffFunction"
                                    >
                                        <el-icon>
                                            <Check />
                                        </el-icon>
                                        {{ $t("home.saveFunction") }}
                                    </el-button>
                                    <el-button
                                        size="small"
                                        @click="resetPayoffFunction"
                                    >
                                        <el-icon>
                                            <Refresh />
                                        </el-icon>
                                        {{ $t("home.resetToDefault") }}
                                    </el-button>
                                </div>
                            </div>

                            <!-- 收益函数配置模块 -->
                            <div class="payoff-config" style="margin-top: 20px">
                                <h4 class="section-title">
                                    Payoff Function Configuration
                                </h4>

                                <!-- 方法选择 -->
                                <div style="margin-bottom: 15px">
                                    <label
                                        style="
                                            display: block;
                                            margin-bottom: 5px;
                                            font-weight: 500;
                                        "
                                        >Method:</label
                                    >
                                    <el-select
                                        v-model="payoffConfig.method"
                                        style="width: 100%"
                                    >
                                        <el-option
                                            label="Expected Value (EV)"
                                            value="ev"
                                        />
                                        <el-option
                                            label="Certainty Equivalent (CE)"
                                            value="ce"
                                        />
                                        <el-option
                                            label="Expected Utility (EU)"
                                            value="eu"
                                        />
                                    </el-select>
                                </div>

                                <!-- 效用函数选择 -->
                                <div style="margin-bottom: 15px">
                                    <label
                                        style="
                                            display: block;
                                            margin-bottom: 5px;
                                            font-weight: 500;
                                        "
                                        >Utility Function:</label
                                    >
                                    <el-select
                                        v-model="payoffConfig.utility_fn"
                                        style="width: 100%"
                                    >
                                        <el-option
                                            label="None (Expected Utility)"
                                            value="None"
                                        />
                                        <el-option
                                            label="Exponential Utility Function"
                                            value="exp"
                                        />
                                        <el-option
                                            label="Logarithmic Utility Function"
                                            value="log"
                                        />
                                    </el-select>
                                </div>

                                <!-- 风险容忍度 -->
                                <div style="margin-bottom: 15px">
                                    <label
                                        style="
                                            display: block;
                                            margin-bottom: 5px;
                                            font-weight: 500;
                                        "
                                        >Risk Tolerance:</label
                                    >
                                    <el-input-number
                                        v-model="payoffConfig.risk_tolerance"
                                        :step="0.1"
                                        :precision="2"
                                        style="width: 100%"
                                    />
                                </div>
                            </div>
                        </el-card>
                    </el-col>

                    <!-- 右侧可视化区域 -->
                    <el-col :span="16">
                        <el-card class="visualization-area" shadow="hover">
                            <template #header>
                                <div class="card-header">
                                    <span class="card-title">{{
                                        $t("home.decisionTreeVisualization")
                                    }}</span>
                                    <div class="interaction-controls">
                                        <el-button
                                            size="small"
                                            @click="resetZoom"
                                            :disabled="!hasGraphviz"
                                        >
                                            <el-icon>
                                                <Refresh />
                                            </el-icon>
                                            {{ $t("home.resetZoom") }}
                                        </el-button>
                                        <el-button
                                            size="small"
                                            @click="fitGraph"
                                            :disabled="!hasGraphviz"
                                        >
                                            <el-icon>
                                                <FullScreen />
                                            </el-icon>
                                            {{ $t("home.fitWindow") }}
                                        </el-button>
                                        <el-button
                                            size="small"
                                            @click="toggleZoom"
                                            :disabled="!hasGraphviz"
                                        >
                                            <el-icon>
                                                <ZoomIn />
                                            </el-icon>
                                            {{
                                                zoomEnabled
                                                    ? $t("home.disableZoom")
                                                    : $t("home.enableZoom")
                                            }}
                                        </el-button>
                                        <el-button
                                            size="small"
                                            @click="showPreviewDialog = true"
                                            :disabled="nodes.length === 0"
                                        >
                                            <el-icon>
                                                <View />
                                            </el-icon>
                                            {{
                                                $t("home.preview") || "Preview"
                                            }}
                                        </el-button>
                                    </div>
                                </div>
                            </template>

                            <!-- 决策树可视化区域 -->
                            <div
                                id="tree-container"
                                class="tree-container"
                            ></div>

                            <!-- 敏感性分析结果区域 -->
                            <div
                                v-if="sensitivityAnalysisResult"
                                class="sensitivity-analysis-section"
                            >
                                <el-divider content-position="left">
                                    <h4>
                                        {{
                                            $t(
                                                "home.sensitivityAnalysisResults",
                                            )
                                        }}
                                    </h4>
                                </el-divider>
                                <div class="sensitivity-results">
                                    <div class="result-content">
                                        <div class="result-info">
                                            <el-tag
                                                :type="
                                                    getNodeTypeColor(
                                                        sensitivityAnalysisResult.node_type,
                                                    )
                                                "
                                            >
                                                {{
                                                    getNodeTypeName(
                                                        sensitivityAnalysisResult.node_type,
                                                    )
                                                }}
                                            </el-tag>
                                            <span class="variable-name">{{
                                                sensitivityAnalysisResult.varname
                                            }}</span>
                                        </div>
                                        <div class="result-image">
                                            <img
                                                :src="
                                                    sensitivityAnalysisResult.file_url
                                                "
                                                :alt="
                                                    $t(
                                                        'home.sensitivityAnalysisChart',
                                                    )
                                                "
                                                @error="handleImageError"
                                                class="sensitivity-chart"
                                            />
                                        </div>
                                        <div class="result-actions">
                                            <el-button
                                                type="primary"
                                                size="small"
                                                @click="
                                                    downloadSensitivityImage
                                                "
                                                :disabled="
                                                    !sensitivityAnalysisResult.file_url
                                                "
                                            >
                                                {{ $t("home.downloadChart") }}
                                            </el-button>
                                            <el-button
                                                size="small"
                                                @click="clearSensitivityResults"
                                            >
                                                {{ $t("home.clearResults") }}
                                            </el-button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </el-card>
                    </el-col>
                </el-row>
            </el-main>
        </el-container>

        <!-- 创建节点对话框 -->
        <el-dialog
            v-model="showCreateNodeDialog"
            :title="$t('home.createNodeTitle')"
            width="600px"
        >
            <el-form :model="newNode" label-width="120px">
                <el-form-item :label="$t('home.nodeNameLabel')">
                    <el-input
                        v-model="newNode.name"
                        :placeholder="$t('home.nodeNamePlaceholder')"
                    />
                </el-form-item>

                <el-form-item :label="$t('home.nodeTypeLabel')">
                    <el-select
                        v-model="newNode.type"
                        :placeholder="$t('home.nodeTypePlaceholder')"
                    >
                        <el-option
                            :label="$t('home.decisionNode')"
                            value="decision"
                        />
                        <el-option
                            :label="$t('home.chanceNode')"
                            value="chance"
                        />
                        <el-option
                            :label="$t('home.terminalNode')"
                            value="terminal"
                        />
                    </el-select>
                </el-form-item>

                <!-- 决策节点配置 -->
                <template v-if="newNode.type === 'decision'">
                    <el-form-item :label="$t('home.maximize')">
                        <el-switch v-model="newNode.maximize" />
                    </el-form-item>

                    <el-form-item :label="$t('home.branchConfig')">
                        <div
                            v-for="(branch, index) in newNode.branches"
                            :key="index"
                            class="branch-item"
                        >
                            <div class="branch-form">
                                <el-form-item
                                    :label="$t('home.branchName')"
                                    label-width="80px"
                                >
                                    <el-input
                                        v-model="branch.name"
                                        :placeholder="
                                            $t('home.branchNamePlaceholder')
                                        "
                                    />
                                </el-form-item>
                                <el-form-item
                                    :label="$t('home.value')"
                                    label-width="80px"
                                >
                                    <el-input
                                        v-model="branch.value"
                                        :placeholder="
                                            $t('home.valuePlaceholder')
                                        "
                                    />
                                </el-form-item>
                                <el-form-item
                                    :label="$t('home.targetNode')"
                                    label-width="80px"
                                >
                                    <el-input
                                        v-model="branch.target"
                                        :placeholder="
                                            $t('home.targetNodePlaceholder')
                                        "
                                    />
                                </el-form-item>
                                <el-form-item>
                                    <el-button
                                        type="danger"
                                        size="small"
                                        @click="removeBranch(index)"
                                        >{{
                                            $t("home.deleteBranch")
                                        }}</el-button
                                    >
                                </el-form-item>
                            </div>
                        </div>
                        <el-button
                            type="primary"
                            size="small"
                            @click="addBranch"
                            >{{ $t("home.addBranch") }}</el-button
                        >
                    </el-form-item>
                </template>

                <!-- 机会节点配置 -->
                <template v-if="newNode.type === 'chance'">
                    <el-form-item :label="$t('home.branchConfig')">
                        <div
                            v-for="(branch, index) in newNode.branches"
                            :key="index"
                            class="branch-item"
                        >
                            <div class="branch-form">
                                <el-form-item
                                    :label="$t('home.branchName')"
                                    label-width="80px"
                                >
                                    <el-input
                                        v-model="branch.name"
                                        :placeholder="
                                            $t('home.branchNamePlaceholder')
                                        "
                                    />
                                </el-form-item>
                                <el-form-item
                                    :label="$t('home.probability')"
                                    label-width="80px"
                                >
                                    <el-input
                                        v-model="branch.probability"
                                        :placeholder="
                                            $t('home.probabilityPlaceholder')
                                        "
                                    />
                                </el-form-item>
                                <el-form-item
                                    :label="$t('home.value')"
                                    label-width="80px"
                                >
                                    <el-input
                                        v-model="branch.value"
                                        :placeholder="
                                            $t('home.valuePlaceholder')
                                        "
                                    />
                                </el-form-item>
                                <el-form-item
                                    :label="$t('home.targetNode')"
                                    label-width="80px"
                                >
                                    <el-input
                                        v-model="branch.target"
                                        :placeholder="
                                            $t('home.targetNodePlaceholder')
                                        "
                                    />
                                </el-form-item>
                                <el-form-item>
                                    <el-button
                                        type="danger"
                                        size="small"
                                        @click="removeBranch(index)"
                                        >{{
                                            $t("home.deleteBranch")
                                        }}</el-button
                                    >
                                </el-form-item>
                            </div>
                        </div>
                        <el-button
                            type="primary"
                            size="small"
                            @click="addBranch"
                            >{{ $t("home.addBranch") }}</el-button
                        >
                    </el-form-item>
                </template>

                <!-- 结束节点配置 -->
                <template v-if="newNode.type === 'terminal'">
                    <el-form-item :label="$t('home.payoffFunction')">
                        <el-input
                            v-model="newNode.payoffFn"
                            :placeholder="$t('home.payoffFunctionName')"
                        />
                    </el-form-item>
                </template>
            </el-form>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="showCreateNodeDialog = false">{{
                        $t("home.cancel")
                    }}</el-button>
                    <el-button type="primary" @click="createNode">{{
                        $t("home.create")
                    }}</el-button>
                </span>
            </template>
        </el-dialog>

        <!-- 编辑节点对话框 -->
        <el-dialog
            v-model="showEditNodeDialog"
            :title="$t('home.editNodeTitle')"
            width="600px"
        >
            <el-form :model="editingNode" label-width="120px">
                <el-form-item :label="$t('home.nodeNameLabel')">
                    <el-input
                        v-model="editingNode.name"
                        :placeholder="$t('home.nodeNamePlaceholder')"
                    />
                </el-form-item>

                <el-form-item :label="$t('home.nodeTypeLabel')">
                    <el-select
                        v-model="editingNode.type"
                        :placeholder="$t('home.nodeTypePlaceholder')"
                        disabled
                    >
                        <el-option
                            :label="$t('home.decisionNode')"
                            value="decision"
                        />
                        <el-option
                            :label="$t('home.chanceNode')"
                            value="chance"
                        />
                        <el-option
                            :label="$t('home.terminalNode')"
                            value="terminal"
                        />
                    </el-select>
                </el-form-item>

                <!-- 决策节点配置 -->
                <template v-if="editingNode.type === 'decision'">
                    <el-form-item :label="$t('home.maximize')">
                        <el-switch v-model="editingNode.maximize" />
                    </el-form-item>

                    <el-form-item :label="$t('home.branchConfig')">
                        <div
                            v-for="(branch, index) in editingNode.branches"
                            :key="index"
                            class="branch-item"
                        >
                            <div class="branch-form">
                                <el-form-item
                                    :label="$t('home.branchName')"
                                    label-width="80px"
                                >
                                    <el-input
                                        v-model="branch.name"
                                        :placeholder="
                                            $t('home.branchNamePlaceholder')
                                        "
                                    />
                                </el-form-item>
                                <el-form-item
                                    :label="$t('home.value')"
                                    label-width="80px"
                                >
                                    <el-input
                                        v-model="branch.value"
                                        :placeholder="
                                            $t('home.valuePlaceholder')
                                        "
                                    />
                                </el-form-item>
                                <el-form-item
                                    :label="$t('home.targetNode')"
                                    label-width="80px"
                                >
                                    <el-input
                                        v-model="branch.target"
                                        :placeholder="
                                            $t('home.targetNodePlaceholder')
                                        "
                                    />
                                </el-form-item>
                                <el-form-item>
                                    <el-button
                                        type="danger"
                                        size="small"
                                        @click="removeEditBranch(index)"
                                        >{{
                                            $t("home.deleteBranch")
                                        }}</el-button
                                    >
                                </el-form-item>
                            </div>
                        </div>
                        <el-button
                            type="primary"
                            size="small"
                            @click="addEditBranch"
                            >{{ $t("home.addBranch") }}</el-button
                        >
                    </el-form-item>
                </template>

                <!-- 机会节点配置 -->
                <template v-if="editingNode.type === 'chance'">
                    <el-form-item :label="$t('home.branchConfig')">
                        <div
                            v-for="(branch, index) in editingNode.branches"
                            :key="index"
                            class="branch-item"
                        >
                            <div class="branch-form">
                                <el-form-item
                                    :label="$t('home.branchName')"
                                    label-width="80px"
                                >
                                    <el-input
                                        v-model="branch.name"
                                        :placeholder="
                                            $t('home.branchNamePlaceholder')
                                        "
                                    />
                                </el-form-item>
                                <el-form-item
                                    :label="$t('home.probability')"
                                    label-width="80px"
                                >
                                    <el-input
                                        v-model="branch.probability"
                                        :placeholder="
                                            $t('home.probabilityPlaceholder')
                                        "
                                    />
                                </el-form-item>
                                <el-form-item
                                    :label="$t('home.value')"
                                    label-width="80px"
                                >
                                    <el-input
                                        v-model="branch.value"
                                        :placeholder="
                                            $t('home.valuePlaceholder')
                                        "
                                    />
                                </el-form-item>
                                <el-form-item
                                    :label="$t('home.targetNode')"
                                    label-width="80px"
                                >
                                    <el-input
                                        v-model="branch.target"
                                        :placeholder="
                                            $t('home.targetNodePlaceholder')
                                        "
                                    />
                                </el-form-item>
                                <el-form-item>
                                    <el-button
                                        type="danger"
                                        size="small"
                                        @click="removeEditBranch(index)"
                                        >{{
                                            $t("home.deleteBranch")
                                        }}</el-button
                                    >
                                </el-form-item>
                            </div>
                        </div>
                        <el-button
                            type="primary"
                            size="small"
                            @click="addEditBranch"
                            >{{ $t("home.addBranch") }}</el-button
                        >
                    </el-form-item>
                </template>

                <!-- 结束节点配置 -->
                <template v-if="editingNode.type === 'terminal'">
                    <el-form-item :label="$t('home.payoffFunction')">
                        <el-input
                            v-model="editingNode.payoffFn"
                            :placeholder="$t('home.payoffFunctionName')"
                        />
                    </el-form-item>
                </template>
            </el-form>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="showEditNodeDialog = false">{{
                        $t("home.cancel")
                    }}</el-button>
                    <el-button type="primary" @click="saveNodeEdit">{{
                        $t("home.save")
                    }}</el-button>
                </span>
            </template>
        </el-dialog>

        <!-- Probabilistic Sensitivity Analysis对话框 -->
        <el-dialog
            v-model="showSensitivityAnalysisDialog"
            :title="$t('home.sensitivityAnalysisTitle')"
            width="700px"
            @close="clearSensitivityResults"
        >
            <el-form
                :model="sensitivityAnalysisForm"
                label-width="120px"
                @submit.prevent
            >
                <el-form-item :label="$t('home.variableName')" required>
                    <el-input
                        v-model="sensitivityAnalysisForm.varname"
                        :placeholder="$t('home.variableNamePlaceholder')"
                        @keydown.enter.prevent="performSensitivityAnalysis"
                    />
                </el-form-item>
            </el-form>

            <!-- 敏感性分析结果图片显示 -->
            <div v-if="sensitivityAnalysisResult" class="dialog-results">
                <el-divider content-position="left">
                    <h4>{{ $t("home.analysisResults") }}</h4>
                </el-divider>

                <div class="result-summary">
                    <div class="result-info">
                        <el-tag
                            :type="
                                getNodeTypeColor(
                                    sensitivityAnalysisResult.node_type,
                                )
                            "
                        >
                            {{
                                getNodeTypeName(
                                    sensitivityAnalysisResult.node_type,
                                )
                            }}
                        </el-tag>
                        <span class="variable-name">{{
                            sensitivityAnalysisResult.varname
                        }}</span>
                    </div>

                    <div class="result-image-container">
                        <img
                            :src="sensitivityAnalysisResult.file_url"
                            :alt="$t('home.sensitivityAnalysisChart')"
                            @error="handleImageError"
                            class="result-image"
                        />
                    </div>

                    <div class="result-actions">
                        <el-button
                            type="primary"
                            size="small"
                            @click="downloadSensitivityImage"
                            :disabled="!sensitivityAnalysisResult.file_url"
                        >
                            {{ $t("home.downloadChart") }}
                        </el-button>
                        <el-button
                            size="small"
                            @click="clearSensitivityResults"
                        >
                            {{ $t("home.clearResults") }}
                        </el-button>
                    </div>
                </div>
            </div>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="showSensitivityAnalysisDialog = false">{{
                        $t("home.cancel")
                    }}</el-button>
                    <el-button
                        type="primary"
                        @click="performSensitivityAnalysis"
                        :loading="sensitivityAnalysisLoading"
                    >
                        {{ $t("home.analyze") }}
                    </el-button>
                </span>
            </template>
        </el-dialog>

        <!-- Risk Profile对话框 -->
        <el-dialog
            v-model="showRiskProfileDialog"
            :title="$t('home.riskProfileTitle')"
            width="700px"
            @close="clearRiskProfileResults"
        >
            <el-form :model="riskProfileForm" label-width="120px">
                <el-form-item :label="$t('home.nodeIndex')" required>
                    <el-input-number
                        v-model="riskProfileForm.idx"
                        :min="0"
                        :max="nodes.length - 1"
                        :placeholder="$t('home.nodeIndexPlaceholder')"
                    />
                </el-form-item>

                <el-form-item :label="$t('home.cumulative')">
                    <el-switch v-model="riskProfileForm.cumulative" />
                </el-form-item>

                <el-form-item :label="$t('home.single')">
                    <el-switch v-model="riskProfileForm.single" />
                </el-form-item>
            </el-form>

            <!-- Risk Profile结果图片显示 -->
            <div v-if="riskProfileResult" class="dialog-results">
                <el-divider content-position="left">
                    <h4>{{ $t("home.riskProfileResults") }}</h4>
                </el-divider>

                <div class="result-summary">
                    <div class="result-info">
                        <span class="variable-name"
                            >{{ $t("home.nodeIndex") }}:
                            {{ riskProfileForm.idx }}</span
                        >
                        <el-tag
                            :type="
                                riskProfileForm.cumulative
                                    ? 'success'
                                    : 'primary'
                            "
                        >
                            {{
                                riskProfileForm.cumulative
                                    ? $t("home.cumulative")
                                    : $t("home.nonCumulative")
                            }}
                        </el-tag>
                        <el-tag
                            :type="riskProfileForm.single ? 'warning' : 'info'"
                        >
                            {{
                                riskProfileForm.single
                                    ? $t("home.single")
                                    : $t("home.multiple")
                            }}
                        </el-tag>
                    </div>

                    <div class="result-image-container">
                        <img
                            :src="riskProfileResult.file_url"
                            :alt="$t('home.riskProfileChart')"
                            @error="handleImageError"
                            class="result-image"
                        />
                    </div>

                    <div class="result-actions">
                        <el-button
                            type="primary"
                            size="small"
                            @click="downloadRiskProfileImage"
                            :disabled="!riskProfileResult.file_url"
                        >
                            {{ $t("home.downloadChart") }}
                        </el-button>
                        <el-button
                            size="small"
                            @click="clearRiskProfileResults"
                        >
                            {{ $t("home.clearResults") }}
                        </el-button>
                    </div>
                </div>
            </div>

            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="showRiskProfileDialog = false">{{
                        $t("home.cancel")
                    }}</el-button>
                    <el-button
                        type="primary"
                        @click="performRiskProfileAnalysis"
                        :loading="riskProfileLoading"
                    >
                        {{ $t("home.analyze") }}
                    </el-button>
                </span>
            </template>
        </el-dialog>

        <el-dialog
            v-model="showPreviewDialog"
            :title="$t('home.preview') || 'Preview'"
            width="80vw"
            :before-close="
                () => {
                    showPreviewDialog = false;
                }
            "
            @open="onPreviewOpen"
        >
            <div style="height: 80vh; width: 100%">
                <div id="preview-graph" style="width: 100%; height: 100%"></div>
            </div>
            <template #footer>
                <el-button size="small" @click="showPreviewDialog = false">{{
                    $t("home.close") || "Close"
                }}</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import * as echarts from "echarts";
import * as d3 from "d3";
import { ElMessage, ElMessageBox } from "element-plus";
import axios from "axios";
import { useI18n } from "vue-i18n";
import {
    Plus,
    Refresh,
    FullScreen,
    ZoomIn,
    View,
    Delete,
    Document,
    Upload,
    Download,
    Share,
    TrendCharts,
    DataAnalysis,
    Edit,
    Check,
} from "@element-plus/icons-vue";

const { t } = useI18n();

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

// 确保默认结束节点存在（仅在需要时）
const ensureDefaultEndNode = () => {
    const hasDefaultNode = nodes.value.find((n) => n.name === DEFAULT_END_NODE);
    const needsDefault = needsDefaultEndNode();

    if (needsDefault && !hasDefaultNode) {
        nodes.value.unshift(createDefaultEndNode()); // 添加到列表开头
    }
};

// 检查是否为默认结束节点
const isDefaultEndNode = (nodeName) => {
    return nodeName === DEFAULT_END_NODE;
};

// 响应式数据
const nodes = ref([]);
const showCreateNodeDialog = ref(false);
const showEditNodeDialog = ref(false);
const editingNodeIndex = ref(-1);
const payoffFunction = ref("");
const hasGraphviz = ref(false);
const zoomEnabled = ref(true);
const currentGraphviz = ref(null);
const showSensitivityAnalysisDialog = ref(false);
const sensitivityAnalysisLoading = ref(false);

// 敏感性分析结果
const sensitivityAnalysisResult = ref(null);

// Risk Profile相关
const showRiskProfileDialog = ref(false);

// 预览弹窗控制
const showPreviewDialog = ref(false);

// 将当前 nodes 格式转换为边列表（兼容当前 nodes 的结构：branch.target / branch.name）
function convertDecisionTreeData(decisionTreeData) {
    const edgeList = [];
    decisionTreeData.forEach((node) => {
        if (node.branches && node.branches.length > 0) {
            const sourceNode = node.name;
            node.branches.forEach((branch) => {
                const targetNode = branch.next || branch.target || null;
                const label =
                    branch.label !== undefined ? branch.label : branch.name;
                let edgeLabel = `${label}: (value: ${branch.value}`;
                if (
                    branch.probability !== undefined &&
                    branch.probability !== null
                ) {
                    edgeLabel += `, p: ${branch.probability}`;
                }
                edgeLabel += ")";
                if (targetNode) {
                    edgeList.push({
                        src: sourceNode,
                        dst: targetNode,
                        edge: edgeLabel,
                    });
                }
            });
        }
    });
    return edgeList;
}

// ==================================================================
// 2. 修正后的通用渲染函数
// ==================================================================
/**
 * 渲染带边标签的树状图
 * @param {Array<Object>} data - 边列表数据，格式为 [{"src": "...", "dst": "...", "edge": "..."}]
 * @param {string} containerId - 用于承载SVG图表的DIV容器的ID
 */
function renderTreeWithLabels(data, containerId) {
    // === 修正后的 buildHierarchy 函数 ===
    function buildHierarchy(edgeListData) {
        const nodeMap = new Map(); // 存储所有节点对象
        const parentChildLinks = new Map(); // 存储父子节点之间的具体链接数据

        // 确保所有节点都被创建
        edgeListData.forEach((item) => {
            if (!nodeMap.has(item.src))
                nodeMap.set(item.src, {
                    name: item.src,
                    children: [],
                });
            if (!nodeMap.has(item.dst))
                nodeMap.set(item.dst, {
                    name: item.dst,
                    children: [],
                });
        });

        // 构建层次结构并存储链接数据
        edgeListData.forEach((item) => {
            const srcNode = nodeMap.get(item.src);
            const dstNode = nodeMap.get(item.dst);

            // 在父节点的children数组中，不仅仅是子节点本身，还要包含这条边的数据
            // 这允许 D3 的 hierarchy 和 tree layout 在遍历时携带这些信息
            srcNode.children.push({
                name: dstNode.name, // 子节点的名字
                children: dstNode.children, // 子节点的后代
                linkData: {
                    // 存储这条边的详细信息，包括标签
                    src: item.src,
                    dst: item.dst,
                    edgeLabel: item.edge, // 修正后的边标签
                },
            });
        });

        // 找到根节点
        const destinations = new Set(edgeListData.map((d) => d.dst));
        const roots = Array.from(nodeMap.values()).filter(
            (node) => !destinations.has(node.name),
        );
        return roots[0] || null; // 假设是单根树
    }
    // === buildHierarchy 函数结束 ===

    const container = d3.select(`#${containerId}`);
    if (container.empty()) {
        console.error(`错误：找不到ID为 "${containerId}" 的容器。`);
        return;
    }
    if (!data || data.length === 0) {
        container.html("<p>无数据显示。</p>");
        return;
    }

    const hierarchicalData = buildHierarchy(data);
    if (!hierarchicalData) {
        console.error("错误：无法从数据中构建树结构，请检查是否存在根节点。");
        container.html("<p>数据格式错误，无法生成树状图。</p>");
        return;
    }

    container.html(""); // 清空容器
    const { width, height } = container.node().getBoundingClientRect();
    const margin = { top: 40, right: 120, bottom: 40, left: 120 };

    const treeLayout = d3
        .tree()
        .size([
            height - margin.top - margin.bottom,
            width - margin.left - margin.right,
        ]);

    // 重要：在这里，d3.hierarchy 会根据我们修改后的结构正确识别 children
    const root = d3.hierarchy(hierarchicalData, (d) => d.children); // 显式指定 children 访问器
    treeLayout(root);

    const svg = container
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", [0, 0, width, height])
        .style("user-select", "none")
        .style("background", "transparent");

    // defs: drop shadow for nodes
    const defs = svg.append("defs");
    defs.append("filter")
        .attr("id", "dt-drop-shadow")
        .attr("height", "130%")
        .append("feDropShadow")
        .attr("dx", 0)
        .attr("dy", 2)
        .attr("stdDeviation", 3)
        .attr("flood-color", "#2b6fc3")
        .attr("flood-opacity", 0.12);

    const g = svg.append("g");

    const linkGenerator = d3
        .linkHorizontal()
        .x((d) => d.y)
        .y((d) => d.x);

    // links with nicer color and rounded caps
    g.append("g")
        .attr("class", "links")
        .selectAll("path")
        .data(root.links())
        .join("path")
        .attr("class", "link")
        .attr("d", linkGenerator)
        .attr("fill", "none")
        .attr("stroke", "#6EA8FE")
        .attr("stroke-width", 2)
        .attr("stroke-linecap", "round")
        .attr("opacity", 0.95);

    // nodes
    const node = g
        .append("g")
        .attr("class", "nodes")
        .selectAll("g")
        .data(root.descendants())
        .join("g")
        .attr("class", "node")
        .attr("transform", (d) => `translate(${d.y},${d.x})`);

    // styled circles: white fill, colored stroke, subtle shadow
    node.append("circle")
        .attr("r", 10)
        .attr("fill", "#ffffff")
        .attr("stroke", "#2B7AE4")
        .attr("stroke-width", 2)
        .attr("filter", "url(#dt-drop-shadow)");

    // node labels: darker, slightly larger, bold
    node.append("text")
        .text((d) => d.data.name)
        .attr("dy", "0.31em")
        .attr("x", (d) => (d.children ? -18 : 18))
        .attr("text-anchor", (d) => (d.children ? "end" : "start"))
        .attr("fill", "#16324F")
        .style("font-weight", 600)
        .style("font-size", "12px");

    // === 更美观的边标签（带浅色背景） ===
    const edgeGroups = g
        .append("g")
        .attr("class", "edge-labels")
        .selectAll("g")
        .data(root.links())
        .join("g")
        .attr(
            "transform",
            (d) =>
                `translate(${(d.source.y + d.target.y) / 2},${(d.source.x + d.target.x) / 2})`,
        );

    // approximate label width using text length (simple but effective)
    edgeGroups
        .append("rect")
        .attr("x", (d) => {
            const txt = d.target.data.linkData
                ? d.target.data.linkData.edgeLabel
                : "";
            const w = Math.max(40, txt.length * 7);
            return -w / 2;
        })
        .attr("y", -14)
        .attr("rx", 6)
        .attr("ry", 6)
        .attr("width", (d) => {
            const txt = d.target.data.linkData
                ? d.target.data.linkData.edgeLabel
                : "";
            return Math.max(40, txt.length * 7);
        })
        .attr("height", 22)
        .attr("fill", "#f0f6ff")
        .attr("stroke", "#d6e9ff")
        .attr("opacity", 0.95);

    edgeGroups
        .append("text")
        .attr("class", "edge-label")
        .attr("x", 0)
        .attr("y", 0)
        .attr("dy", "-1px")
        .attr("text-anchor", "middle")
        .text((d) =>
            d.target.data.linkData ? d.target.data.linkData.edgeLabel : "",
        )
        .attr("fill", "#2C5366")
        .style("font-size", "11px")
        .style("font-weight", 500);

    // === 边标签结束 ===

    const zoom = d3
        .zoom()
        .scaleExtent([0.2, 5])
        .on("zoom", (event) => g.attr("transform", event.transform));
    const initialTransform = d3.zoomIdentity.translate(margin.left, margin.top);
    svg.call(zoom).call(zoom.transform, initialTransform);
    g.attr("transform", initialTransform.toString());
}

// 当 Preview 弹窗打开时调用：把当前 nodes 转成决策树数据并渲染
function onPreviewOpen() {
    const decisionTreeData = nodes.value.map((node) => ({
        name: node.name,
        branches: (node.branches || []).map((b) => ({
            label: b.name,
            next: b.target,
            value: b.value,
            probability: b.probability,
        })),
    }));

    const edges = convertDecisionTreeData(decisionTreeData);

    const containerEl = document.getElementById("preview-graph");
    if (containerEl) containerEl.innerHTML = "";

    renderTreeWithLabels(edges, "preview-graph");
}
const riskProfileLoading = ref(false);
const riskProfileResult = ref(null);

// 收益函数类型选择
const selectedPayoffFunctionType = ref("default");

// 收益函数配置
const payoffConfig = reactive({
    method: "ev", // ev, ce, eu
    utility_fn: "None", // None, exp, log
    risk_tolerance: 0.1,
});

// 敏感性分析表单数据
const sensitivityAnalysisForm = reactive({
    varname: "",
});

// Risk Profile表单数据
const riskProfileForm = reactive({
    idx: 0,
    cumulative: false,
    single: true,
});

// 新节点数据
const newNode = reactive({
    name: "",
    type: "decision",
    maximize: true,
    branches: [],
    payoffFn: "",
});

// 编辑节点数据
const editingNode = reactive({
    name: "",
    type: "decision",
    maximize: true,
    branches: [],
    payoffFn: "",
});

// 初始化新节点
const initNewNode = () => {
    newNode.name = "";
    newNode.type = "decision";
    newNode.maximize = true;
    newNode.branches = [];
    newNode.payoffFn = "";
};

// 添加分支
const addBranch = () => {
    if (newNode.type === "decision") {
        newNode.branches.push({
            name: "",
            value: "",
            target: DEFAULT_END_NODE,
        });
    } else if (newNode.type === "chance") {
        newNode.branches.push({
            name: "",
            probability: "",
            value: "",
            target: DEFAULT_END_NODE,
        });
    }
};

// 移除分支
const removeBranch = (index) => {
    newNode.branches.splice(index, 1);
};

// 添加编辑分支
const addEditBranch = () => {
    if (editingNode.type === "decision") {
        editingNode.branches.push({
            name: "",
            value: "",
            target: DEFAULT_END_NODE,
        });
    } else if (editingNode.type === "chance") {
        editingNode.branches.push({
            name: "",
            probability: "",
            value: "",
            target: DEFAULT_END_NODE,
        });
    }
};

// 移除编辑分支
const removeEditBranch = (index) => {
    editingNode.branches.splice(index, 1);
};

// 创建节点
const createNode = () => {
    if (!newNode.name) {
        ElMessage.error(t("home.enterNodeName"));
        return;
    }

    if (nodes.value.find((n) => n.name === newNode.name)) {
        ElMessage.error(t("home.nodeNameExists"));
        return;
    }

    // 处理分支目标节点，如果为空则设置为默认结束节点
    const processedBranches = newNode.branches.map((branch) => ({
        ...branch,
        target: branch.target || DEFAULT_END_NODE,
    }));

    const node = {
        name: newNode.name,
        type: newNode.type,
        maximize: newNode.maximize,
        branches: processedBranches,
        payoffFn: newNode.payoffFn,
    };

    nodes.value.push(node);

    // 确保默认结束节点存在（在添加节点后检查）
    ensureDefaultEndNode();

    showCreateNodeDialog.value = false;
    initNewNode();
    ElMessage.success(t("home.nodeCreatedSuccessfully"));
};

// 编辑节点
const editNode = (node) => {
    const index = nodes.value.findIndex((n) => n.name === node.name);
    if (index !== -1) {
        editingNodeIndex.value = index;
        Object.assign(editingNode, JSON.parse(JSON.stringify(node)));
        showEditNodeDialog.value = true;
    }
};

// 保存节点编辑
const saveNodeEdit = () => {
    if (!editingNode.name) {
        ElMessage.error(t("home.enterNodeName"));
        return;
    }

    const existingNode = nodes.value.find(
        (n, i) => n.name === editingNode.name && i !== editingNodeIndex.value,
    );
    if (existingNode) {
        ElMessage.error(t("home.nodeNameExists"));
        return;
    }

    // 处理分支目标节点，如果为空则设置为默认结束节点
    const processedBranches = editingNode.branches.map((branch) => ({
        ...branch,
        target: branch.target || DEFAULT_END_NODE,
    }));

    nodes.value[editingNodeIndex.value] = {
        ...editingNode,
        branches: processedBranches,
    };

    // 确保默认结束节点存在（在更新节点后检查）
    ensureDefaultEndNode();
    showEditNodeDialog.value = false;
    ElMessage.success(t("home.nodeEditedSuccessfully"));
};

// 删除节点
const deleteNode = (node) => {
    ElMessageBox.confirm(t("home.confirmDeleteNode"), t("home.prompt"), {
        confirmButtonText: t("home.confirm"),
        cancelButtonText: t("home.cancel"),
        type: "warning",
    }).then(() => {
        const index = nodes.value.findIndex((n) => n.name === node.name);
        if (index !== -1) {
            nodes.value.splice(index, 1);
            ElMessage.success(t("home.nodeDeletedSuccessfully"));
        }
    });
};

// 获取节点类型颜色
const getNodeTypeColor = (type) => {
    const colors = {
        decision: "primary",
        chance: "success",
        terminal: "warning",
    };
    return colors[type] || "info";
};

// 获取节点类型名称
const getNodeTypeName = (type) => {
    const names = {
        decision: t("home.decisionNodeType"),
        chance: t("home.chanceNodeType"),
        terminal: t("home.terminalNodeType"),
    };
    return names[type] || type;
};

// 可视化决策树
const visualizeTree = () => {
    if (nodes.value.length === 0) {
        ElMessage.warning(t("home.pleaseCreateNodesFirst"));
        return;
    }

    // 清除现有可视化
    const container = document.getElementById("tree-container");
    container.innerHTML = "";

    // 构建ECharts树形数据
    const treeData = buildEChartsTreeData();

    // 创建ECharts实例
    const chart = echarts.init(container);

    // 配置选项
    const option = {
        tooltip: {
            trigger: "item",
            backgroundColor: "rgba(255, 255, 255, 0.9)",
            borderColor: "#ccc",
            borderWidth: 1,
            textStyle: {
                color: "#333",
            },
            formatter: function (params) {
                if (params.data.type === "node") {
                    let tooltip = `<div style="font-weight: bold; margin-bottom: 5px;">${params.data.name}</div>`;
                    tooltip += `<div style="color: #666;">${t("home.typeLabel")}${getNodeTypeName(params.data.nodeType)}</div>`;
                    if (params.data.branchInfo) {
                        tooltip += `<div style="color: #666; margin-top: 3px;">${t("home.attributesLabel")}${params.data.branchInfo}</div>`;
                    }
                    return tooltip;
                }
                return params.data.name;
            },
        },
        series: [
            {
                type: "tree",
                data: [treeData],
                top: "8%",
                left: "10%",
                bottom: "5%",
                right: "25%",
                symbolSize: function (value, params) {
                    // 根据节点类型设置不同大小
                    const nodeType = params.data.nodeType;
                    if (nodeType === "decision") return 20;
                    if (nodeType === "chance") return 18;
                    if (nodeType === "terminal") return 16;
                    return 16;
                },
                orient: "vertical",
                label: {
                    position: "left",
                    verticalAlign: "middle",
                    align: "right",
                    fontSize: 11,
                    lineHeight: 16,
                    padding: [4, 8],
                    backgroundColor: "rgba(255, 255, 255, 0.8)",
                    borderRadius: 4,
                    formatter: function (params) {
                        // 如果是分支节点，显示分支信息
                        if (params.data.branchInfo) {
                            return `${params.data.name}\n${params.data.branchInfo}`;
                        }
                        return params.data.name;
                    },
                },
                leaves: {
                    label: {
                        position: "right",
                        verticalAlign: "middle",
                        align: "left",
                        fontSize: 11,
                        lineHeight: 16,
                        padding: [4, 8],
                        backgroundColor: "rgba(255, 255, 255, 0.8)",
                        borderRadius: 4,
                    },
                },
                emphasis: {
                    focus: "descendant",
                    itemStyle: {
                        shadowBlur: 10,
                        shadowColor: "rgba(0, 0, 0, 0.3)",
                    },
                },
                expandAndCollapse: true,
                animationDuration: 550,
                animationDurationUpdate: 750,
                initialTreeDepth: -1,
                lineStyle: {
                    color: "#999",
                    width: 2,
                    curveness: 0.1,
                },
                itemStyle: {
                    color: function (params) {
                        return getNodeColor(params.data.nodeType);
                    },
                    borderColor: "#333",
                    borderWidth: 2,
                    borderRadius: function (params) {
                        // 根据节点类型设置不同圆角
                        const nodeType = params.data.nodeType;
                        if (nodeType === "decision") return 8;
                        if (nodeType === "chance") return 6;
                        if (nodeType === "terminal") return 4;
                        return 4;
                    },
                },
            },
        ],
    };

    // 设置配置并渲染
    chart.setOption(option);

    // 监听窗口大小变化
    window.addEventListener("resize", () => {
        chart.resize();
    });

    ElMessage.success(t("home.visualizationGeneratedSuccessfully"));
};

// 构建ECharts树形数据
const buildEChartsTreeData = () => {
    const nodeMap = new Map();
    const allNodes = new Set();

    // 收集所有节点名称（包括目标节点）
    nodes.value.forEach((node) => {
        allNodes.add(node.name);
        if (node.branches) {
            node.branches.forEach((branch) => {
                if (branch.target) {
                    allNodes.add(branch.target);
                }
            });
        }
    });

    // 创建所有节点的映射
    allNodes.forEach((nodeName) => {
        const existingNode = nodes.value.find((n) => n.name === nodeName);
        if (existingNode) {
            nodeMap.set(nodeName, {
                name: nodeName,
                type: "node",
                nodeType: existingNode.type,
                children: [],
                branches: existingNode.branches,
            });
        } else {
            // 自动创建缺失的目标节点
            nodeMap.set(nodeName, {
                name: nodeName,
                type: "node",
                nodeType: "terminal", // 默认为结束节点
                children: [],
                branches: [],
            });
        }
    });

    // 构建连接关系
    nodes.value.forEach((node) => {
        if (node.branches) {
            node.branches.forEach((branch) => {
                if (branch.target) {
                    const targetNode = nodeMap.get(branch.target);
                    const sourceNode = nodeMap.get(node.name);
                    if (targetNode && sourceNode) {
                        // 创建分支标签
                        let label = branch.name;
                        let attributes = [];

                        if (
                            branch.value !== undefined &&
                            branch.value !== null &&
                            branch.value !== ""
                        ) {
                            attributes.push(
                                `${t("home.valueLabel")}${branch.value}`,
                            );
                        }
                        if (
                            branch.probability !== undefined &&
                            branch.probability !== null &&
                            branch.probability !== ""
                        ) {
                            const prob = parseFloat(branch.probability);
                            if (!isNaN(prob)) {
                                attributes.push(
                                    `${t("home.probabilityLabel")}${(prob * 100).toFixed(1)}%`,
                                );
                            }
                        }

                        const childNode = {
                            ...targetNode,
                            name: `${label} → ${targetNode.name}`,
                            branchInfo: attributes.join(", "),
                        };

                        sourceNode.children.push(childNode);
                    }
                }
            });
        }
    });

    // 找到根节点（没有父节点的节点）
    const childNodes = new Set();
    nodes.value.forEach((node) => {
        if (node.branches) {
            node.branches.forEach((branch) => {
                if (branch.target) {
                    childNodes.add(branch.target);
                }
            });
        }
    });

    // 找到根节点
    const rootNodes = [];
    nodes.value.forEach((node) => {
        if (!childNodes.has(node.name)) {
            const rootNode = nodeMap.get(node.name);
            if (rootNode) {
                rootNodes.push(rootNode);
            }
        }
    });

    // 如果没有找到根节点，使用第一个节点作为根节点
    if (rootNodes.length === 0 && nodes.value.length > 0) {
        const firstNode = nodeMap.get(nodes.value[0].name);
        if (firstNode) {
            rootNodes.push(firstNode);
        }
    }

    return (
        rootNodes[0] || {
            name: "root",
            type: "node",
            nodeType: "terminal",
            children: [],
        }
    );
};

// 获取节点颜色
const getNodeColor = (type) => {
    const colors = {
        decision: "#1890FF", // 更深的蓝色
        chance: "#52C41A", // 更深的绿色
        terminal: "#FA8C16", // 更深的橙色
    };
    return colors[type] || "#8C8C8C";
};

// 清除可视化
const clearVisualization = () => {
    const container = document.getElementById("tree-container");
    container.innerHTML = "";
    ElMessage.success(t("home.visualizationCleared"));
};

// 加载示例
const loadExample = () => {
    nodes.value = [
        {
            name: "bid",
            type: "decision",
            maximize: true,
            branches: [
                { name: "low", value: "300", target: "competitor_bid" },
                { name: "medium", value: "500", target: "competitor_bid" },
                { name: "high", value: "700", target: "competitor_bid" },
                { name: "no-bid", value: "0", target: "profit" },
            ],
        },
        {
            name: "competitor_bid",
            type: "chance",
            branches: [
                {
                    name: "low",
                    probability: "0.35",
                    value: "400",
                    target: "cost",
                },
                {
                    name: "medium",
                    probability: "0.50",
                    value: "600",
                    target: "cost",
                },
                {
                    name: "high",
                    probability: "0.15",
                    value: "800",
                    target: "cost",
                },
            ],
        },
        {
            name: "cost",
            type: "chance",
            branches: [
                {
                    name: "low",
                    probability: "0.25",
                    value: "200",
                    target: "profit",
                },
                {
                    name: "medium",
                    probability: "0.50",
                    value: "400",
                    target: "profit",
                },
                {
                    name: "high",
                    probability: "0.25",
                    value: "600",
                    target: "profit",
                },
            ],
        },
        {
            name: "profit",
            type: "terminal",
            payoffFn: "payoff_fn",
        },
    ];

    // 确保默认结束节点存在
    ensureDefaultEndNode();

    ElMessage.success(t("home.exampleDataLoadedSuccessfully"));
};

const loadExample2 = () => {
    nodes.value = [
        {
            name: "start",
            type: "decision",
            branches: [
                {
                    name: "yes",
                    target: "market",
                    value: "-4000",
                },
                {
                    name: "no",
                    target: "DEFAULT_END",
                    value: "0",
                },
            ],
        },
        {
            name: "market",
            type: "chance",
            branches: [
                {
                    name: "yes",
                    target: "sale",
                    value: "-2000",
                    probability: "0.8",
                },
                {
                    name: "no",
                    target: "DEFAULT_END",
                    value: "0",
                    probability: "0.2",
                },
            ],
        },
        {
            name: "sale",
            type: "chance",
            branches: [
                {
                    name: "great",
                    target: "DEFAULT_END",
                    value: "10800",
                    probability: "0.45",
                },
                {
                    name: "fair",
                    target: "DEFAULT_END",
                    value: "5400",
                    probability: "0.35",
                },
                {
                    name: "awful",
                    target: "DEFAULT_END",
                    value: "1620",
                    probability: "0.2",
                },
            ],
        },
    ];

    // 设置自定义收益函数
    payoffFunction.value = `def payoff_fn(values, probabilities, branches):
    value_keys = values.keys()
    prob_keys = probabilities.keys()
    not_in_prob_keys = [key for key in value_keys if key not in prob_keys]
    outcome = sum([ values[key] for key in not_in_prob_keys ])
    for key in prob_keys:
        outcome += values[key] #* probabilities[key]
    return outcome`;

    // 确保默认结束节点存在
    ensureDefaultEndNode();

    ElMessage.success("示例二数据加载成功");
};

// 导出数据
const exportData = () => {
    if (nodes.value.length === 0) {
        ElMessage.warning(t("home.noDataToExport"));
        return;
    }

    // 转换数据格式
    const exportNodes = nodes.value.map((node) => {
        // 确保branches存在且是数组
        const branches =
            node.branches && Array.isArray(node.branches)
                ? node.branches.map((branch) => {
                      const exportBranch = {
                          label: branch.name || "",
                          next: branch.target || "",
                      };

                      // 添加值（如果存在）
                      if (
                          branch.value !== undefined &&
                          branch.value !== null &&
                          branch.value !== ""
                      ) {
                          exportBranch.value =
                              parseFloat(branch.value) || branch.value;
                      }

                      // 添加概率（如果存在）
                      if (
                          branch.probability !== undefined &&
                          branch.probability !== null &&
                          branch.probability !== ""
                      ) {
                          exportBranch.probability =
                              parseFloat(branch.probability) ||
                              branch.probability;
                      }

                      return exportBranch;
                  })
                : [];

        return {
            name: node.name || "",
            type: node.type || "terminal",
            branches: branches,
        };
    });

    // 创建导出数据对象
    const exportDataObj = {
        nodes: exportNodes,
        payoff_function: payoffFunction.value,
    };

    // 转换为JSON字符串
    const jsonString = JSON.stringify(exportDataObj, null, 2);

    // 创建Blob对象
    const blob = new Blob([jsonString], { type: "application/json" });

    // 创建下载链接
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "decision_tree_data.json";

    // 触发下载
    document.body.appendChild(link);
    link.click();

    // 清理
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    ElMessage.success(t("home.dataExportedSuccessfully"));
};

// 导入数据
const importData = () => {
    // 创建文件输入元素
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".json";

    input.onchange = (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const data = JSON.parse(e.target.result);

                if (!data.nodes || !Array.isArray(data.nodes)) {
                    ElMessage.error(t("home.incorrectFileFormat"));
                    return;
                }

                // 转换导入的数据格式
                const importedNodes = data.nodes.map((node) => {
                    // 确保branches存在且是数组
                    const branches =
                        node.branches && Array.isArray(node.branches)
                            ? node.branches.map((branch) => {
                                  const importBranch = {
                                      name: branch.label || "",
                                      target: branch.next || "",
                                  };

                                  // 添加值（如果存在）
                                  if (branch.value !== undefined) {
                                      importBranch.value =
                                          branch.value.toString();
                                  }

                                  // 添加概率（如果存在）
                                  if (branch.probability !== undefined) {
                                      importBranch.probability =
                                          branch.probability.toString();
                                  }

                                  return importBranch;
                              })
                            : [];

                    return {
                        name: node.name || "",
                        type: node.type || "terminal",
                        maximize: node.type === "decision" ? true : undefined,
                        branches: branches,
                        payoffFn: node.type === "terminal" ? "payoff_fn" : "",
                    };
                });

                // 更新节点数据
                nodes.value = importedNodes;

                // 确保默认结束节点存在
                ensureDefaultEndNode();

                // 导入payoff函数（如果存在）
                if (data.payoff_function) {
                    payoffFunction.value = data.payoff_function;
                }

                ElMessage.success(t("home.dataImportedSuccessfully"));
            } catch (error) {
                ElMessage.error(
                    `${t("home.fileParsingFailed")}${error.message}`,
                );
            }
        };

        reader.readAsText(file);
    };

    input.click();
};

// 生成决策树
const generateTree = async () => {
    if (nodes.value.length === 0) {
        ElMessage.warning(t("home.pleaseCreateNodesFirst"));
        return;
    }

    if (!payoffFunction.value.trim()) {
        ElMessage.warning(t("home.pleaseConfigurePayoffFunction"));
        return;
    }

    try {
        // 准备请求数据
        const sortedNodes = [...nodes.value].sort((a, b) => {
            // 将 DEFAULT_END 节点排在最后
            if (a.name === DEFAULT_END_NODE) return 1;
            if (b.name === DEFAULT_END_NODE) return -1;
            return 0;
        });

        const requestData = {
            json_data: {
                nodes: sortedNodes.map((node) => {
                    const branches =
                        node.branches && Array.isArray(node.branches)
                            ? node.branches.map((branch) => {
                                  const exportBranch = {
                                      label: branch.name || "",
                                      next: branch.target || "",
                                  };

                                  if (
                                      branch.value !== undefined &&
                                      branch.value !== null &&
                                      branch.value !== ""
                                  ) {
                                      exportBranch.value =
                                          parseFloat(branch.value) ||
                                          branch.value;
                                  }

                                  if (
                                      branch.probability !== undefined &&
                                      branch.probability !== null &&
                                      branch.probability !== ""
                                  ) {
                                      exportBranch.probability =
                                          parseFloat(branch.probability) ||
                                          branch.probability;
                                  }

                                  return exportBranch;
                              })
                            : [];

                    return {
                        name: node.name || "",
                        type: node.type || "terminal",
                        branches: branches,
                    };
                }),
            },
            payoff_fn_code: payoffFunction.value,
            payoff_config: {
                method: payoffConfig.method,
                utility_fn: payoffConfig.utility_fn,
                risk_tolerance: payoffConfig.risk_tolerance,
            },
        };

        ElMessage.info(t("home.generatingDecisionTree"));

        // 调用API
        const response = await axios.post(
            "http://localhost:8000/api/generate-tree",
            requestData,
            {
                headers: {
                    "Content-Type": "application/json",
                },
            },
        );

        if (
            response.data &&
            response.data.success &&
            response.data.dot_content
        ) {
            // 渲染dot文件
            renderDotGraph(response.data.dot_content);
            ElMessage.success(t("home.decisionTreeGeneratedSuccessfully"));
        } else {
            const errorMessage =
                response.data?.message || t("home.apiErrorFormat");
            ElMessage.error(errorMessage);
        }
    } catch (error) {
        console.error(t("home.decisionTreeGenerationFailed"), error);
        ElMessage.error(
            `${t("home.decisionTreeGenerationFailed")} ${error.response?.data?.detail || error.message}`,
        );
    }
};

// 渲染dot图
const renderDotGraph = async (dotContent) => {
    try {
        // 动态加载d3和d3-graphviz
        const d3 = await import("d3");
        const d3Graphviz = await import("d3-graphviz");

        // 清除容器
        const container = document.getElementById("tree-container");
        container.innerHTML = "";

        // 创建graphviz渲染器
        const graphviz = d3Graphviz
            .graphviz(container)
            .width(container.clientWidth)
            .height(container.clientHeight)
            .fit(true)
            .zoom(zoomEnabled.value)
            .attributer(function (d) {
                // 为节点添加交互样式
                if (d.tag === "ellipse" || d.tag === "polygon") {
                    d3.select(this)
                        .style("cursor", "pointer")
                        .style("stroke-width", "2")
                        .on("mouseover", function () {
                            d3.select(this)
                                .style("stroke-width", "3")
                                .style("stroke", "#409eff")
                                .style("opacity", "0.8");
                        })
                        .on("mouseout", function () {
                            d3.select(this)
                                .style("stroke-width", "2")
                                .style("stroke", "#333")
                                .style("opacity", "1");
                        })
                        .on("click", function () {
                            // 点击节点时显示信息
                            const nodeName = d3
                                .select(this.parentNode)
                                .select("text")
                                .text();
                            if (nodeName) {
                                ElMessage.info(
                                    `${t("home.clickedNode")}${nodeName}`,
                                );
                            }
                        });
                }

                // 为边添加交互样式
                if (d.tag === "path" && d.class === "edge") {
                    d3.select(this)
                        .style("cursor", "pointer")
                        .style("stroke-width", "2")
                        .on("mouseover", function () {
                            d3.select(this)
                                .style("stroke-width", "3")
                                .style("stroke", "#409eff")
                                .style("opacity", "0.8");
                        })
                        .on("mouseout", function () {
                            d3.select(this)
                                .style("stroke-width", "2")
                                .style("stroke", "#333")
                                .style("opacity", "1");
                        })
                        .on("click", function () {
                            // 点击边时显示信息
                            const edgeLabel = d3
                                .select(this.parentNode)
                                .select("text")
                                .text();
                            if (edgeLabel) {
                                ElMessage.info(
                                    `${t("home.clickedEdge")}${edgeLabel}`,
                                );
                            }
                        });
                }

                // 为文本添加交互样式
                if (d.tag === "text") {
                    d3.select(this)
                        .style("cursor", "pointer")
                        .style("font-weight", "normal")
                        .on("mouseover", function () {
                            d3.select(this)
                                .style("font-weight", "bold")
                                .style("fill", "#409eff");
                        })
                        .on("mouseout", function () {
                            d3.select(this)
                                .style("font-weight", "normal")
                                .style("fill", "#333");
                        });
                }
            });

        // 渲染dot内容
        await graphviz.renderDot(dotContent);

        // 保存graphviz实例
        currentGraphviz.value = graphviz;
        hasGraphviz.value = true;

        ElMessage.success(t("home.decisionTreeRenderedSuccessfully"));
    } catch (error) {
        console.error(t("home.decisionTreeRenderingFailed"), error);
        ElMessage.error(
            `${t("home.decisionTreeRenderingFailed")} ${error.message}`,
        );
    }
};

// 默认payoff函数
const defaultPayoffFunction = `def payoff_fn(values, probabilities, branches):
    value_keys = values.keys()
    prob_keys = probabilities.keys()
    not_in_prob_keys = [key for key in value_keys if key not in prob_keys]
    outcome = sum([ values[key] for key in not_in_prob_keys ])
    for key in prob_keys:
        outcome += values[key] #* probabilities[key]
    return outcome`;

// 默认的收益函数模板
const payoffFunctionTemplates = {
    default: `def payoff_fn(values, probabilities, branches):
    value_keys = values.keys()
    prob_keys = probabilities.keys()
    not_in_prob_keys = [key for key in value_keys if key not in prob_keys]
    outcome = sum([ values[key] for key in not_in_prob_keys ])
    for key in prob_keys:
        outcome += values[key] #* probabilities[key]
    return outcome`,
};

// 收益函数类型改变处理
const onPayoffFunctionTypeChange = (type) => {
    payoffFunction.value = payoffFunctionTemplates[type];
};

// 保存payoff函数
const savePayoffFunction = () => {
    if (!payoffFunction.value.trim()) {
        ElMessage.warning(t("home.pleaseEnterPayoffFunction"));
        return;
    }

    // 这里可以添加函数语法验证
    try {
        // 简单的语法检查：确保包含def关键字
        if (!payoffFunction.value.includes("def ")) {
            throw new Error(t("home.functionMustStartWithDef"));
        }

        ElMessage.success(t("home.payoffFunctionSavedSuccessfully"));
    } catch (error) {
        ElMessage.error(`${t("home.fileParsingFailed")}${error.message}`);
    }
};

// 重置为默认函数
const resetPayoffFunction = () => {
    payoffFunction.value = payoffFunctionTemplates.default;
    ElMessage.success(t("home.resetToDefaultFunction"));
};

// 交互控制函数
const resetZoom = () => {
    if (currentGraphviz.value) {
        currentGraphviz.value.resetZoom();
        ElMessage.success(t("home.zoomReset"));
    }
};

const fitGraph = () => {
    if (currentGraphviz.value) {
        currentGraphviz.value.fit();
        ElMessage.success(t("home.graphFittedToWindow"));
    }
};

const toggleZoom = () => {
    if (currentGraphviz.value) {
        zoomEnabled.value = !zoomEnabled.value;
        if (zoomEnabled.value) {
            currentGraphviz.value.zoom(true);
        } else {
            currentGraphviz.value.zoom(false);
        }
        ElMessage.success(
            zoomEnabled.value ? t("home.zoomEnabled") : t("home.zoomDisabled"),
        );
    }
};

// 执行敏感性分析
const performSensitivityAnalysis = async () => {
    if (!sensitivityAnalysisForm.varname.trim()) {
        ElMessage.warning(t("home.pleaseEnterVariableName"));
        return;
    }

    if (nodes.value.length === 0) {
        ElMessage.warning(t("home.pleaseCreateNodesFirst"));
        return;
    }

    if (!payoffFunction.value.trim()) {
        ElMessage.warning(t("home.pleaseConfigurePayoffFunction"));
        return;
    }

    try {
        sensitivityAnalysisLoading.value = true;

        // 准备请求数据
        const sortedNodes = [...nodes.value].sort((a, b) => {
            // 将 DEFAULT_END 节点排在最后
            if (a.name === DEFAULT_END_NODE) return 1;
            if (b.name === DEFAULT_END_NODE) return -1;
            return 0;
        });

        const requestData = {
            json_data: {
                nodes: sortedNodes.map((node) => {
                    const branches =
                        node.branches && Array.isArray(node.branches)
                            ? node.branches.map((branch) => {
                                  const exportBranch = {
                                      label: branch.name || "",
                                      next: branch.target || "",
                                  };

                                  if (
                                      branch.value !== undefined &&
                                      branch.value !== null &&
                                      branch.value !== ""
                                  ) {
                                      exportBranch.value =
                                          parseFloat(branch.value) ||
                                          branch.value;
                                  }

                                  if (
                                      branch.probability !== undefined &&
                                      branch.probability !== null &&
                                      branch.probability !== ""
                                  ) {
                                      exportBranch.probability =
                                          parseFloat(branch.probability) ||
                                          branch.probability;
                                  }

                                  return exportBranch;
                              })
                            : [];

                    return {
                        name: node.name || "",
                        type: node.type || "terminal",
                        branches: branches,
                    };
                }),
            },
            payoff_fn_code: payoffFunction.value,
            varname: sensitivityAnalysisForm.varname.trim(),
        };

        ElMessage.info(t("home.performingSensitivityAnalysis"));

        // 调用后端API
        const response = await axios.post(
            "http://localhost:8000/api/sensitivity-analysis",
            requestData,
            {
                headers: {
                    "Content-Type": "application/json",
                },
            },
        );

        if (response.data && response.data.success) {
            // 处理返回的分析结果
            sensitivityAnalysisResult.value = {
                varname: sensitivityAnalysisForm.varname.trim(),
                node_type: response.data.node_type,
                file_url: response.data.file_url,
            };
            ElMessage.success(t("home.sensitivityAnalysisCompleted"));
            console.log("Sensitivity Analysis Result:", response.data);

            // 不关闭对话框，让用户查看结果
            // showSensitivityAnalysisDialog.value = false
            // 重置表单
            sensitivityAnalysisForm.varname = "";
        } else {
            const errorMessage =
                response.data?.message || t("home.apiErrorFormat");
            ElMessage.error(errorMessage);
        }
    } catch (error) {
        console.error(t("home.sensitivityAnalysisFailed"), error);
        ElMessage.error(
            `${t("home.sensitivityAnalysisFailed")} ${error.response?.data?.detail || error.message}`,
        );
    } finally {
        sensitivityAnalysisLoading.value = false;
    }
};

// 下载敏感性分析图
const downloadSensitivityImage = () => {
    if (
        sensitivityAnalysisResult.value &&
        sensitivityAnalysisResult.value.file_url
    ) {
        const link = document.createElement("a");
        link.href = sensitivityAnalysisResult.value.file_url;
        link.download = `${sensitivityAnalysisResult.value.varname}_sensitivity_analysis.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        ElMessage.success(t("home.chartDownloadedSuccessfully"));
    } else {
        ElMessage.warning(t("home.noChartToDownload"));
    }
};

// 清除敏感性分析结果
const clearSensitivityResults = () => {
    sensitivityAnalysisResult.value = null;
    ElMessage.success(t("home.sensitivityResultsCleared"));
};

// 处理图片加载错误
const handleImageError = (event) => {
    event.target.src = "https://via.placeholder.com/150"; // 替换为默认图片
    event.target.alt = t("home.imageLoadError");
};

// 执行Risk Profile分析
const performRiskProfileAnalysis = async () => {
    if (nodes.value.length === 0) {
        ElMessage.warning(t("home.pleaseCreateNodesFirst"));
        return;
    }

    if (!payoffFunction.value.trim()) {
        ElMessage.warning(t("home.pleaseConfigurePayoffFunction"));
        return;
    }

    if (riskProfileForm.idx < 0 || riskProfileForm.idx >= nodes.value.length) {
        ElMessage.warning(t("home.invalidNodeIndex"));
        return;
    }

    try {
        riskProfileLoading.value = true;

        // 准备请求数据
        const sortedNodes = [...nodes.value].sort((a, b) => {
            // 将 DEFAULT_END 节点排在最后
            if (a.name === DEFAULT_END_NODE) return 1;
            if (b.name === DEFAULT_END_NODE) return -1;
            return 0;
        });

        const requestData = {
            json_data: {
                nodes: sortedNodes.map((node) => {
                    const branches =
                        node.branches && Array.isArray(node.branches)
                            ? node.branches.map((branch) => {
                                  const exportBranch = {
                                      label: branch.name || "",
                                      next: branch.target || "",
                                  };

                                  if (
                                      branch.value !== undefined &&
                                      branch.value !== null &&
                                      branch.value !== ""
                                  ) {
                                      exportBranch.value =
                                          parseFloat(branch.value) ||
                                          branch.value;
                                  }

                                  if (
                                      branch.probability !== undefined &&
                                      branch.probability !== null &&
                                      branch.probability !== ""
                                  ) {
                                      exportBranch.probability =
                                          parseFloat(branch.probability) ||
                                          branch.probability;
                                  }

                                  return exportBranch;
                              })
                            : [];

                    return {
                        name: node.name || "",
                        type: node.type || "terminal",
                        branches: branches,
                    };
                }),
            },
            payoff_fn_code: payoffFunction.value,
            idx: riskProfileForm.idx,
            cumulative: riskProfileForm.cumulative,
            single: riskProfileForm.single,
        };

        ElMessage.info(t("home.generatingRiskProfile"));

        // 调用后端API
        const response = await axios.post(
            "http://localhost:8000/api/risk-profile",
            requestData,
            {
                headers: {
                    "Content-Type": "application/json",
                },
            },
        );

        if (response.data && response.data.success) {
            // 处理返回的分析结果
            riskProfileResult.value = {
                file_url: response.data.file_url,
            };
            ElMessage.success(t("home.riskProfileGeneratedSuccessfully"));
            console.log("Risk Profile Result:", response.data);
        } else {
            const errorMessage =
                response.data?.message || t("home.apiErrorFormat");
            ElMessage.error(errorMessage);
        }
    } catch (error) {
        console.error(t("home.riskProfileGenerationFailed"), error);
        ElMessage.error(
            `${t("home.riskProfileGenerationFailed")} ${error.response?.data?.detail || error.message}`,
        );
    } finally {
        riskProfileLoading.value = false;
    }
};

// 下载Risk Profile图片
const downloadRiskProfileImage = () => {
    if (riskProfileResult.value && riskProfileResult.value.file_url) {
        const link = document.createElement("a");
        link.href = riskProfileResult.value.file_url;
        link.download = `risk_profile_node_${riskProfileForm.idx}.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        ElMessage.success(t("home.chartDownloadedSuccessfully"));
    } else {
        ElMessage.warning(t("home.noChartToDownload"));
    }
};

// 清除Risk Profile结果
const clearRiskProfileResults = () => {
    riskProfileResult.value = null;
    ElMessage.success(t("home.riskProfileResultsCleared"));
};

// 组件挂载时初始化
onMounted(() => {
    initNewNode();
    // 设置默认的payoff函数
    payoffFunction.value = payoffFunctionTemplates.default;
});
</script>

<style scoped>
.decision-tree-container {
    height: 100vh;
    background-color: #f5f5f5;
}

.el-header {
    background-color: #fff;
    border-bottom: 1px solid #e4e7ed;
    display: flex;
    align-items: center;
    justify-content: center;
}

.el-header h1 {
    margin: 0;
    color: #303133;
}

.control-panel {
    height: calc(100vh - 120px);
    overflow-y: auto;
}

.visualization-area {
    height: calc(100vh - 120px);
}

.tree-container {
    height: calc(100vh - 200px);
    overflow: hidden;
    border: 1px solid #e4e7ed;
    border-radius: 8px;
    background-color: #fafafa;
    padding: 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-title {
    font-size: 16px;
    font-weight: 600;
    color: #303133;
}

.interaction-controls {
    display: flex;
    gap: 8px;
}

.interaction-controls .el-button {
    margin: 0;
}

.node-list {
    margin-bottom: 20px;
}

.node-list h3 {
    margin-bottom: 10px;
    color: #303133;
}

.branch-item {
    margin-bottom: 10px;
    padding: 15px;
    border: 1px solid #e4e7ed;
    border-radius: 6px;
    background-color: #fafafa;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.branch-item .el-input-number {
    width: 100%;
}

.branch-item .el-input-number .el-input__inner {
    text-align: center;
}

.branch-form {
    padding: 10px;
}

.branch-form .el-form-item {
    margin-bottom: 15px;
}

.branch-form .el-form-item:last-child {
    margin-bottom: 0;
}

.visualization-controls {
    border-top: 1px solid #e4e7ed;
    padding-top: 20px;
}

.visualization-controls .el-button {
    margin-right: 10px;
}

/* Preview graph styles for D3 rendering */
.edge-label {
    font-size: 11px;
    fill: #2c5366;
    pointer-events: none;
    font-weight: 500;
}
.link {
    fill: none;
    stroke: #6ea8fe;
    stroke-width: 2px;
    stroke-linecap: round;
    opacity: 0.95;
}

.payoff-config h4 {
    margin-bottom: 10px;
    color: #303133;
    font-size: 14px;
    font-weight: 600;
}

.payoff-config .el-textarea__inner {
    font-family: "Courier New", "Monaco", "Menlo", monospace;
    font-size: 12px;
    line-height: 1.4;
    background-color: #fafafa;
    border: 1px solid #e4e7ed;
}

.payoff-config .el-textarea__inner:focus {
    background-color: #fff;
    border-color: #409eff;
}

/* 收益函数类型选择器样式 */
.function-type-selector {
    margin-bottom: 15px;
}

.function-type-selector .el-select {
    width: 100%;
}

.function-type-selector .el-select .el-input__inner {
    border-radius: 6px;
    border: 1px solid #e4e7ed;
}

.function-type-selector .el-select:hover .el-input__inner {
    border-color: #409eff;
}

/* 头部样式优化 */
.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
    padding: 0 20px;
}

.main-title {
    margin: 0;
    color: #303133;
    font-size: 24px;
    font-weight: 600;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.header-controls {
    display: flex;
    align-items: center;
    gap: 15px;
}

.language-selector {
    width: 120px;
}

/* 卡片样式优化 */
.control-panel,
.visualization-area {
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
}

.control-panel:hover,
.visualization-area:hover {
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    transform: translateY(-2px);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 20px 15px 20px;
    border-bottom: 1px solid #f0f0f0;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 12px 12px 0 0;
}

.card-title {
    font-size: 18px;
    font-weight: 600;
    color: #303133;
    margin: 0;
}

/* 控制区域样式 */
.control-section {
    margin-bottom: 25px;
    padding: 20px;
    background: #fafbfc;
    border-radius: 8px;
    border: 1px solid #e4e7ed;
}

.control-section:last-child {
    margin-bottom: 0;
}

.section-title {
    margin: 0 0 15px 0;
    font-size: 16px;
    font-weight: 600;
    color: #303133;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-title::before {
    content: "";
    width: 4px;
    height: 16px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 2px;
}

.button-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.button-group .el-button {
    margin: 0;
    border-radius: 6px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.button-group .el-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 节点列表样式 */
.node-list {
    margin-bottom: 25px;
}

.node-list .el-table {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.node-list .el-table th {
    background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
    color: #606266;
    font-weight: 600;
}

/* 收益函数配置样式 */
.payoff-config {
    background: #fafbfc;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #e4e7ed;
}

.code-editor-container {
    margin-bottom: 15px;
}

.code-editor {
    font-family: "JetBrains Mono", "Fira Code", "Courier New", monospace;
    font-size: 13px;
    line-height: 1.6;
}

.code-editor .el-textarea__inner {
    background: #1e1e1e;
    color: #d4d4d4;
    border: 1px solid #3c3c3c;
    border-radius: 6px;
    padding: 15px;
    font-family: inherit;
    font-size: inherit;
    line-height: inherit;
}

.code-editor .el-textarea__inner:focus {
    background: #252526;
    border-color: #007acc;
    box-shadow: 0 0 0 2px rgba(0, 122, 204, 0.2);
}

.function-actions {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
}

/* 可视化控制样式 */
.interaction-controls {
    display: flex;
    gap: 8px;
}

.interaction-controls .el-button {
    margin: 0;
    border-radius: 6px;
    transition: all 0.3s ease;
}

.interaction-controls .el-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 树容器样式优化 */
.tree-container {
    height: calc(100vh - 200px);
    overflow: hidden;
    border: 1px solid #e4e7ed;
    border-radius: 8px;
    background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
    padding: 0;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* 响应式设计 */
@media (max-width: 1200px) {
    .el-col-8 {
        width: 100%;
        margin-bottom: 20px;
    }

    .el-col-16 {
        width: 100%;
    }

    .button-group {
        flex-direction: column;
    }

    .button-group .el-button {
        width: 100%;
    }
}

/* 动画效果 */
.el-card {
    animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* 滚动条美化 */
.control-panel::-webkit-scrollbar {
    width: 6px;
}

.control-panel::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
}

.control-panel::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
}

.control-panel::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
}
</style>
