---
title: "写作指南：如何发布一篇文章"
date: 2026-09-10
description: "从新建文件到发布上线的完整流程，包含图片、代码、表格等元素的写法，每个组件都附带源码和实际效果对照。"
---

## 1. 新建文章

文章就是 Markdown 文件，放到对应栏目目录即可。推荐用命令创建：

```bash
# 在"深度评测/大语言模型"下新建一篇
hugo new content reviews/llm/my-new-review.md

# 在"使用教程"下新建
hugo new content tutorials/my-guide.md
```

也可以直接手动创建 `.md` 文件。文件开头是 front matter（YAML 元数据）：

```yaml
---
title: "文章标题"
date: 2026-09-10
description: "一句话简介，会显示在列表卡片和 SEO 元数据里"
tags: ["横评", "LLM"]
draft: true   # 草稿状态，只在本地预览可见；写完后删掉这行或改为 false
---
```

## 2. 图片

**方式 A：页面捆绑包（推荐）**——文章改成同名目录 + `index.md`，图片放同一目录：

```text
content/reviews/llm/
└── my-new-review/        # 与文章同名的目录
    ├── index.md          # 文章内容
    ├── cover.png         # 图片直接放旁边
    └── benchmark.png
```

引用时直接写文件名：

```markdown
![评测结果对比](benchmark.png)
```

这种方式图片和文章绑定，移动、删除文章时不会留下孤儿图片。

**方式 B：全局静态目录**——多篇文章共用的图（logo、头像等）放 `static/images/`：

```markdown
![站点 Logo](/images/logo.png)
```

引用路径以 `/` 开头，对应 `static/` 目录。

> [!TIP]
> 截图建议压缩后再入库（PNG → WebP 或 tinypng），仓库和加载速度都会更好。

## 3. 代码

用标准的围栏代码块，**注明语言**即可获得语法高亮，主题自动加语言标签和复制按钮。

**写法：**

````markdown
```python
def hello():
    print("自动带语言标签和复制按钮")
```
````

**效果：**

```python
def hello():
    print("自动带语言标签和复制按钮")
```

## 4. 列表、表格

全部是标准 Markdown。

**写法：**

```markdown
- 无序列表用 `-`
- 缩进两格形成嵌套
  - 嵌套项

| 模型 | 得分 |
|------|------|
| A    | 92   |
| B    | 87   |
```

**效果：**

- 无序列表用 `-`
- 缩进两格形成嵌套
  - 嵌套项

| 模型 | 得分 |
|------|------|
| A    | 92   |
| B    | 87   |

## 5. 提示框（GitHub 风格告警）

**写法：**

```markdown
> [!NOTE]
> 蓝色备注

> [!TIP]
> 绿色建议

> [!WARNING]
> 黄色警告

> [!DANGER]
> 红色危险
```

**效果：**

> [!NOTE]
> 蓝色备注

> [!TIP]
> 绿色建议

> [!WARNING]
> 黄色警告

> [!DANGER]
> 红色危险

## 6. 选项卡 tabs

适合对比多个方案、多平台安装命令。

**写法：**

````markdown
{{</* tabs */>}}
  {{</* tab name="macOS" icon="simple-icons:apple" */>}}
  ```bash
  brew install yourapp
  ```
  {{</* /tab */>}}
  {{</* tab name="Linux" icon="simple-icons:linux" */>}}
  ```bash
  sudo apt install yourapp
  ```
  {{</* /tab */>}}
{{</* /tabs */>}}
````

**效果：**

{{< tabs >}}
  {{< tab name="macOS" icon="simple-icons:apple" >}}
  ```bash
  brew install yourapp
  ```
  {{< /tab >}}
  {{< tab name="Linux" icon="simple-icons:linux" >}}
  ```bash
  sudo apt install yourapp
  ```
  {{< /tab >}}
{{< /tabs >}}

## 7. 步骤 steps

教程分步讲解。

**写法：**

```markdown
{{</* steps */>}}
  {{</* step number="1" title="安装 Hugo" */>}}
  用包管理器安装，macOS：`brew install hugo`
  {{</* /step */>}}
  {{</* step number="2" title="新建站点" */>}}
  执行 `hugo new site mysite`
  {{</* /step */>}}
{{</* /steps */>}}
```

**效果：**

{{< steps >}}
  {{< step number="1" title="安装 Hugo" >}}
  用包管理器安装，macOS：`brew install hugo`
  {{< /step >}}
  {{< step number="2" title="新建站点" >}}
  执行 `hugo new site mysite`
  {{< /step >}}
{{< /steps >}}

## 8. 按钮 button

**写法：**

```markdown
{{</* buttons */>}}
  {{</* button href="/rankings/" variant="primary" icon="mdi:trophy" */>}}模型榜单{{</* /button */>}}
  {{</* button href="/reviews/" variant="ghost" icon="mdi:arrow-right" iconPosition="right" */>}}深度评测{{</* /button */>}}
{{</* /buttons */>}}
```

**效果：**

{{< buttons >}}
  {{< button href="/rankings/" variant="primary" icon="mdi:trophy" >}}模型榜单{{< /button >}}
  {{< button href="/reviews/" variant="ghost" icon="mdi:arrow-right" iconPosition="right" >}}深度评测{{< /button >}}
{{< /buttons >}}

## 9. 图标卡片网格 feature-grid

栏目页展示子分类用的就是它。

**写法：**

```markdown
{{</* feature-grid */>}}
  {{</* feature-card title="大语言模型" icon="mdi:chat-processing" url="/reviews/llm/" */>}}
  对话、推理、写作能力横评。
  {{</* /feature-card */>}}
  {{</* feature-card title="代码模型" icon="mdi:code-braces" url="/reviews/coding/" */>}}
  编程补全与工程实战评测。
  {{</* /feature-card */>}}
{{</* /feature-grid */>}}
```

**效果：**

{{< feature-grid >}}
  {{< feature-card title="大语言模型" icon="mdi:chat-processing" url="/reviews/llm/" >}}
  对话、推理、写作能力横评。
  {{< /feature-card >}}
  {{< feature-card title="代码模型" icon="mdi:code-braces" url="/reviews/coding/" >}}
  编程补全与工程实战评测。
  {{< /feature-card >}}
{{< /feature-grid >}}

## 10. 模型专页与 `specs` 字段

模型专页放在 `content/models/<模型名>/_index.md`，front matter 比普通文章多两个字段：`model: true` 和 `specs`。`specs` 是对比组件（`{{< model-compare >}}`，页面在 `/compare/`）的唯一数据来源，字段展示配置在 `assets/js/custom.js` 的 `FIELDS` 数组里。

### 字段完整定义

`specs` 共 10 个字段，分两组：

**规格组**（字符串，对比时原样展示、不判胜负）：

| 字段 | 展示名 | 类型 | 格式 / 示例 | 说明 |
|------|--------|------|-------------|------|
| `category` | 分类 | string 或数组 | `"国内"`、`["国内","开源"]` | 不显示在对比表，供 `model-compare category=` 按分类过滤 |
| `vendor` | 厂商 | string | `"阿里云"` | 厂商或实验室名称 |
| `released` | 发布时间 | string | `"2026-08"` | 建议 `YYYY-MM` |
| `context` | 上下文窗口 | string | `"1M tokens"` | 数字 + 单位，自由格式 |
| `price_input` | 输入价格 | string | `"¥2/M"` | M = 1M tokens |
| `price_output` | 输出价格 | string | `"¥8/M"` | 同上 |

**跑分组**（数字，对比时大者高亮、并显示分差）：

| 字段 | 展示名 | 类型 | 范围 | 说明 |
|------|--------|------|------|------|
| `scores.reasoning` | 推理 | number | 0–100 | 推理能力跑分 |
| `scores.coding` | 代码 | number | 0–100 | 代码能力跑分 |
| `scores.chinese` | 中文理解 | number | 0–100 | 中文理解跑分 |
| `scores.longtext` | 长文本 | number | 0–100 | 长文本处理跑分 |

### front matter 完整模板

```yaml
---
title: "模型名"
model: true              # 必需：自动收录进 /models/ 总索引
description: "一句话简介。"
specs:
  category: "国内"       # 分类，可为数组；用于按分类过滤对比
  vendor: "厂商名"
  released: "2026-08"
  context: "1M tokens"
  price_input: "¥2/M"
  price_output: "¥8/M"
  scores:
    reasoning: 90
    coding: 85
    chinese: 95
    longtext: 80
hero:
  title: "模型名"
  subtitle: "专题副标题。"
  highlights:
    - icon: "mdi:factory"
      label: "厂商名"
    - icon: "mdi:calendar"
      label: "2026-08 发布"
---
```

**按分类对比**：在任意页面再放一个带 `category` 参数的组件，下拉框就只剩该分类的模型（分类值取自 `specs.category`，数组时任一命中即可）：

````markdown
{{</* model-compare category="国内" */>}}
````

不带参数则对比全部模型，同一页面可以放多个不同分类的组件。

> [!NOTE]
> - 缺失的字段在对比表里显示为 "—"，允许只填部分；建议 10 个字段都填，对比体验完整。
> - 跑分必须是 YAML 数字（不要加引号），否则对比时不会判胜负。
> - 新增一个跑分维度：在 `scores` 下加 key，并同步在 `assets/js/custom.js` 的 `FIELDS` 数组里加一行 `{ group: "跑分", label: "…", key: "scores.xxx", numeric: true }`。

## 11. 预览与发布

```bash
# 本地实时预览（-D 显示草稿），改文件自动刷新
hugo server -D

# 发布前正式构建一次，确认无 WARN/ERROR
hugo
```

确认效果后发布上线：

```bash
git add -A
git commit -m "add: 某某文章"
git push
```

push 之后 Cloudflare 会自动构建部署，约 1-2 分钟后线上生效。

> [!WARNING]
> 记得把 front matter 里的 `draft: true` 删掉，否则线上构建会跳过这篇文章。
