---
title: "国产性价比榜"
model: false
count: 23
description: "平衡算法：价格分×70%（对数归一化，越便宜越高）+ 评分分×30%（0-100 平衡分，越高越划算；免费模型不参与）"
---

<!-- 榜单: 国产性价比榜 (23个模型) -->
<div class="domestic-chart">
{{< echarts id="chart-domestic_value" height="460px" enableClick="true" >}}
title: {
  text: '国产模型性价比 Top 10（价格 70% + 评分 30%）',
  left: 'center',
  textStyle: { fontSize: 15 }
},
tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
grid: { left: '3%', right: '8%', top: '12%', bottom: '3%', containLabel: true },
xAxis: { type: 'value' },
yAxis: {
  type: 'category',
  inverse: true,
  data: ["DeepSeek V4 Flash 0731", "DeepSeek V3.2", "DeepSeek V4 Pro 0813", "Qwen3.5 Flash", "DeepSeek V4.1 Flash", "MiniMax M3", "MiniMax M2.7", "GLM-4.5-Air", "DeepSeek V3", "DeepSeek-R1"],
  axisLabel: {
    formatter: function(value, index) {
      var v = [80.3, 73.9, 67.4, 63.7, 63.4, 59.4, 54.7, 52.3, 49.1, 44.9][index];
      return (index + 1) + '. ' + value + ' (' + v + ')';
    }
  }
},
series: [{
  name: '性价比',
  type: 'bar',
  data: [80.3, 73.9, 67.4, 63.7, 63.4, 59.4, 54.7, 52.3, 49.1, 44.9],
  barMaxWidth: 22,
  itemStyle: {
    borderRadius: [0, 4, 4, 0],
    color: function(params) {
      var c = '#f39c12';
      return params.dataIndex < 3
        ? echarts.color.lift(c, 0.12 * (3 - params.dataIndex))
        : c;
    }
  },
  label: { show: true, position: 'right' }
}]
{{< /echarts >}}
</div>

| 排名 | 模型 | 厂商 | 评分 | 输入价格 | 输出价格 | 速度 | 首字延迟 |
|------|------|------|------|----------|----------|------|------ |
| 1 | [DeepSeek V4 Flash 0731](/models/deepseek-v4-flash-0731/) | 深度求索 | 55 | $0.14/M | $0.28/M | — | 11.08秒 |
| 2 | [DeepSeek V3.2](/models/deepseek-v3-2/) | 深度求索 | 56 | $0.28/M | $0.42/M | — | 3.75秒 |
| 3 | [DeepSeek V4 Pro 0813](/models/deepseek-v4-pro-0813/) | 深度求索 | 64 | $0.435/M | $0.87/M | — | 30.68秒 |
| 4 | [Qwen3.5 Flash](/models/qwen3-5-flash/) | 阿里通义 | 42 | $0.1/M | $0.4/M | — | — |
| 5 | [DeepSeek V4.1 Flash](/models/deepseek-v4-1-flash/) | 深度求索 | 66 | $0.3/M | $1.2/M | — | 11.25秒 |
| 6 | [MiniMax M3](/models/minimax-m3/) | MiniMax | 61 | $0.3/M | $1.2/M | — | 24.76秒 |
| 7 | [MiniMax M2.7](/models/minimax-m2-7/) | MiniMax | 55 | $0.3/M | $1.2/M | — | 44.78秒 |
| 8 | [GLM-4.5-Air](/models/glm-4-5-air/) | 智谱 AI | 50 | $0.2/M | $1.1/M | — | 41.38秒 |
| 9 | [DeepSeek V3](/models/deepseek-v3/) | 深度求索 | 46 | $0.27/M | $1.1/M | — | — |
| 10 | [DeepSeek-R1](/models/deepseek-r1/) | 深度求索 | 56 | $0.55/M | $2.19/M | — | — |
| 11 | [GLM-5.2](/models/glm-5-2/) | 智谱 AI | 67 | $1.4/M | $4.4/M | — | 34.33秒 |
| 12 | [Kimi K2](/models/kimi-k2/) | 月之暗面 | 53 | $0.6/M | $2.5/M | — | 1.67秒 |
| 13 | [GLM-5-Turbo](/models/glm-5-turbo/) | 智谱 AI | 63 | $1.2/M | $4/M | — | — |
| 14 | [GLM-5V-Turbo](/models/glm-5v-turbo/) | 智谱 AI | 62 | $1.2/M | $4/M | — | — |
| 15 | [Kimi K2.5 (Reasoning)](/models/kimi-k2-5-reasoning/) | 月之暗面 | 54 | $0.6/M | $3/M | — | — |
| 16 | [Kimi K2.6](/models/kimi-2-6/) | 月之暗面 | 60 | $0.95/M | $4/M | — | 2.87秒 |
| 17 | [Qwen3.5 Plus](/models/qwen3-5-plus/) | 阿里通义 | 48 | $0.4/M | $2.4/M | — | — |
| 18 | [GLM-5](/models/glm-5/) | 智谱 AI | 54 | $1/M | $3.2/M | — | 48.44秒 |
| 19 | [GLM-5.1](/models/glm-5-1/) | 智谱 AI | 60 | $1.4/M | $4.4/M | — | 60.12秒 |
| 20 | [Kimi K2.5](/models/kimi-k2-5/) | 月之暗面 | 49 | $0.6/M | $3/M | — | 38.77秒 |
| 21 | [Kimi K2.7 Code](/models/kimi-k2-7-code/) | 月之暗面 | 55 | $0.95/M | $4/M | — | 47.89秒 |
| 22 | [Qwen3.5 397B](/models/qwen3-5-397b/) | 阿里通义 | 50 | $0.6/M | $3.6/M | — | 42.70秒 |
| 23 | [Kimi K3](/models/kimi-k3/) | 月之暗面 | 80 | $3/M | $15/M | — | 56.57秒 |
