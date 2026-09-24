# 科学多模态时序大模型与科学推理大模型综述（中文概述）

**论文全称**：*Foundation Models and Reasoning LLMs for Scientific Multimodal Time Series: A Survey*  
**维护机构**：Antigravity Autonomous Research Loop (`lihuirui/awesome-scientific-time-series-foundation-models-survey`)  
**当前版本**：v1.0 (迭代 1 - 启动与骨架奠基阶段)  
**更新日期**：2026-09-24  

---

## 1. 综述背景与研究动机 (Introduction & Motivation)

在过去十年中，深度学习在通用时间序列预测与时空数据挖掘（如城市交通、金融行情、人体姿态）取得了长足进步。然而，当技术延伸至**地球与自然科学物理系统**（自然科学领域：天气预报、气候模拟、极端洪水演进、海洋动力学、遥感对地观测、地震监测与日地空间天气）时，经典方法面临严峻瓶颈：
1. **多物理模态异构性**：物理世界产生的数据跨越离散站点时序（雨量站、水文站、地震台网）、高维网格再分析场（如 ECMWF ERA5、MERRA-2）、多光谱/高光谱卫星影像序列、物理波形与连续张量场。
2. **多尺度连续动力学**：物理现象在空间上跨越米级局部湍流至数万公里全球环流；时间上跨越秒级（地震波）、天级（台风路径）、至百年级（气候变化）。
3. **物理守恒律与一致性约束**：经典神经网络容易产生“物理幻觉”（违背质量守恒、动量守恒或能量守恒），在极值灾害场景出现累积漂移或虚假平滑。
4. **科学推理与智能体决策瓶颈**：随着大语言模型（LLM）的兴起，如何让通用智能体理解科学时间序列并进行专业假设验证、工具编排与多步科学推理（Scientific Reasoning），成为当前学术界最前沿的交叉课题。

本文首次系统梳理 **面向自然科学领域的科学多模态时序基础模型（Scientific Multimodal Time Series Foundation Models）** 与 **科学时序推理大语言模型（Scientific Reasoning LLMs / Agents）**，构建了一套严格对齐物理规律与计算范式的分类体系。

---

## 2. 核心分类框架 (Taxonomy Architecture)

根据 Jin et al. (arXiv:2310.10196, 2310.10196) 的经典结构，本综述从四个正交维度解构科学时序基础模型：

```
                               科学多模态时序大模型与科学推理 LLM 体系
                                                │
       ┌────────────────────────┼───────────────┴────────────────┼────────────────────────┐
       ▼                        ▼                                ▼                        ▼
 [维度 1: 科学领域与模态]  [维度 2: 基础模型骨架网络]      [维度 3: 物理规律融合层次]   [维度 4: 大模型科学推理角色]
  - 气象与气候 (ERA5/雷达)   - 3D 空间球形 Transformer      - 纯数据驱动 (统计回归)       - 科学推理核心 (SciTS/TimeOmni)
  - 对地观测与遥感时序      - 多重网格图神经网络 (GNN)     - 软物理约束损失函数 (PINN)   - 上下文增强器 (ClimateLLM)
  - 水文与极端洪水预报      - 连续神经算子 (AFNO/SFNO)      - 硬投影物理守恒结构          - 自主科学智能体 (ClimateAgent)
  - 海洋动力学 (GLORYS)     - 跨模态掩码自编码器 (MAE)      - 混合动力偏微分方程求解器    - 自然语言交互接口
  - 地震学与地球物理波形    - 扩散概率生成模型 (Diffusion)
  - 空间天气与日地物理
```

### 维度 1：科学领域与多模态数据源 (Scientific Domains & Modalities)
- **气象与全球气候**：以 ECMWF ERA5、IFS HRES、MERRA-2 为代表的高维三维大气再分析张量（包含位势高度、温度、U/V 风场、比湿等数十种变量及多个气压层）。
- **对地观测与遥感**：融合 Sentinel-1 (SAR)、Sentinel-2 (多光谱)、Landsat 与高程 DEM 的多时相像素/面域时序。
- **水文与水资源**：全球数千个河流测站的流量时序、集水区地形属性与陆面降水/蒸发网格场。
- **海洋动力学**：海表面高度 (SSH)、海表温度 (SST)、盐度与三维洋流涡旋场。
- **地球物理与地震学**：三分量高频连续地震波形张量（STEAD、INSTANCE 数据集）。
- **空间天气与日地物理**：NASA SDO 卫星 13 年多波段极紫外 (EUV) 影像时序与光球磁场图。

### 维度 2：模型代表骨架与预训练范式 (Backbones & Pretraining)
- **3D 地球空间 Transformer**：以 **Pangu-Weather (盘古气象)** 为代表，提出 3D Earth-Specific Transformer，引入高度层特定的自注意力与层次化时间汇聚；以 **Aurora (极光)** 为代表，扩展至 13 亿参数的多源 3D Perceiver 架构。
- **多重网格图神经网络 (Multi-Mesh GNNs)**：以 DeepMind **GraphCast** 为代表，在 icosahedral（正二十面体）多层球形网格上执行空间消息传递，有效避免极地投影形变。
- **自适应傅里叶神经算子 (AFNO/SFNO)**：以 NVIDIA **FourCastNet** 为代表，利用频域谱卷积实现网格无关的连续空间算子映射。
- **级联自回归 Transformer**：以复旦大学 **FuXi (伏羲)** 为代表，采用短期、中期、长期三阶段级联策略缓解长时段预测累积误差。
- **跨模态掩码自编码 (Multimodal Spatio-Temporal MAE)**：以 **SatMAE**、**Presto**、**Galileo** 为代表，利用时间-波段双重掩码重建自监督预训练。
- **生成式扩散集合预报 (Diffusion Ensembles)**：以 DeepMind **GenCast** 为代表，采用隐空间扩散去噪生成具有物理扰动特性的概率集合预报。

### 维度 3：物理先验与物理约束机制 (Physics Integration Levels)
1. **纯数据驱动 (Purely Data-Driven)**：完全依赖海量再分析数据（如 ERA5 40年时序）拟合动力演化，通过大模型容量隐式捕捉流动特征。
2. **软物理损失惩罚 (Soft Physics Loss Penalties)**：在损失函数中显式加入动能守恒、散度为零约束或质量通量惩罚项（如 FengWu、FourCastNet）。
3. **硬物理投影约束 (Hard Architectural Conservation Constraints)**：在网络输出端通过正交投影算子或守恒层，保证输出状态严格满足连续性方程。
4. **混合神经-偏微分方程耦合系统 (Hybrid PDE-Neural Solvers)**：神经网络预测局部通量或径流，外接物理连续性方程路由求解器（如 Google Global Flood 系统）。

### 维度 4：大语言模型在科学时序中的推理角色 (Role of Reasoning LLMs)
1. **科学推理核心 (Scientific Reasoner)**：如 **SciTS (TimeOmni)**，构建涵盖 12 个自然科学学科的专业时序指令微调基准，使 LLM 能够结合专业知识解释物理规律。
2. **频域感知上下文增强 (Contextual Enhancer)**：如 **ClimateLLM**，利用傅里叶谱分解捕获周期性动力，将时序投影为 LLM 词表前缀向量进行时序预测。
3. **自主科学多智能体 (Autonomous Scientific Agent)**：如 **ClimateAgent**，通过规划、检索、分析、代码执行智能体协作，自主调用专业气象/水文诊断工具包完成端到端科学研究。

---

## 3. 标准化评估基准与对比进展 (Benchmarks & Evaluation)

### 3.1 气象领域基准：WeatherBench 2
Google 与 ECMWF 等联合建立的 **WeatherBench 2** 成为评估全球数据驱动气象大模型的行业黄金标准：
- **评估指标**：纬度加权均方根误差 (Latitude-weighted RMSE)、异常相关系数 (ACC)、连续分级概率评分 (CRPS)、谱能量分布 (Energy Spectrum)。
- **核心结论**：在 1-10 天确定性预报中，GraphCast、Pangu-Weather、FuXi、FengWu 在 90% 以上的气象指标上超越传统欧洲中期天气预报中心高分辨率数值预报系统 (ECMWF IFS HRES)；但在极端极值捕获与长时段能量守恒方面，生成式模型（GenCast）展现出显著优势。

### 3.2 科学推理基准：SciTS
涵盖天文学（恒星光变曲线）、气象学、神经科学等 12 个学科、43 项下游任务。基准测试表明，直接使用通用文本大模型进行数值时序拟合效果受限，而采用统一连续时序 Tokenizer（如 TimeOmni）与专业跨学科科学微调，能使大模型具备对物理时序的因果归因与生成能力。

---

## 4. 关键挑战与未来展望 (Open Challenges & Future Directions)

1. **跨分辨率与跨物理场统一表示 (Universal Scientific Tokenization)**：如何构建同时支持离散测站、三维气象网格、卫星影像与波形信号的多模态科学物理基底模型。
2. **硬物理守恒与极端极值外推 (Physical Trust & Extremes)**：解决纯数据驱动模型在罕见世纪灾害（如极端干旱、特大风暴）下的平滑欠拟合问题，探索物理神经算子与大模型隐式流形的深度融合。
3. **自主科学发现闭环 (Closed-loop Scientific Discovery)**：发展能够自主提出科学假设、设计仿真实验、驱动时序基础模型推演并反思校验的科学 AI 智能体体系。
