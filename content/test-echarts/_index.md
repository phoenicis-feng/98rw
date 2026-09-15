---
title: "ECharts 图表测试"
date: 2026-09-15
description: "测试 ECharts Hugo shortcode 的多种图表类型"
---

## 柱状图（竖向条形图）

每个柱子的颜色不同：

{{< echarts id="vertical-bar" height="450px" >}}
title: {
  text: '各季度销售对比',
  left: 'center'
},
tooltip: {
  trigger: 'axis',
  axisPointer: {
    type: 'shadow'
  }
},
legend: {
  data: ['A 组', 'B 组'],
  top: '8%'
},
grid: {
  left: '3%',
  right: '4%',
  bottom: '3%',
  containLabel: true
},
xAxis: {
  type: 'category',
  data: ['Q1', 'Q2', 'Q3', 'Q4']
},
yAxis: {
  type: 'value'
},
series: [
  {
    name: 'A 组',
    type: 'bar',
    data: [120, 200, 150, 180],
    itemStyle: {
      color: '#FF6B6B'
    }
  },
  {
    name: 'B 组',
    type: 'bar',
    data: [80, 150, 200, 120],
    itemStyle: {
      color: '#4ECDC4'
    }
  }
]
{{< /echarts >}}

## 横向条形图

横向条形图，每个数据的颜色都不同：

{{< echarts id="horizontal-bar" height="450px" >}}
title: {
  text: '编程语言热度排名',
  left: 'center'
},
tooltip: {
  trigger: 'axis',
  axisPointer: {
    type: 'line'
  }
},
grid: {
  left: '12%',
  right: '4%',
  bottom: '3%',
  containLabel: true
},
xAxis: {
  type: 'value'
},
yAxis: {
  type: 'category',
  data: ['Rust', 'Go', 'TypeScript', 'Python', 'Java']
},
series: [
  {
    name: '热度',
    type: 'bar',
    data: [95, 88, 82, 75, 60],
    itemStyle: {
      color: function(params) {
        var colors = ['#FF6B6B', '#FFD93D', '#6BCB77', '#4D96FF', '#9C51B6'];
        return colors[params.dataIndex];
      }
    }
  }
]
{{< /echarts >}}

## 雷达图

多个维度的数据对比，每个维度颜色不同：

{{< echarts id="radar-chart" height="500px" >}}
title: {
  text: '模型能力评测',
  left: 'center'
},
tooltip: {
  trigger: 'item'
},
legend: {
  data: ['模型 A', '模型 B'],
  top: '10%'
},
radar: {
  radius: '65%',
  center: ['50%', '55%'],
  splitArea: {
    areaStyle: {
      color: ['rgba(122, 184, 255, 0.1)', 'rgba(122, 184, 255, 0.05)', 'rgba(122, 184, 255, 0.05)', 'rgba(122, 184, 255, 0.02)']
    },
    splitLine: {
      lineStyle: {
        color: 'rgba(122, 184, 255, 0.3)'
      }
    }
  },
  indicator: [
    { name: '推理', max: 100 },
    { name: '编码', max: 100 },
    { name: '数学', max: 100 },
    { name: '知识', max: 100 },
    { name: '速度', max: 100 },
    { name: '创造', max: 100 }
  ]
},
series: [
  {
    name: '模型 A',
    type: 'radar',
    lineStyle: {
      width: 3
    },
    emphasis: {
      linestyle: {
        width: 5
      }
    },
    data: [{
      value: [85, 90, 78, 92, 88, 70],
      name: '模型 A'
    }],
    itemStyle: {
      color: '#FF6B6B'
    }
  },
  {
    name: '模型 B',
    type: 'radar',
    lineStyle: {
      width: 3
    },
    emphasis: {
      linestyle: {
        width: 5
      }
    },
    data: [{
      value: [75, 82, 85, 78, 95, 88],
      name: '模型 B'
    }],
    itemStyle: {
      color: '#4ECDC4'
    }
  }
]
{{< /echarts >}}

## 饼图（自定义颜色）

每个扇形颜色不同，悬浮展开效果：

{{< echarts id="custom-pie" height="450px" >}}
title: {
  text: '浏览器市场份额',
  left: 'center',
  top: '5%'
},
tooltip: {
  trigger: 'item',
  formatter: '{a} <br/>{b}: {c} ({d}%)'
},
legend: {
  orient: 'vertical',
  left: 'left',
  top: '15%',
  data: ['Chrome', 'Safari', 'Firefox', 'Edge', 'Other']
},
series: [
  {
    name: '浏览器',
    type: 'pie',
    radius: ['50%', '70%'],
    center: ['60%', '55%'],
    avoidLabelOverlap: false,
    label: {
      show: false,
      position: 'center'
    },
    emphasis: {
      label: {
        show: true,
        fontSize: '18',
        fontWeight: 'bold'
      }
    },
    labelLine: {
      show: false
    },
    data: [
      { value: 62.5, name: 'Chrome', itemStyle: { color: '#4D96FF' } },
      { value: 18.0, name: 'Safari', itemStyle: { color: '#FF6B6B' } },
      { value: 10.0, name: 'Firefox', itemStyle: { color: '#FFD93D' } },
      { value: 6.0, name: 'Edge', itemStyle: { color: '#6BCB77' } },
      { value: 3.5, name: 'Other', itemStyle: { color: '#9C51B6' } }
    ]
  }
]
{{< /echarts >}}
