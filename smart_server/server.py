from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx
import uvicorn
import os
from pathlib import Path
import mimetypes
from typing import Optional
import json
from pydantic import BaseModel
from matplotlib import pyplot as plt

from smart_choice.datanodes import DataNodes
from smart_choice.decisiontree import DecisionTree
from smart_choice.probabilistic_sensitivity import ProbabilisticSensitivity
from smart_choice.risk_profile import RiskProfile


class TreeRequest(BaseModel):
    json_data: dict
    payoff_fn_code: str
    payoff_config: dict


class SensitivityAnalysisRequest(BaseModel):
    json_data: dict
    payoff_fn_code: str
    varname: str


class RiskProfileRequest(BaseModel):
    json_data: dict
    payoff_fn_code: str
    idx: int = 0
    cumulative: bool = False
    single: bool = True


def json_to_datanodes(json_data, payoff_fn):
    nodes = DataNodes()
    for node in json_data["nodes"]:
        name = node["name"]
        node_type = node["type"]
        branches = node.get("branches", [])

        if node_type == "decision":
            # 决策节点
            branches_tuple = [
                (b["label"], float(b["value"]), b["next"]) for b in branches
            ]
            nodes.add_decision(name=name, branches=branches_tuple, maximize=True)

        elif node_type == "chance":
            # 概率节点
            branches_tuple = [
                (b["label"], float(b["probability"]), float(b["value"]), b["next"])
                for b in branches
            ]
            nodes.add_chance(name=name, branches=branches_tuple)

        elif node_type == "terminal":
            # 终点节点
            nodes.add_terminal(name=name, payoff_fn=payoff_fn)

        else:
            raise ValueError(f"Unsupported node type: {node_type}")

    return nodes


LINEFMTS = [
    "-k",
    "--k",
    ".-k",
    ":k",
    "-r",
    "--r",
    ".-r",
    ":r",
    "-g",
    "--g",
    ".-g",
    ":g",
]

COLORS = [
    "black",
    "red",
    "green",
    "blue",
    "orange",
    "purple",
    "brown",
    "pink",
    "gray",
    "olive",
    "cyan",
    "magenta",
]


def plot(self, filename):
    if isinstance(self.expected_values_, dict):
        for fmt, tag_branch in zip(LINEFMTS, self.expected_values_.keys()):
            plt.gca().plot(
                self.probabilities_,
                self.expected_values_[tag_branch],
                fmt,
                label=tag_branch,
            )
    else:
        plt.gca().plot(self.probabilities_, self.expected_values_, "-k")

    plt.gca().spines["bottom"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["top"].set_visible(False)
    plt.gca().set_ylabel("Expected values")
    plt.gca().set_xlabel("Probability")
    plt.legend()
    plt.grid()
    plt.savefig(f"{filename}.png")
    plt.close()


def plot_risk_profile(risk_profile_analyzer, filename):
    """Global function to plot and save risk profile"""

    def format_plot():
        plt.gca().spines["bottom"].set_visible(False)
        plt.gca().spines["left"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.gca().spines["top"].set_visible(False)

        plt.gca().set_xlabel("Expected values")
        plt.gca().set_ylabel("Probability")
        plt.gca().legend()
        plt.grid()

    def stem_plot():
        for i_key, key in enumerate(risk_profile_analyzer.df_.keys()):
            df_ = risk_profile_analyzer.df_[key]
            x_points = df_["Value"]
            y_points = df_["Probability"]
            markerline, _, _ = plt.gca().stem(
                x_points,
                y_points,
                linefmt=LINEFMTS[i_key % len(LINEFMTS)],
                basefmt="gray",
                label=key,
            )
            markerline.set_markerfacecolor(COLORS[i_key % len(COLORS)])
            markerline.set_markeredgecolor(COLORS[i_key % len(COLORS)])

        format_plot()

    def step_plot():
        for i_key, key in enumerate(risk_profile_analyzer.df_.keys()):
            df_ = risk_profile_analyzer.df_[key]
            x_points = df_["Value"].tolist()
            x_points += [x_points[-1]]
            y_points = [0] + df_["Cumulative Probability"].tolist()
            plt.gca().step(
                x_points,
                y_points,
                LINEFMTS[i_key % len(LINEFMTS)],
                label=key,
                alpha=0.8,
            )

        format_plot()

    if risk_profile_analyzer._cumulative is False:
        stem_plot()
    else:
        step_plot()

    plt.savefig(f"{filename}.png")
    plt.close()


class SmartServer:
    def __init__(self, static_dir: Optional[str] = None):
        """
        Initialize the SmartServer.

        Args:
            static_dir (str, optional): Path to the directory containing static files.
                                      If not provided, uses 'src/frontend/dist' relative to the package.
        """
        # Initialize MIME types
        mimetypes.add_type("application/javascript", ".js")
        mimetypes.add_type("application/javascript", ".mjs")
        mimetypes.add_type("text/css", ".css")
        mimetypes.add_type("text/html", ".html")

        self.app = FastAPI(title="Smart Server")

        # Set default static directory relative to this file if not provided
        if static_dir is None:
            # 尝试多个可能的路径
            possible_paths = [
                os.path.join(os.path.dirname(__file__), "src", "frontend", "dist"),
                os.path.join(os.path.dirname(__file__), "static"),
                "static",  # 当前工作目录下的 static
            ]

            for path in possible_paths:
                if os.path.exists(path):
                    static_dir = path
                    break
            else:
                # 如果都找不到，使用第一个路径作为默认值
                static_dir = possible_paths[0]

        self.static_dir = Path(static_dir)
        self.http_client = httpx.AsyncClient(follow_redirects=True)

        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Register routes
        self._setup_routes()

    def _setup_routes(self):
        """Setup all route handlers"""

        # Mount output directory for sensitivity analysis images - must be done first
        output_dir = Path("output")
        if not output_dir.exists():
            output_dir.mkdir(exist_ok=True)

        # Mount output directory as static files
        self.app.mount("/output", StaticFiles(directory=str(output_dir)), name="output")

        @self.app.get("/api/health")
        async def health_check():
            """Health check endpoint"""
            return {"status": "healthy"}

        @self.app.post("/api/generate-tree")
        async def generate_tree(request: TreeRequest):
            """Generate decision tree from JSON data and payoff function"""
            try:
                # 动态创建 payoff 函数
                local_vars = {}
                exec(request.payoff_fn_code, globals(), local_vars)
                payoff_fn = local_vars.get("payoff_fn")
                payoff_config = request.payoff_config
                method = payoff_config.get("method", "ev")
                risk_tol = payoff_config.get("risk_tolerance", 0.05)
                utility_fn = payoff_config.get("utility_fn", None)
                print(method, risk_tol, utility_fn)
                if not payoff_fn:
                    raise HTTPException(
                        status_code=400,
                        detail="payoff_fn function not found in the provided code",
                    )

                # 调用 json_to_datanodes 转换为 datanode
                nodes = json_to_datanodes(request.json_data, payoff_fn)
                print(nodes)
                # 创建决策树进行评估
                tree = DecisionTree(nodes=nodes)
                tree.evaluate()
                if utility_fn != "None":
                    tree.rollback(
                        view=method, utility_fn=utility_fn, risk_tolerance=risk_tol
                    )
                else:
                    tree.rollback(view=method)

                # 生成 dot 文件
                dot = tree.plot()
                dot_content = dot.source
                # print(tree)

                # 可选：保存 dot 文件到本地
                dot.save("tree_output.dot")

                return {
                    "success": True,
                    "dot_content": dot_content,
                    "message": "Decision tree generated successfully",
                }

            except Exception as e:
                import traceback

                traceback.print_exc()
                raise HTTPException(
                    status_code=500, detail=f"Error generating decision tree: {str(e)}"
                )

        @self.app.post("/api/sensitivity-analysis")
        async def sensitivity_analysis(request: SensitivityAnalysisRequest):
            """Perform sensitivity analysis on a decision tree"""
            try:
                # 动态创建 payoff 函数
                local_vars = {}
                exec(request.payoff_fn_code, globals(), local_vars)
                payoff_fn = local_vars.get("payoff_fn")

                if not payoff_fn:
                    raise HTTPException(
                        status_code=400,
                        detail="payoff_fn function not found in the provided code",
                    )

                # 调用 json_to_datanodes 转换为 datanode
                nodes = json_to_datanodes(request.json_data, payoff_fn)

                # 创建决策树进行评估
                tree = DecisionTree(nodes=nodes)
                tree.evaluate()

                # 创建概率敏感性分析器
                sensitivity_analyzer = ProbabilisticSensitivity(tree, request.varname)

                # 执行敏感性分析 - 根据节点类型调用相应方法
                # 首先检查变量名对应的节点类型
                target_node = None
                for node in request.json_data["nodes"]:
                    if node["name"] == request.varname:
                        target_node = node
                        break

                if not target_node:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Variable '{request.varname}' not found in the decision tree",
                    )

                # 根据节点类型执行相应的敏感性分析
                if target_node["type"] == "chance":
                    sensitivity_analyzer.probabilistic_sensitivity_chance()
                elif target_node["type"] == "decision":
                    sensitivity_analyzer.probabilistic_sensitivity_decision()
                else:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Cannot perform sensitivity analysis on node type '{target_node['type']}'",
                    )

                # 生成图表文件名
                import uuid

                filename = str(uuid.uuid4())
                plot(sensitivity_analyzer, filename=f"output/{filename}")

                return {
                    "success": True,
                    "message": f"Sensitivity analysis completed for variable '{request.varname}'",
                    "node_type": target_node["type"],
                    "file_url": f"http://localhost:8000/output/{filename}.png",
                }

            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error performing sensitivity analysis: {str(e)}",
                )

        @self.app.post("/api/risk-profile")
        async def risk_profile(request: RiskProfileRequest):
            """Generate risk profile for a decision tree"""
            try:
                # 动态创建 payoff 函数
                local_vars = {}
                exec(request.payoff_fn_code, globals(), local_vars)
                payoff_fn = local_vars.get("payoff_fn")

                if not payoff_fn:
                    raise HTTPException(
                        status_code=400,
                        detail="payoff_fn function not found in the provided code",
                    )

                # 调用 json_to_datanodes 转换为 datanode
                nodes = json_to_datanodes(request.json_data, payoff_fn)

                # 创建决策树进行评估
                tree = DecisionTree(nodes=nodes)
                tree.evaluate()
                tree.rollback()

                # 创建风险分析器
                risk_profile_analyzer = RiskProfile(tree, request.idx)

                # 执行风险分析 - 根据请求参数调用相应方法
                # if request.cumulative:
                #     risk_profile_analyzer.cumulative_risk_profile()
                # else:
                #     risk_profile_analyzer.single_risk_profile()

                # 生成图表文件名
                import uuid

                filename = str(uuid.uuid4())
                plot_risk_profile(risk_profile_analyzer, filename=f"output/{filename}")

                return {
                    "success": True,
                    "message": f"Risk profile generated for index {request.idx}",
                    "file_url": f"http://localhost:8000/output/{filename}.png",
                }

            except Exception as e:
                import traceback

                traceback.print_exc()
                raise HTTPException(
                    status_code=500, detail=f"Error generating risk profile: {str(e)}"
                )

        @self.app.get("/proxy/{path:path}")
        async def proxy_request(path: str):
            """Proxy endpoint that forwards requests to target URL"""
            try:
                base_url = "https://example.com"  # Configurable in the future
                url = f"{base_url}/{path}"
                response = await self.http_client.get(url)
                return StreamingResponse(
                    content=response.iter_bytes(),
                    status_code=response.status_code,
                    headers=dict(response.headers),
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/data")
        async def get_data():
            """Example data endpoint"""
            return {
                "data": [
                    {"id": 1, "name": "Item 1"},
                    {"id": 2, "name": "Item 2"},
                ]
            }

        # Setup static file handling
        if self.static_dir and self.static_dir.exists():

            async def custom_file_response(path: str):
                """Handle static file responses with proper MIME types"""
                file_path = self.static_dir / path
                if not file_path.exists() or not file_path.is_file():
                    file_path = self.static_dir / "index.html"
                    if not file_path.exists():
                        raise HTTPException(
                            status_code=404,
                            detail=f"File not found and no index.html in {self.static_dir}",
                        )

                content_type = (
                    mimetypes.guess_type(str(file_path))[0]
                    or "application/octet-stream"
                )
                return FileResponse(
                    path=str(file_path),
                    media_type=content_type,
                    headers={"Content-Type": content_type},
                )

            @self.app.get("/{full_path:path}")
            async def serve_static(full_path: str):
                """Serve static files with proper MIME types"""
                if full_path.startswith("api/") or full_path.startswith("proxy/"):
                    raise HTTPException(status_code=404, detail="Not Found")
                return await custom_file_response(full_path)
        else:
            # If no static directory is available, show a helpful message
            @self.app.get("/")
            async def root():
                return {
                    "message": "Smart Server is running",
                    "static_dir": str(self.static_dir),
                    "static_dir_exists": self.static_dir.exists()
                    if self.static_dir
                    else False,
                    "api_endpoints": [
                        "/api/health",
                        "/api/generate-tree",
                        "/api/sensitivity-analysis",
                        "/api/risk-profile",
                        "/api/data",
                        "/proxy/{path}",
                    ],
                }

    def run(self, host: str = "0.0.0.0", port: int = 8000, **kwargs):
        """
        Run the server.

        Args:
            host (str): Host to bind to. Defaults to "0.0.0.0".
            port (int): Port to bind to. Defaults to 8000.
            **kwargs: Additional arguments to pass to uvicorn.run
        """
        print(f"Starting Smart Server...")
        print(f"Static files directory: {self.static_dir}")
        print(
            f"Static files available: {self.static_dir.exists() if self.static_dir else False}"
        )
        print(f"API endpoints available at: http://{host}:{port}/api/")

        if kwargs.get("reload", False):
            print("Running in reload mode - automatic reloading enabled")

        uvicorn.run(self.app, host=host, port=port, **kwargs)

    def get_app(self) -> FastAPI:
        """
        Get the FastAPI application instance.

        Returns:
            FastAPI: The FastAPI application instance
        """
        return self.app

    async def shutdown(self):
        """Cleanup resources"""
        await self.http_client.aclose()


# Example usage and entry point
def main():
    # mkdir output
    import os

    os.makedirs("./output", exist_ok=True)
    server = SmartServer()
    server.run(reload=False)


if __name__ == "__main__":
    main()
