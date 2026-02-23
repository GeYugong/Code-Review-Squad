# Code-Review-Squad

一个最小可运行的 **Multi-Agent 代码评审小队**（Dev / Reviewer / Tester / PerfSec），提供 HTTP API：输入「需求 + 代码上下文」，输出「补丁建议 + 审查意见 + 测试建议 + 性能/安全提示」。  
当前版本是 MVP：重点把闭环跑通，后续会加入自动返工、自动跑测试等能力。

---

## 功能概览

- **Dev（实现）**：根据任务与上下文生成统一 diff（或给出实现建议）
- **Reviewer（审查）**：输出分级的 review 问题清单（blocker/major/minor/nit）
- **Tester（测试）**：给出测试用例建议（可选生成 test diff）
- **PerfSec（性能/安全）**：给出性能风险与安全风险点及缓解建议
- **FastAPI 接口**：`POST /review` 一次调用跑完整个小队流程

---

## 项目结构

```text
Code-Review-Squad/
├─ app/
│  ├─ api/
│  │  └─ main.py            # FastAPI 入口
│  ├─ agents/
│  │  ├─ dev.py             # Dev agent
│  │  ├─ reviewer.py        # Reviewer agent
│  │  ├─ tester.py          # Tester agent
│  │  └─ perfsec.py         # Perf/Sec agent
│  ├─ core/
│  │  ├─ llm.py             # 大模型调用封装（OpenAI SDK）
│  │  ├─ orchestrator.py    # 编排器：按顺序/并行调度 agents
│  │  └─ utils.py
│  └─ llm.py
├─ tests/
├─ requirements.txt
├─ README.md
└─ .env                     # 本地环境变量（不要提交）
```

---

## 环境要求

- Windows 11（其他系统也可）
- Python 3.8+（建议 3.11/3.12）
- 已安装 Git
- 需要可用的大模型 API Key（默认读取环境变量 `OPENAI_API_KEY`）

---

## 安装与启动（Windows PowerShell）

### 1）创建虚拟环境并安装依赖

在仓库根目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> 如果 PowerShell 不允许执行脚本：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

---

### 2）配置 API Key

在仓库根目录创建 `.env`（不要提交到 Git）：

```env
OPENAI_API_KEY=你的key
```

项目启动时会读取 `.env`（当前 `app/core/llm.py` 已调用 `load_dotenv()`）。

---

### 3）启动服务

```powershell
uvicorn app.api.main:app --port 8000
```

打开 Swagger：

- http://127.0.0.1:8000/docs

---

## 使用方式

### 方式 A：Swagger UI

在 `/docs` 页面，展开 `POST /review` → `Try it out`，输入示例：

```json
{
	"task": "Add input validation: reject empty username, trim whitespace.",
	"context": "File: app/user.py\n\n\ndef create_user(username: str):\n    return {\"username\": username}\n"
}
```

点击 `Execute` 查看返回。

---

### 方式 B：PowerShell 调用（推荐）

> PowerShell 的 `curl` 常常是别名，建议用 `Invoke-RestMethod`：

```powershell
$body = @{
	task = "Add input validation: reject empty username, trim whitespace."
	context = "File: app/user.py`n`n`ndef create_user(username: str):`n    return {`"username`": username}`n"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/review" -Method Post -ContentType "application/json" -Body $body
```

---

## 返回结果说明

接口返回一个 JSON，包含：

- `patch`：Dev 的补丁建议（通常是 unified diff）
- `review`：Reviewer 的审查输出（建议逐步改成结构化 JSON，便于后续处理）
- `tests`：Tester 的测试建议（可选包含 test diff）
- `perfsec`：性能/安全建议

---

## Windows + Clash/VPN 代理说明（常见坑）

如果你在安装依赖或运行时遇到网络问题（例如 pip 连接失败、模型请求超时），可以在启动前显式设置代理（以 Clash 本地端口 7897 为例）：

```powershell
$env:HTTP_PROXY="http://127.0.0.1:7897"
$env:HTTPS_PROXY="http://127.0.0.1:7897"
```

然后再执行 `pip install ...` 或 `uvicorn ...`。

---

## TODO（下一步计划）

1. **Maintainer（裁判）**：基于规则自动判定是否返工（Blocker 必修，最多 2 轮）
2. **自动应用 patch + 真实跑 pytest**：让 Tester 生成的测试能实际执行并回传结果
3. **读取本地仓库文件**：不再手动粘贴 context，支持传路径/文件列表自动收集上下文
4. **结构化输出**：将 agent 输出统一解析为 JSON，方便前端展示与后续统计

---

## 说明

当前版本是用于验证工作流的 MVP，优先保证链路完整与输出可读性。后续版本会补齐自动返工、自动测试执行、结果追踪与可观测性能力。