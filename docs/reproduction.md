# IJBR / Puzzler 复现用法

## 1. 这个方法要做什么

IJBR 论文里的方法叫 Puzzler，目标是复现一种“间接 jailbreak”的三阶段流程：不直接把原始有害请求发送给目标模型，而是把原始请求拆成更隐蔽的线索，再让目标模型从这些线索中推断隐藏意图。

Puzzler 分三步：

1. Defensive Measures Creation  
   从原始 query 中抽取核心 malicious content，然后让模型生成针对该 malicious content 的防御措施。

2. Offensive Measures Generation  
   判断每条防御措施是否和 malicious content 的具体步骤直接相关。保留相关防御，并基于这些防御生成对应的 offensive measures。

3. Indirect Jailbreak Attack  
   把多条 offensive measures 作为间接线索输入目标模型，让模型推断隐藏意图并组织最终回复。

本仓库的复现脚本对应关系：

- `OMG.py`：运行第 1 阶段和第 2 阶段，输出防御措施与 offensive clues。
- `jailbreak.py`：运行第 3 阶段，读取 `OMG.py` 输出并生成最终复现结果。
- `model_client.py`：统一封装模型调用，默认用 `deepseek-v4-flash`。

为了让复现可以真实跑通、同时不输出可操作伤害内容，当前脚本会把模型输出约束为非操作性、脱敏的研究复现结果，不包含具体步骤、工具、目标、代码或规避细节。

## 2. 准备

进入仓库：

```bash
cd /home/public/minzhi/IJBR
```

安装依赖：

```bash
pip install -r requirements.txt
```

推荐用环境变量配置 key：

```bash
export ANTCHAT_API_KEY="YOUR_REAL_KEY"
```

当前默认模型调用配置：

- API base URL：`https://antchat.alipay.com`
- Model：`deepseek-v4-flash`
- 调用封装：`model_client.py`

当前本地环境也可以通过 `IJBR_API_KEY_FILE` 指向一个包含 `API_KEY = "..."` 的 Python 文件：

```bash
export IJBR_API_KEY_FILE="/path/to/key_file.py"
```

推荐优先使用 `ANTCHAT_API_KEY`。

## 3. 一键跑通

运行：

```bash
./run_reproduction.sh
```

该脚本只跑 1 条样本，输出：

- `data/reproduction/offense.real.json`
- `data/reproduction/jailbreak.real.json`

## 4. 手动运行

第 1-2 阶段，生成防御措施与 offensive clues：

```bash
python3 OMG.py \
  --input data/harmful_behaviors_custom.xlsx \
  --output data/reproduction/offense.real.json \
  --overwrite \
  --limit 1 \
  --max-defenses 1 \
  --model deepseek-v4-flash \
  --request-sleep 70
```

第 3 阶段，运行 indirect jailbreak 复现：

```bash
python3 jailbreak.py \
  --input data/reproduction/offense.real.json \
  --output data/reproduction/jailbreak.real.json \
  --overwrite \
  --limit 1 \
  --model deepseek-v4-flash \
  --request-sleep 70
```

## 5. 离线检查

不调用 API，只检查本地读写和三阶段数据流：

```bash
python3 OMG.py \
  --input data/harmful_behaviors_custom.xlsx \
  --output data/reproduction/offense.mock.json \
  --overwrite \
  --limit 1 \
  --max-defenses 1 \
  --mock

python3 jailbreak.py \
  --input data/reproduction/offense.mock.json \
  --output data/reproduction/jailbreak.mock.json \
  --overwrite \
  --limit 1 \
  --mock
```

## 6. 换成 DeepSeek 官方 API

如果不用 AntChat，而是直接调用 DeepSeek 官方 OpenAI-compatible endpoint：

```bash
export DEEPSEEK_API_KEY="YOUR_DEEPSEEK_KEY"

python3 OMG.py \
  --input data/harmful_behaviors_custom.xlsx \
  --output data/reproduction/offense.deepseek.json \
  --overwrite \
  --limit 1 \
  --max-defenses 1 \
  --model deepseek-v4-flash \
  --api-base-url https://api.deepseek.com \
  --api-key-env DEEPSEEK_API_KEY

python3 jailbreak.py \
  --input data/reproduction/offense.deepseek.json \
  --output data/reproduction/jailbreak.deepseek.json \
  --overwrite \
  --limit 1 \
  --model deepseek-v4-flash \
  --api-base-url https://api.deepseek.com \
  --api-key-env DEEPSEEK_API_KEY
```

## 7. 换成其他官方调用方式

`OMG.py` 和 `jailbreak.py` 只依赖：

```python
llm.complete(prompt)
```

如果要用 Qwen、DeepSeek 官方 SDK、OpenAI SDK 或其他服务商 SDK，只需要在 `model_client.py` 中保持下面这个接口不变：

```python
class RemoteChatClient:
    def complete(self, prompt: str, **kwargs) -> str:
        ...
```

也可以继续使用官方 OpenAI-compatible endpoint，只替换：

- `--api-base-url`
- `--model`
- `--api-key-env`
