import axios from 'axios'

// 使用当前页面的 origin 作为后端 API 基础地址（如果 window 不可用则回退到 localhost:8000）
const API_BASE_URL = (typeof window !== 'undefined' ? window.location.origin : 'http://localhost:8000') + '/api'

// 创建 axios 实例
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json'
    }
})

// 决策树分析 API
export const decisionTreeApi = {
    // 分析决策树
    async analyzeTree(treeData) {
        try {
            const response = await apiClient.post('/analyze', treeData)
            return response.data
        } catch (error) {
            console.error('分析决策树失败:', error)
            throw new Error(error.response?.data?.message || '分析失败')
        }
    },

    // 保存决策树
    async saveTree(treeData) {
        try {
            const response = await apiClient.post('/save', treeData)
            return response.data
        } catch (error) {
            console.error('保存决策树失败:', error)
            throw new Error(error.response?.data?.message || '保存失败')
        }
    },

    // 加载决策树
    async loadTree(treeId) {
        try {
            const response = await apiClient.get(`/load/${treeId}`)
            return response.data
        } catch (error) {
            console.error('加载决策树失败:', error)
            throw new Error(error.response?.data?.message || '加载失败')
        }
    },

    // 获取所有决策树列表
    async getTreeList() {
        try {
            const response = await apiClient.get('/trees')
            return response.data
        } catch (error) {
            console.error('获取决策树列表失败:', error)
            throw new Error(error.response?.data?.message || '获取列表失败')
        }
    }
}

// 数据转换工具
export const dataTransformers = {
    // 将前端节点数据转换为 smart_choice 格式
    toSmartChoiceFormat(nodes, edges) {
        const dataNodes = []
        const decisionTree = {
            nodes: [],
            edges: []
        }

        // 转换节点
        nodes.forEach(node => {
            const smartChoiceNode = {
                id: node.id,
                name: node.name,
                type: node.type,
                position: { x: node.x, y: node.y }
            }

            if (node.type === 'terminal') {
                smartChoiceNode.payoff = parseFloat(node.payoff) || 0
            } else {
                smartChoiceNode.branches = node.branches.map(branch => ({
                    name: branch.name,
                    value: branch.value,
                    probability: parseFloat(branch.probability) || 0,
                    targetNode: branch.targetNode
                }))
            }

            dataNodes.push(smartChoiceNode)
        })

        // 转换边
        edges.forEach(edge => {
            decisionTree.edges.push({
                source: edge.source,
                target: edge.target,
                label: edge.label
            })
        })

        return {
            dataNodes,
            decisionTree
        }
    },

    // 将 smart_choice 格式转换为前端格式
    fromSmartChoiceFormat(dataNodes, decisionTree) {
        const nodes = dataNodes.map(node => ({
            id: node.id,
            name: node.name,
            type: node.type,
            x: node.position?.x || 0,
            y: node.position?.y || 0,
            branches: node.branches || [],
            payoff: node.payoff?.toString() || ''
        }))

        const edges = decisionTree.edges.map(edge => ({
            source: edge.source,
            target: edge.target,
            label: edge.label
        }))

        return { nodes, edges }
    }
}

// 模拟分析结果（当后端不可用时使用）
export const mockAnalysis = (treeData) => {
    const { nodes } = treeData

    // 简单的期望值计算
    let expectedValue = 0
    const paths = []

    // 找到终止节点
    const terminalNodes = nodes.filter(node => node.type === 'terminal')

    terminalNodes.forEach(node => {
        const payoff = parseFloat(node.payoff) || 0
        expectedValue += payoff
        paths.push({
            path: [node.name],
            value: payoff,
            probability: 1 / terminalNodes.length
        })
    })

    return {
        expectedValue: expectedValue / terminalNodes.length,
        optimalPath: paths.reduce((max, path) =>
            path.value > max.value ? path : max
        ).path,
        allPaths: paths
    }
} 