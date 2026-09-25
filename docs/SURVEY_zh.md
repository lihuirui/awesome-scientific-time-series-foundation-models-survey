# 科学多模态时序大模型与科学推理大模型综述（中文概述）

**论文全称**：*Foundation Models and Reasoning LLMs for Scientific Multimodal Time Series: A Survey*  
**维护机构**：Antigravity Autonomous Research Loop (`lihuirui/awesome-scientific-time-series-foundation-models-survey`)  
**当前版本**：v4.0 (迭代 4 - 跨学科全景定量评测元表、超算能耗与算力开销评测、多智能体科学推理 DAG 闭环系统)  
**更新日期**：2026-09-26  
**论文正文**：[`paper/main.pdf`](file:///workspace/survey-sci-ts/paper/main.pdf) (IEEEtran 双栏, 11 页, 包含 7 幅高分辨率出版级图表与 4 个全景对比表格)

---

## 1. 综述背景与研究动机 (Introduction & Motivation)

在过去十年中，深度学习在通用时间序列预测与时空数据挖掘（如城市交通、金融行情、人体姿态）取得了长足进步。然而，当技术延伸至**自然科学与地球物理系统**（大气天气预报、百年轻慢气候演变、流域水文与极端洪涝、海洋多尺度动力学、对地观测与卫星遥感、地震台网波形监测与日地空间物理）时，传统深度时序模型遭遇深刻瓶颈：

1. **多物理模态极端异构**：科学时序跨越离散不规则测站观测（雨量站、水文计、地震台网）、连续空间再分析网格场（ECMWF ERA5, MERRA-2）、多光谱/高光谱卫星影像序列（Sentinel-1/2, Landsat）、连续物理张量波形与跨圈层通量数据。
2. **多尺度连续动力学**：物理现象在空间上跨越米级局部湍流至数万公里全球环流；时间尺度跨越毫秒级（地震破裂波形）、小时/天级（强对流降水与台风路径）、至百年/千年级（温室气体驱动的气候变暖）。
3. **物理守恒律与一致性约束**：经典自回归神经网络易发生“物理幻觉”（违背质量守恒、动量守恒或能量守恒），在长时段循环推演中出现累积谱衰减、过度平滑或极端事件失真。
4. **科学推理与智能体决策**：随着大语言模型（LLM）的爆发，如何使智能体深度理解物理时序中的空间依赖与动力演进，具备科学假设生成、物理参数反演、多工具编排与闭环科学推理（Scientific Reasoning）能力，成为人工智能驱动科学研究（AI for Science）的核心命题。

本综述系统梳理了 2021 年至今自然科学领域的 **科学多模态时序基础模型（Scientific Multimodal Time Series Foundation Models）** 与 **科学时序推理大语言模型（Scientific Reasoning LLMs / Multi-Agent Systems）**，收录并深度解构了 47 篇经过学术 API 严格验证的标志性研究。

---

## 2. 核心分类体系 (4-Pillar Taxonomy Architecture)

本综述从四个正交的理论与计算维度，构建了贯穿科学多模态时序研究的全景分类体系：

```
                                科学多模态时序大模型与科学推理 LLM 体系
                                                 │
        ┌────────────────────────┼───────────────┴────────────────┼────────────────────────┐
        ▼                        ▼                                ▼                        ▼
  [维度 1: 科学领域与模态]  [维度 2: 基础模型骨架网络]      [维度 3: 物理规律融合层次]   [维度 4: 大模型科学推理角色]
   - 全球气象与长期气候      - 3D 空间球形 Transformer      - 纯数据驱动 (统计回归)       - 科学推理核心 (SciTS/TimeOmni)
   - 对地观测与多光谱遥感    - 多重网格图神经网络 (GNN)     - 软物理约束损失函数 (PINN)   - 上下文增强器 (ClimateLLM)
   - 水文流域与洪涝预报      - 连续神经算子 (AFNO/SFNO)      - 硬投影物理守恒结构          - 多模态科学对齐 (K2/GeoChat)
   - 海洋流场与涡旋动力学    - 跨模态掩码自编码器 (MAE)      - 混合动力偏微分方程系统      - 自主科学智能体 (ClimateAgent/OceanGPT)
   - 地震学与地球物理波形    - 生成式扩散集合 (Diffusion)    (如 NeuralGCM 可微动力核)
   - 空间天气与太阳物理      - 动态波长超网络 (DOFA)
```

### 维度 1：自然科学领域与多模态数据源 (Scientific Domains & Modalities)
- **全球天气预报 (Weather Forecasting)**：以 ECMWF ERA5 为主流预训练语料，包含多层三维大气动力场（位势高度 $Z$、温度 $T$、风场 $U/V$、比湿 $Q$），模型分辨率从 0.25° (~28 km) 逐步推进至公里级。代表工作：Pangu-Weather、GraphCast、FourCastNet、FuXi、FengWu、Aurora、Prithvi WxC、Stormer（随机动态时间 Patching）。
- **气候模拟与长期预估 (Climate Modeling)**：面向百年尺度演化，模拟全球表面温度 ($TAS$)、区域降水量 ($PR$) 对温室气体与气溶胶排放情景的响应。代表基准与模型：ClimateBench、ClimaX、ACE、ClimSim（NeurIPS 2023 杰出论文，涵盖 5.7 亿高分辨率垂直柱样本的混合多尺度物理参数化基准）。
- **对地观测与多模态遥感 (Earth Observation & Remote Sensing)**：融合 Sentinel-1 (SAR)、Sentinel-2 (多光谱)、Landsat 与高程 DEM 的多时相、多波长序列。代表工作：SatMAE、Presto、Galileo、DOFA（动态波长超网络实现任意光学-SAR-热红外模态即插即用）、EarthPT（基于 700M 参数的全球网格遥感时序自回归基础模型）。
- **水文流域与洪涝演进 (Hydrology & Streamflow)**：跨越全球数千个水文流域。代表工作：Google Global Flood、Caravan（涵盖全球 6,830 个集水区的标准化水文基准）。
- **海洋动力学与流场 (Oceanography)**：模拟海表面高度异常 (SSH)、海表温度 (SST) 与中尺度涡旋演化。代表工作：XiHe、OceanGPT（融合海洋动力学与具身轨迹推理的专业大模型）、OceanBench（NeurIPS 2025 全球海洋对地观测与流场多任务基准平台）。
- **地震学与地球物理波形 (Seismology & Waveforms)**：利用高频连续三分量台网波形实现微震检测与走时拾取。代表工作：SeisT、QuakeFlow、SeisBench（SRL 2022 全球多区域标准化地震机器学习基准与开源生态）。
- **日地物理与空间天气 (Space Weather & Solar Physics)**：利用 SDO 极紫外 (EUV) 影像与光球磁场时序，实现太阳耀斑预测。代表工作：SurffNet。
- **通用跨学科科学时序 (Cross-Domain Scientific Time Series)**：突破领域孤岛，实现多学科时序的跨域预训练与零样本迁移。代表工作：UniTS（NeurIPS 2024 统一多任务时序大模型）、MOMENT（ICML 2024 开源通用时序基础模型族）。

### 维度 2：核心骨架网络与空间离散化 (Core Backbones & Discretization)
- **3D 空间球形 Transformer**：如 **Pangu-Weather** 引入针对地球几何特征的高程感知三维注意力，结合多时步层级自回归；**Aurora** 则利用 3D Perceiver 架构将不同垂直分辨率与变量压缩为潜在空间表示。
- **多重网格图神经网络 (Multi-Mesh GNNs)**：如 **GraphCast** 构建从正二十面体 (Icosahedral) 递归细分的多层空间立体图网格，消息在网格层次间双向传递，彻底避免传统等经纬度网格在南北两极的网格奇异性。
- **球面傅里叶神经算子 (SFNO / AFNO)**：如 **SFNO**（Bonev et al., ICML 2023）在二维球面上严格引入离散球面调和变换（Spherical Harmonics $Y_\ell^m$），在谱域实现频域卷积，具备天然的连续空间表示与 $\mathrm{SO}(3)$ 球面旋转等变性；**FourCastNet** 则在展平网格上采用自适应傅里叶神经算子 (AFNO)。
- **跨模态掩码自编码器 (Multimodal Spatio-Temporal MAE)**：如 **Galileo**、**Presto** 与 **SatMAE**，将时间步长、空间 Patch 与传感器波段联合编码，采用高比例掩码自回归重建预训练。
- **动态波长超网络 (Wavelength Hypernetworks)**：如 **DOFA**（Xiong et al., CVPR 2024），引入连续波长超网络动态生成视觉骨干的卷积/注意力权重，打破多传感器波段对齐壁垒。
- **统一时序补丁化与跨域分词 (Universal Time Series Patching & Tokenization)**：如 **UniTS** 与 **MOMENT** 采用统一时间步长自适应分词与跨变量掩码，**Stormer** 引入空间随机 Patching 破坏空间网格的固定归纳偏置，显著缓解自回归误差积累。
- **连续生成式扩散集合预报 (Generative Score-Based Diffusion Ensembles)**：如 **GenCast** 与 **SEEDS**（Li et al., Science Advances 2024），利用条件随机微分方程（SDE）与得分匹配（Score Matching），直接从真实物理后验中采样高分辨率集合成员，彻底克服确定性自回归模型的谱能量模糊。

### 维度 3：物理规律融合层次 (Physics Integration Levels)
1. **纯数据驱动 (Purely Data-Driven)**：完全依赖数据规模与模型容量隐式拟合物理场演进。
2. **软物理损失惩罚 (Soft Physics Loss Penalties)**：在损失函数中显式加入动能守恒、散度为零约束或质量通量惩罚项（如 FengWu、FourCastNet）。
3. **硬几何与结构守恒 (Hard Architectural Constraints)**：在模型架构内部设置正交投影层或保通量层，确保每一步预测严格满足质量连续性方程。
4. **混合神经-偏微分方程可微动力核 (Differentiable Hybrid Core & Multiscale Parameterization)**：
   - **NeuralGCM**（Kochkov et al., Nature 2024）：采用可微流体动力学谱变换核心解析计算大尺度绝热运动（平流、重力波），神经网络高效学习亚网格辐射与云水相变；
   - **ClimSim**（Yu et al., NeurIPS 2023）：将全球高分辨率云微物理模拟（SP-CAM）与低分辨率大尺度大气循环解耦，由神经网络充当亚网格对流超参数化替代，实现动力学守恒与高吞吐量并重。

### 维度 4：大语言模型在科学时序中的推理范式 (Role of Reasoning LLMs)
1. **科学推理核心 (Scientific Reasoner)**：如 **SciTS (TimeOmni)**，构建包含天文学、气象学、生物学等 12 个自然科学学科的科学时序指令微调体系，赋予 LLM 对时序曲线的因果推理与假设检验能力。
2. **频域感知上下文增强 (Contextual Enhancer)**：如 **ClimateLLM**，利用快速傅里叶变换提取主导动力学特征，将其作为可学习前缀嵌入通用大语言模型。
3. **地学领域全模态对齐 (Domain Alignment)**：如 **K2**（Deng et al., WSDM 2024）基于 >5.5B token 地球科学语料微调；**GeoChat**（Kuckreja et al., CVPR 2024）实现对地观测高分辨率影像时序的像素级地面定点定位与多轮对话。
4. **自主科学智能体与执行沙盒 (Autonomous Agents & Computation Sandboxes)**：如 **ClimateAgent**（Song et al., 2024）与 **OceanGPT**（Bi et al., ACL 2024），构建深度挂载科学计算生态（`xarray`, `dask`, `metpy`, `obspy`, `oceanbench`）的有状态沙盒，融合自主假设生成、自省纠错回路与物理合理性防护栏（Physical Plausibility Guardrails），实现复杂跨学科研究的端到端自动化。

---

## 3. 权威基准量化对比与深度理论分析 (Benchmarks & Theoretical Insights)

### 3.1 WeatherBench 2 确定性基准对比 (0.25° 分辨率，ECMWF ERA5 验证)

| 模型体系 | 空间分辨率 / 架构 | Day 3 $Z500$ ($\mathrm{m}^2/\mathrm{s}^2$) | Day 3 $T850$ ($\mathrm{K}$) | Day 5 $Z500$ ($\mathrm{m}^2/\mathrm{s}^2$) | Day 5 $T850$ ($\mathrm{K}$) | Day 7 $Z500$ ($\mathrm{m}^2/\mathrm{s}^2$) | Day 7 $T850$ ($\mathrm{K}$) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **ECMWF IFS HRES** | 0.1° / 数值流体预报 | 154.2 | 1.36 | 334.5 | 1.82 | 558.1 | 2.34 |
| **Pangu-Weather** | 0.25° / 3D Earth Transformer | 132.8 | 1.15 | 296.7 | 1.58 | 512.4 | 2.14 |
| **GraphCast** | 0.25° / Multi-Mesh GNN | **128.4** | **1.11** | **289.1** | **1.52** | **507.2** | **2.09** |
| **FuXi (伏羲)** | 0.25° / 级联自回归 Swin | 131.0 | 1.14 | 293.4 | 1.55 | 509.8 | 2.11 |
| **FengWu (风乌)** | 0.25° / 多模态跨时间 Transformer | 130.5 | 1.13 | 291.8 | 1.54 | 511.0 | 2.12 |
| **NeuralGCM (混合动力)** | 1.4° / 可微流体动力学+神经网络 | 148.9 | 1.25 | 312.6 | 1.68 | 535.0 | 2.22 |

> **关键科学发现 (Key Insights)**：
> 1. **全周期超越确定性数值模式**：纯数据驱动基础模型（GraphCast、Pangu-Weather、FuXi、FengWu）在第 3、5、7 天的纬度加权均方根误差 (RMSE) 上全线显著优于世界最顶尖的操作性数值预报模型 ECMWF IFS HRES。例如在第 5 天，GraphCast 将 500 hPa 位势高度 ($Z500$) 误差由数值预报的 334.5 压低至 289.1 $\mathrm{m}^2/\mathrm{s}^2$（降低约 13.6%）。
> 2. **空间离散化带来的优势**：GraphCast 采用的多尺度正二十面体图网格在两极区域保持均匀空间覆盖，相较于经纬度投影网格有效抑制了两极走样，使其在 Day 7 仍保持最佳的确定性得分 ($507.2\ \mathrm{m}^2/\mathrm{s}^2$)。
> 3. **谱能量衰减与混合物理模型的均衡**：尽管纯神经网络在 RMSE 领先，但其在 7 天以上积分时易出现高频波谱能量耗散（产生“平滑模糊”效应）；而 **NeuralGCM** 依托显式流体力学核心，在保持极低物理漂移的同时，在中期气候推演中呈现出无与伦比的长时段物理保真度。

### 3.2 概率扩散与极端事件理论突破 (Diffusion Ensembles vs. MSE Spectral Blur)
传统确定性深度学习模型以均方误差（$L_2$ 损失）为优化目标：
$$\mathcal{L}_{\mathrm{MSE}} = \mathbb{E}_{(\mathbf{x}, \mathbf{y}) \sim p(\mathbf{x}, \mathbf{y})} \left[ \|\mathbf{x} - f_\theta(\mathbf{y})\|_2^2 \right]$$
理论上，其全局最优解为后验条件均值：
$$f^*(\mathbf{y}) = \mathbb{E}_{p(\mathbf{x}|\mathbf{y})}[\mathbf{x}] = \int \mathbf{x} p(\mathbf{x}|\mathbf{y}) d\mathbf{x}$$
由于地球流体动力系统的内禀混沌性（李雅普诺夫时间尺度），当预报时效超过 5 天后，多模态后验分布 $p(\mathbf{x}|\mathbf{y})$ 呈现宽幅多峰分散。此时取条件期望等价于对所有可能的状态轨迹进行线性叠加加权，导致高波数湍流涡旋在积分中相互抵消，高频动能谱 $E(k)$ 发生不可逆的严重谱耗散（造成“模糊平滑”视觉伪影），并系统性抹杀台风中心气压与极端暴雨的重尾分布。

与此相对，**GenCast** 与 **SEEDS** 采用连续时间反向扩散 SDE 进行条件后验采样：
$$d\mathbf{x} = \left[ \mathbf{f}(\mathbf{x}, t) - g(t)^2 \mathbf{s}_\theta(\mathbf{x}, t; \mathbf{y}) \right] dt + g(t) d\bar{\mathbf{w}}$$
直接从真实条件后验 $p(\mathbf{x}|\mathbf{y})$ 中抽取物理真实现象样本。实验证明，扩散集合预报严格保持了柯尔莫哥洛夫 $k^{-5/3}$ 惯性子区能谱斜率，并在连续分级概率评分（CRPS）上全面超越了欧洲中期天气预报中心顶尖的 50 成员操作性集合模式（ECMWF ENS）。

### 3.3 跨学科全景定量评测元表 (Multi-Domain Benchmark Meta-Synthesis)
本综述首次在同一框架下整合了五大跨学科权威基准的量化表现（详见论文 Table III）：
- **大气天气基准 (WeatherBench 2)**：ECMWF IFS HRES 与各大 AI 模型相比，GraphCast、FuXi 与 AIFS 在 3、5、7 天预测中均保持领先。ECMWF 官方自研的 AIFS 模型在 Day 3 $Z500$ 达到 $124.6\ \mathrm{m}^2/\mathrm{s}^2$（IFS 为 152.8），验证了图编码-滑动窗口 Transformer 在业务化运行中的优越稳定性。
- **气候模拟与亚网格物理 (ClimateBench & ClimSim)**：深度卷积与多尺度 Transformer 模拟器将年表面温度 $TAS$ 均方根误差由传统线性模式缩放（Pattern Scaling）的 $0.32\ \mathrm{K}$ 降至 $0.16\ \mathrm{K}$。在 ClimSim 亚网格对流加热率 $dT/dt$ 与增湿率 $dq/dt$ 预测中，多尺度 Transformer 达到 $R^2 \ge 0.79$，有效支持与流体动力核的长时间稳定耦合。
- **全球水文与无测站流域洪涝演进 (Caravan & GlobalFlood)**：在涵盖全球 5,680 个水文站的统一评测中，传统基于物理的全球数值水文模式（GloFAS）的中位数纳什效率系数（NSE）仅为 0.35（Day 1）与 0.26（Day 5）；而融合河道拓扑汇流路由的实体感知 LSTM（EA-LSTM）在 Day 1 达到 0.74，在 Day 5 达到 0.62，实现了对无资料流域（Ungauged Basins）5天预警精度超越传统模式在第0天水平的跨越。
- **全球海洋动力学基准 (OceanBench)**：基于 Mercator GLORYS12 再分析数据，球面傅里叶神经算子与分层 Transformer（如 XiHe）将第 5 天海表面高度异常（SSH）误差由气候态基线的 $0.120\ \mathrm{m}$ 压低至 $0.054\ \mathrm{m}$，海表温度（SST）误差压低至 $0.32\ \mathrm{K}$。
- **全球地震连续波形拾取基准 (SeisBench)**：在 STEAD 与 INSTANCE 跨大洲台网标准化评测中，深度分层 Transformer（SeisT）与残差 U-Net（PhaseNet）将 P 波走时绝对误差降低至 $0.034\ \mathrm{s}$（经典 STA/LTA 为 $0.185\ \mathrm{s}$），震相识别 $F_1$ 分数突破 95.8%。

### 3.4 算力开销、吞吐量与绿色计算能耗评测 (Computational Efficiency & Green NWP)
本综述在 Table IV 中系统量化对比了操作性数值天气预报（NWP）与各大数据驱动基础模型的资源与能耗消耗：
1. **能耗降维打击（3 至 5 个数量级削减）**：ECMWF IFS HRES 0.1° 高分辨率数值模式在超算集群（如 Atos Sequana，使用 3,500+ CPU 核心）上完成一次 10 天预报需耗费约 50 分钟（3,000 秒），耗电约 **$180\ \mathrm{kWh}$**；而 51 个成员的操作性集合预报耗电高达 **$2,200\ \mathrm{kWh}$**。与之对比，数据驱动模型在单块商用 GPU/TPU 上即可在秒级完成（FourCastNet $0.25\ \mathrm{s}$，Pangu-Weather $2.0\ \mathrm{s}$，FuXi $6.0\ \mathrm{s}$，AIFS $20.0\ \mathrm{s}$），单次预报能耗降至 **$0.00015\ \mathrm{kWh}$ 至 $0.005\ \mathrm{kWh}$**。
2. **显存墙瓶颈与架构权衡**：基于全空间图消息传递的 GraphCast 在自回归单步中需维护复杂的网格拓扑张量缓冲区，峰值显存达 $28.5\ \mathrm{GB}$ HBM；而采用滑动窗口自注意力的 AIFS（$22\ \mathrm{GB}$）与谱域卷积的 SFNO（$10\ \mathrm{GB}$ 级）有效打破显存墙限制，具备更佳的工业级边缘端部署可行性。
3. **预训练摊销与全球科研普惠**：虽然训练一个千亿 Token 级大气基础模型需消耗 16–40 GPU/TPU 周，但由于推理加速比达到 $50\times$ 至 $12,000\times$，模型在上线运行数百次后即可全面收回预训练算力成本，使不具备数千万美元超算中心的发展中国家气象水文机构能够运行高精度全球预警。

### 3.5 自主多智能体科学推理 DAG 闭环工作流 (Multi-Agent Reasoning DAG)
为实现真正的自主科学发现，本综述提炼了基于有状态执行沙盒的多智能体协同拓扑（见论文 Fig. 6）：
- **规划智能体 (Plan-Agent)**：将抽象自然科学目标（如“分析 2024 年地中海海洋热浪诱因并检验涡动能耗散”）拓扑拆解为有向无环图（DAG）；
- **数据智能体 (Data-Agent)**：对接 CDS / USGS / GLORYS 分布式数据接口，基于 `xarray` 和 `dask` 进行分块延迟加载（Chunked Out-of-Core IO）；
- **编码与执行智能体 (Coding-Agent)**：在受控 REPL 沙盒中调用 `MetPy`、`ObsPy`、`PyTorch` 等科学求解器生成诊断结果；
- **自省纠错回路 (Self-Correction Loop)**：解析运行时 Traceback 异常，针对地学数据特有的坐标反转、360天气候历法与气压单位错配进行自动反射重构；
- **审判智能体与物理防护栏 (Critic-Agent Guardrails)**：在报告生成前严格校验质量守恒、降水非负性（$P \ge 0$）与量纲一致性，杜绝大模型科学幻觉。

---

## 4. 关键挑战与未来前沿方向 (Open Challenges & Frontiers)

1. **多模态连续物理统一分词器 (Unified Continuous Physical Tokenization)**：打破结构化规整网格（ERA5）、稀疏离散测站（雨量计、水文计、地震台网）与异构非规则遥感影像（Sentinel/Landsat）的表征边界，构建具备空间连续内插、时间自适应采样与物理守恒先验的通用物理分词架构。
2. **硬性物理守恒约束与极端极值可靠性标定 (Hard Physical Invariants & Extreme Event Calibration)**：在网络底层深度嵌入连续流形几何算子（如球面谐波 SFNO）与流体动力保真核，解决深度学习在极端台风、暴雨重尾事件中的欠拟合与物理违背缺陷。
3. **高效多尺度可扩展扩散集合系统 (Scalable Probabilistic Diffusion Ensembles)**：降低扩散反向采样求解高维地球物理场时的计算开销，融合流匹配（Flow Matching）与一致性模型（Consistency Models），实现秒级生成全球数十个高保真物理集合成员。
4. **自主科学推理智能体沙盒与闭环验证 (Autonomous Scientific Discovery Sandboxes & Verification Loops)**：推动大语言模型从简单 API 调用迈向挂载全套科学计算生态（`xarray`, `metpy`, `dask`, `obspy`）的有状态沙盒，建立具备假设生成、自动代码推演、物理自检纠错与实验闭环验证的自主科学探索助手。
