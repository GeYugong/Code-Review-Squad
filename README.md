# Code-Review-Squad

一个可运行的 Multi-Agent 代码评审服务，输入需求与代码上下文，输出补丁、评审、测试建议和性能/安全建议。

## 功能

- `Dev`：生成 patch（unified diff）
- `Reviewer`：输出分级问题（`blocker/major/minor/nit`）
- `Tester`：输出测试点和可选测试 patch
- `PerfSec`：输出性能与安全风险
- `Maintainer`：根据评审结果决定 `accept` 或 `rework`，支持最多 N 轮返工

## API

`POST /review`

请求体字段：

- `task`: string，必填
- `context`: string，可选。传了就直接用
- `repo_root`: string，可选。`context` 为空时用于自动收集上下文
- `files`: string[]，可选。指定收集哪些文件
- `include_globs`: string[]，可选。未指定 `files` 时按 glob 扫描
- `max_files`: int，默认 `20`
- `max_chars_per_file`: int，默认 `5000`
- `max_rounds`: int，默认 `2`

返回字段：

- `patch`
- `review`
- `tests`
- `perfsec`
- `maintainer`
- `rounds_used`

## 安装与启动

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

创建 `.env`：

```env
OPENAI_API_KEY=your_key
```

启动：

```powershell
uvicorn app.api.main:app --port 8000
```

文档：

- http://127.0.0.1:8000/docs

## 示例请求

```json
{
  "task": "Add input validation for create_user",
  "context": "File: app/user.py\n\ndef create_user(username: str):\n    return {\"username\": username}\n",
  "max_rounds": 2
}
```

或者自动收集本地仓库上下文：

```json
{
  "task": "Refactor duplicated logic",
  "repo_root": ".",
  "files": ["app/api/main.py", "app/core/orchestrator.py"],
  "max_rounds": 2
}
```

## 运行测试

```powershell
pytest -q
```
