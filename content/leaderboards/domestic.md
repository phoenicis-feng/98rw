---
title: "国产模型榜"
model: false
count: 60
description: "国产厂商模型按综合评分排序（数据源 benchlm.ai，国内外同口径评分）"
---

<!-- 榜单: 国产模型榜 (60个模型) -->
<div class="domestic-chart">
{{< echarts id="chart-domestic" height="460px" enableClick="true" >}}
title: {
  text: '国产模型综合评分 Top 10',
  left: 'center',
  textStyle: { fontSize: 15 }
},
tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
grid: { left: '3%', right: '8%', top: '12%', bottom: '3%', containLabel: true },
xAxis: { type: 'value' },
yAxis: {
  type: 'category',
  inverse: true,
  data: ["Kimi K3", "Qwen3.8 Max", "Qwen3.7 Max", "Qwen3.8-27B", "Hy4 preview", "GLM-5.2", "Qwen3.7 Plus", "DeepSeek V4.1 Flash", "DeepSeek V4 Pro 0813", "GLM-5.3"],
  axisLabel: {
    formatter: function(value, index) {
      var v = [80, 77, 72, 69, 68, 67, 67, 66, 64, 64][index];
      return (index + 1) + '. ' + value + ' (' + v + ')';
    }
  }
},
series: [{
  name: '综合评分',
  type: 'bar',
  data: [80, 77, 72, 69, 68, 67, 67, 66, 64, 64],
  barMaxWidth: 22,
  itemStyle: {
    borderRadius: [0, 4, 4, 0],
    color: function(params) {
      var c = '#e74c3c';
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
| 1 | [Kimi K3](/models/kimi-k3/) | 月之暗面 | 80 | $3/M | $15/M | — | 56.57秒 |
| 2 | [Qwen3.8 Max](/models/qwen3-8-max/) | 阿里通义 | 77 | — | — | — | 55.38秒 |
| 3 | [Qwen3.7 Max](/models/qwen3-7-max/) | 阿里通义 | 72 | — | — | — | 16.58秒 |
| 4 | [Qwen3.8-27B](/models/qwen3-8-27b/) | 阿里通义 | 69 | $0/M | $0/M | — | 51.79秒 |
| 5 | [Hy4 preview](/models/hy4-preview/) | 腾讯 | 68 | $0/M | $0/M | — | — |
| 6 | [GLM-5.2](/models/glm-5-2/) | 智谱 AI | 67 | $1.4/M | $4.4/M | — | 34.33秒 |
| 7 | [Qwen3.7 Plus](/models/qwen3-7-plus/) | 阿里通义 | 67 | — | — | — | 36.90秒 |
| 8 | [DeepSeek V4.1 Flash](/models/deepseek-v4-1-flash/) | 深度求索 | 66 | $0.3/M | $1.2/M | — | 11.25秒 |
| 9 | [DeepSeek V4 Pro 0813](/models/deepseek-v4-pro-0813/) | 深度求索 | 64 | $0.435/M | $0.87/M | — | 30.68秒 |
| 10 | [GLM-5.3](/models/glm-5-3/) | 智谱 AI | 64 | $0/M | $0/M | — | 36.57秒 |
| 11 | [GLM-5.3-Flash](/models/glm-5-3-flash/) | 智谱 AI | 64 | $0/M | $0/M | — | — |
| 12 | [Hy3](/models/hy3/) | 腾讯 | 64 | $0/M | $0/M | — | 26.47秒 |
| 13 | [GLM-5-Turbo](/models/glm-5-turbo/) | 智谱 AI | 63 | $1.2/M | $4/M | — | — |
| 14 | [GLM-5V-Turbo](/models/glm-5v-turbo/) | 智谱 AI | 62 | $1.2/M | $4/M | — | — |
| 15 | [Ling 3.0 Flash VL](/models/ling-3-0-flash-vl/) | 蚂蚁集团 InclusionAI | 62 | $0/M | $0/M | — | — |
| 16 | [MiMo-V2.5-Pro](/models/mimo-v2-5-pro/) | 小米 | 62 | — | — | — | — |
| 17 | [MiMo-V2-Pro](/models/mimo-v2-pro/) | 小米 | 62 | — | — | — | — |
| 18 | [MiniMax M3](/models/minimax-m3/) | MiniMax | 61 | $0.3/M | $1.2/M | — | 24.76秒 |
| 19 | [Kimi K2.6](/models/kimi-2-6/) | 月之暗面 | 60 | $0.95/M | $4/M | — | 2.87秒 |
| 20 | [GLM-5.1](/models/glm-5-1/) | 智谱 AI | 60 | $1.4/M | $4.4/M | — | 60.12秒 |
| 21 | [Qwen3.8-Flash-Next](/models/qwen3-8-flash-next/) | 阿里通义 | 60 | $0/M | $0/M | — | 40.00秒 |
| 22 | [MiMo-V2-Omni](/models/mimo-v2-omni/) | 小米 | 60 | — | — | — | — |
| 23 | [Qwen3.6 Plus](/models/qwen3-6-plus/) | 阿里通义 | 59 | — | — | — | 101.16秒 |
| 24 | [DeepSeek V3.2](/models/deepseek-v3-2/) | 深度求索 | 56 | $0.28/M | $0.42/M | — | 3.75秒 |
| 25 | [DeepSeek V3.1 (Reasoning)](/models/deepseek-v3-1-reasoning/) | 深度求索 | 56 | $0/M | $0/M | — | — |
| 26 | [DeepSeek-R1](/models/deepseek-r1/) | 深度求索 | 56 | $0.55/M | $2.19/M | — | — |
| 27 | [Ling 3.0 Flash FP8](/models/ling-3-0-flash-fp8/) | 蚂蚁集团 InclusionAI | 56 | — | — | — | — |
| 28 | [MiniMax M2.7](/models/minimax-m2-7/) | MiniMax | 55 | $0.3/M | $1.2/M | — | 44.78秒 |
| 29 | [Kimi K2.7 Code](/models/kimi-k2-7-code/) | 月之暗面 | 55 | $0.95/M | $4/M | — | 47.89秒 |
| 30 | [Ling 3.0 Flash](/models/ling-3-0-flash/) | 蚂蚁集团 InclusionAI | 55 | — | — | — | 9.35秒 |
| 31 | [DeepSeek V4 Flash 0731](/models/deepseek-v4-flash-0731/) | 深度求索 | 55 | $0.14/M | $0.28/M | — | 11.08秒 |
| 32 | [MiMo-V2.5](/models/mimo-v2-5/) | 小米 | 55 | — | — | — | 45.64秒 |
| 33 | [Qwen 3.6 Max (preview)](/models/qwen3-6-max-preview/) | 阿里通义 | 55 | — | — | — | — |
| 34 | [GLM-5](/models/glm-5/) | 智谱 AI | 54 | $1/M | $3.2/M | — | 48.44秒 |
| 35 | [Qwen3.6-27B](/models/qwen3-6-27b/) | 阿里通义 | 54 | $0/M | $0/M | — | 105.50秒 |
| 36 | [Kimi K2.5 (Reasoning)](/models/kimi-k2-5-reasoning/) | 月之暗面 | 54 | $0.6/M | $3/M | — | — |
| 37 | [Qwen3 Max](/models/qwen3-max/) | 阿里通义 | 54 | — | — | — | 2.42秒 |
| 38 | [Kimi K2](/models/kimi-k2/) | 月之暗面 | 53 | $0.6/M | $2.5/M | — | 1.67秒 |
| 39 | [Agents-A1](/models/agents-a1/) | 书生 InternScience | 53 | — | — | — | — |
| 40 | [Ling 3.0 Tiny](/models/ling-3-0-tiny/) | 蚂蚁集团 InclusionAI | 53 | $0/M | $0/M | — | — |
| 41 | [DeepSeek V3.1](/models/deepseek-v3-1/) | 深度求索 | 52 | $0/M | $0/M | — | — |
| 42 | [Qwen3 235B 2507](/models/qwen3-235b-2507/) | 阿里通义 | 51 | $0/M | $0/M | — | — |
| 43 | [Qwen3.5 397B](/models/qwen3-5-397b/) | 阿里通义 | 50 | $0.6/M | $3.6/M | — | 42.70秒 |
| 44 | [Qwen3.5-27B](/models/qwen3-5-27b/) | 阿里通义 | 50 | $0/M | $0/M | — | 32.41秒 |
| 45 | [GLM-4.5-Air](/models/glm-4-5-air/) | 智谱 AI | 50 | $0.2/M | $1.1/M | — | 41.38秒 |
| 46 | [MiMo-V2-Flash](/models/mimo-v2-flash/) | 小米 | 50 | $0/M | $0/M | — | 2.14秒 |
| 47 | [Kimi K2.5](/models/kimi-k2-5/) | 月之暗面 | 49 | $0.6/M | $3/M | — | 38.77秒 |
| 48 | [Qwen3.5-122B-A10B](/models/qwen3-5-122b-a10b/) | 阿里通义 | 49 | $0/M | $0/M | — | 18.10秒 |
| 49 | [Qwen3.5 Plus](/models/qwen3-5-plus/) | 阿里通义 | 48 | $0.4/M | $2.4/M | — | — |
| 50 | [Qwen3.6-35B-A3B](/models/qwen3-6-35b-a3b/) | 阿里通义 | 47 | — | — | — | 43.90秒 |
| 51 | [Hy3 Preview](/models/hy3-preview/) | 腾讯 | 46 | $0/M | $0/M | — | — |
| 52 | [DeepSeek V3](/models/deepseek-v3/) | 深度求索 | 46 | $0.27/M | $1.1/M | — | — |
| 53 | [GLM-4.6](/models/glm-4-6/) | 智谱 AI | 45 | — | — | — | 3.57秒 |
| 54 | [Qwen3.5-35B-A3B](/models/qwen3-5-35b-a3b/) | 阿里通义 | 44 | $0/M | $0/M | — | 16.09秒 |
| 55 | [GLM-4.7](/models/glm-4-7/) | 智谱 AI | 43 | $0/M | $0/M | — | 28.72秒 |
| 56 | [Qwen3 235B 2507 (Reasoning)](/models/qwen3-235b-2507-reasoning/) | 阿里通义 | 43 | $0/M | $0/M | — | — |
| 57 | [Qwen3.5 Flash](/models/qwen3-5-flash/) | 阿里通义 | 42 | $0.1/M | $0.4/M | — | — |
| 58 | [Ling 2.6 Flash](/models/ling-2-6-flash/) | 蚂蚁集团 InclusionAI | 41 | — | — | — | 1.07秒 |
| 59 | [Qwen3-Omni-30B-A3B-Instruct](/models/qwen3-omni-30b-a3b-instruct/) | 阿里通义 | 38 | — | — | — | 1.86秒 |
| 60 | [DeepSeek R1 Distill Qwen 32B](/models/deepseek-r1-distill-qwen-32b/) | 深度求索 | 38 | $0/M | $0/M | — | 0.84秒 |
