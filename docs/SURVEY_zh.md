# 科学多模态时序大模型与科学推理大模型综述（中文概述）

**论文全称**：*Foundation Models and Reasoning LLMs for Scientific Multimodal Time Series: A Survey*  
**维护机构**：Antigravity Autonomous Research Loop (`lihuirui/awesome-scientific-time-series-foundation-models-survey`)  
**当前版本**：v9.0 (迭代 9 - 跨模态多星座卫星遥感时序基础模型、异步海气-海冰耦合多智能体地球系统仿真器、次网格微物理参数化与机器精度严格守恒闭环，收录 77 篇严谨学术成果)  
**更新日期**：2026-09-27  
**论文正文**：[`paper/main.pdf`](file:///workspace/survey-sci-ts/paper/main.pdf) (IEEEtran 双栏, 32 页, 包含 8 幅高分辨率出版级图表与 7 个全景对比表格)

---

## 1. 综述背景与研究动机 (Introduction & Motivation)

在过去十年中，深度学习在通用时间序列预测与时空数据挖掘（如城市交通、金融行情、人体姿态）取得了长足进步。然而，当技术延伸至**自然科学与地球物理系统**（大气天气预报、百年轻慢气候演变、流域水文与极端洪涝、海洋多尺度动力学、地热与深部碳封存、对地观测与卫星遥感、地震台网波形监测与日地空间物理、极地冰冻圈演变）时，传统深度时序模型遭遇深刻瓶颈：

1. **多物理模态极端异构**：科学时序跨越离散不规则测站观测（雨量站、水文计、地震台网）、连续空间再分析网格场（ECMWF ERA5, MERRA-2）、多光谱/高光谱卫星影像序列（Sentinel-1/2, Landsat）、连续物理张量波形与跨圈层通量数据。
2. **多尺度连续动力学**：物理现象在空间上跨越米级局部湍流至数万公里全球环流；时间尺度跨越毫秒级（地震破裂波形）、小时/天级（强对流降水与台风路径）、至百年/千年级（温室气体驱动的气候变暖）。
3. **物理守恒律与一致性约束**：经典自回归神经网络易发生“物理幻觉”（违背质量守恒、动量守恒或能量守恒），在长时段循环推演中出现累积谱衰减、过度平滑或极端事件失真。
4. **科学推理与智能体决策**：随着大语言模型（LLM）的爆发，如何使智能体深度理解物理时序中的空间依赖与动力演进，具备科学假设生成、物理参数反演、多工具编排与闭环科学推理（Scientific Reasoning）能力，成为人工智能驱动科学研究（AI for Science）的核心命题。

本综述系统梳理了 2021 年至今自然科学领域的 **科学多模态时序基础模型（Scientific Multimodal Time Series Foundation Models）** 与 **科学时序推理大语言模型（Scientific Reasoning LLMs / Multi-Agent Systems）**，收录并深度解构了 77 篇经过学术 API 严格验证的标志性研究。

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
   - 极地冰冻圈与海冰动力学  - 高阶张量分解与量子神经算子
   - 空间天气与太阳物理      - 动态波长超网络 (DOFA)
```

### 维度 1：自然科学领域与多模态数据源 (Scientific Domains & Modalities)
- **全球天气预报 (Weather Forecasting)**：以 ECMWF ERA5 为主流预训练语料，包含多层三维大气动力场（位势高度 $Z$、温度 $T$、风场 $U/V$、比湿 $Q$），模型分辨率从 0.25° (~28 km) 逐步推进至公里级。代表工作：Pangu-Weather、GraphCast、FourCastNet、FuXi、FengWu、Aurora、Prithvi WxC、Stormer（随机动态时间 Patching）、ExtremeCast（极值理论驱动的重尾天气灾害预报）。
- **气候模拟与长期预估 (Climate Modeling)**：面向百年尺度演化，模拟全球表面温度 ($TAS$)、区域降水量 ($PR$) 对温室气体与气溶胶排放情景的响应。代表基准与模型：ClimateBench、ClimaX、ACE（JAMES 2024，全球干空气质量与全柱水汽严格守恒的超高吞吐气候仿真基石）、ClimSim（NeurIPS 2023 杰出论文，涵盖 5.7 亿高分辨率垂直柱样本的混合多尺度物理参数化基准）、AC-NN（PRL 2021，机器精度解析硬约束对流能量与水守恒神经网络）。
- **对地观测与多模态遥感 (Earth Observation & Remote Sensing)**：融合 Sentinel-1 (SAR)、Sentinel-2 (多光谱)、Landsat 与高程 DEM 的多时相、多波长序列。代表工作：SatMAE、Presto、Galileo、DOFA（动态波长超网络实现任意光学-SAR-热红外模态即插即用）、EarthPT、CROMA（NeurIPS 2023，联合自监督与交叉注意力对齐的光学-雷达多模态基础模型）、AnySat（CVPR 2025 Highlight，跨越 0.2m 至 500m 超大空间分辨率跨星座通用基础模型）。
- **水文流域与洪涝演进 (Hydrology & Streamflow)**：跨越全球数千个水文流域。代表工作：Google Global Flood、Caravan（涵盖全球 6,830 个集水区的标准化水文基准）。
- **海洋动力学与流场 (Oceanography)**：模拟海表面高度异常 (SSH)、海表温度 (SST) 与中尺度涡旋演化。代表工作：XiHe、OceanGPT（融合海洋动力学与具身轨迹推理的专业大模型）、OceanBench（NeurIPS 2025 全球海洋对地观测与流场多任务基准平台）、DLESyM（AGU Advances 2025，全球多年代全耦合海气多智能体仿真器）、SamudrACE（GRL 2025，三维大洋环流基础模型与物理通量边界耦合器）。
- **极地冰冻圈与海冰动力学 (Polar Cryosphere & Sea Ice Dynamics)**：模拟北极与南极海冰浓度（SIC）、厚度、漂移速度矢量以及冰架融化。融合 Sentinel-1 SAR、AMSR2 微波辐射计与跨年代 CMIP6 模拟序列。代表工作：IceNet（Nature Communications 2021，超越 ECMWF 季节模式 SEAS5 的概率海冰预测系统）、IceBench（arXiv 2025，包含多年代卫星遥感与动力耦合模式的极地海冰全任务基准平台）。
- **地震学与地球物理波形 (Seismology & Waveforms)**：利用高频连续三分量台网波形实现微震检测与走时拾取，以及连续弹性动力学波场模拟。代表工作：SeisT、QuakeFlow、SeisBench（SRL 2022 全球多区域标准化地震机器学习基准与开源生态）、WaveFNO（SRL 2021 求解非均匀地壳弹性波方程的傅里叶神经算子）。
- **日地物理与空间天气 (Space Weather & Solar Physics)**：利用 SDO 极紫外 (EUV) 影像与光球磁场时序，实现太阳耀斑预测。代表工作：SurffNet。
- **通用跨学科科学时序 (Cross-Domain Scientific Time Series)**：突破领域孤岛，实现多学科时序的跨域预训练与零样本迁移。代表工作：UniTS（NeurIPS 2024 统一多任务时序大模型）、MOMENT（ICML 2024 开源通用时序基础模型族）。

### 维度 2：核心骨架网络与空间离散化 (Core Backbones & Discretization)
- **3D 空间球形 Transformer**：如 **Pangu-Weather** 引入针对地球几何特征的高程感知三维注意力，结合多时步层级自回归；**Aurora** 则利用 3D Perceiver 架构将不同垂直分辨率与变量压缩为潜在空间表示。
- **多重网格图神经网络 (Multi-Mesh GNNs)**：如 **GraphCast** 构建从正二十面体 (Icosahedral) 递归细分的多层空间立体图网格，消息在网格层次间双向传递，彻底避免传统等经纬度网格在南北两极的网格奇异性。
- **球面傅里叶神经算子 (SFNO / AFNO)**：如 **SFNO**（Bonev et al., ICML 2023）在二维球面上严格引入离散球面调和变换（Spherical Harmonics $Y_\ell^m$），在谱域实现频域卷积，具备天然的连续空间表示与 $\mathrm{SO}(3)$ 球面旋转等变性；**FourCastNet** 则在展平网格上采用自适应傅里叶神经算子 (AFNO)。
- **跨模态掩码自编码器与尺度自适应架构 (Multimodal MAE & Scale-Adaptive JEPA)**：如 **CROMA** 将对比学习与 2D-ALiBi 交叉注意力 MAE 结合，**AnySat** 利用联合嵌入预测（JEPA）与连续尺度调制突破 0.2m–500m 超宽地面采样距离（GSD）；**Galileo**、**Presto** 与 **SatMAE** 实现时间-空间-波段联合掩码自回归重建。
- **动态波长超网络 (Wavelength Hypernetworks)**：如 **DOFA**（Xiong et al., CVPR 2024），引入连续波长超网络动态生成视觉骨干的卷积/注意力权重，打破多传感器波段对齐壁垒。
- **异步多速率耦合积分与地球系统多智能体求解器 (Asynchronous Coupled Solvers)**：如 **DLESyM** 与 **SamudrACE**，在大气快变过程（小时级）与深海慢变过程（月/年级）之间引入多速率可微时间步进与界面通量守恒耦合器。
- **统一时序补丁化与跨域分词 (Universal Time Series Patching & Tokenization)**：如 **UniTS** 与 **MOMENT** 采用统一时间步长自适应分词与跨变量掩码，**Stormer** 引入空间随机 Patching 破坏空间网格的固定归纳偏置，显著缓解自回归误差积累。
- **连续生成式扩散集合预报 (Generative Score-Based Diffusion Ensembles)**：如 **GenCast** 与 **SEEDS**（Li et al., Science Advances 2024），利用条件随机微分方程（SDE）与得分匹配（Score Matching），直接从真实物理后验中采样高分辨率集合成员，彻底克服确定性自回归模型的谱能量模糊。
- **高阶张量分解与量子参数化神经算子 (Tensor-Decomposed & Quantum Neural Operators)**：如 **MG-TFNO**（Kossaifi et al., 2024）利用 Tucker 因子分解与张量网络对高维傅里叶谱核进行降维分解，参数压缩比达 $150\times$ 以上，突破显存墙实现单 GPU 上 $1024^2$ 多尺度湍流解算；**WaveFNO**（Yang et al., 2021）针对复杂地下介质弹性动力学波动方程构建谱域连续求解；**PHQFNO**（Marcandelli et al., 2025）引入保哈密顿酉参数化量子线路（PQC）与经典神经算子混合纠缠，展现量子优势对复杂流体演化的潜在加速。

### 维度 3：物理规律融合层次 (Physics Integration Levels)
1. **纯数据驱动 (Purely Data-Driven)**：完全依赖数据规模与模型容量隐式拟合物理场演进。
2. **软物理损失惩罚 (Soft Physics Loss Penalties)**：在损失函数中显式加入动能守恒、散度为零约束或质量通量惩罚项（如 FengWu、FourCastNet）。
3. **硬几何、辛结构与解析零空间投影守恒 (Hard Invariants & Analytic Projections)**：
   - 几何与辛守恒结构（如 SNO、LPNets）：严格保持相空间体积与所有李-泊松卡西米尔不变量；
   - 解析零空间硬投影层（如 **AC-NN**）：将物理平衡方程 $\mathbf{A} \Delta \mathbf{y} = \mathbf{b}$ 转化为显式零空间投影算子 $\mathbf{P} = \mathbf{I} - \mathbf{A}^T (\mathbf{A}\mathbf{A}^T)^{-1}\mathbf{A}$，使能量与水分守恒残差达到**机器浮点精度（$< 10^{-15}$）**；
   - 全局积分质量修正器（如 **ACE**）：在每步自回归积分中精确恢复干空气总质量与全柱水汽积分闭环。
4. **混合神经-偏微分方程可微动力核与全耦合多智能体系统 (Differentiable Hybrid Core & Coupled Earth Systems)**：
   - **NeuralGCM**（Kochkov et al., Nature 2024）：采用可微流体动力学谱变换核心解析计算大尺度绝热运动（平流、重力波），神经网络高效学习亚网格辐射与云水相变；
   - **ClimSim**（Yu et al., NeurIPS 2023）：将全球高分辨率云微物理模拟（SP-CAM）与低分辨率大尺度大气循环解耦，由神经网络充当亚网格对流超参数化替代，实现动力学守恒与高吞吐量并重；
   - **DLESyM**（Cresswell-Clay et al., AGU Advances 2025）：端到端多圈层全耦合多智能体系统，通过界面通量闭环实现 100 年稳定模拟。

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
本综述首次在同一框架下整合了跨越七大物理学科权威基准的量化表现（详见论文 Table III）：
- **大气天气基准 (WeatherBench 2)**：ECMWF IFS HRES 与各大 AI 模型相比，GraphCast、FuXi 与 AIFS 在 3、5、7 天预测中均保持领先。ECMWF 官方自研的 AIFS 模型在 Day 3 $Z500$ 达到 $124.6\ \mathrm{m}^2/\mathrm{s}^2$（IFS 为 152.8），验证了图编码-滑动窗口 Transformer 在业务化运行中的优越稳定性。
- **气候模拟与亚网格物理 (ClimateBench & ClimSim)**：深度卷积与多尺度 Transformer 模拟器将年表面温度 $TAS$ 均方根误差由传统线性模式缩放（Pattern Scaling）的 $0.32\ \mathrm{K}$ 降至 $0.16\ \mathrm{K}$。在 ClimSim 亚网格对流加热率 $dT/dt$ 与增湿率 $dq/dt$ 预测中，多尺度 Transformer 达到 $R^2 \ge 0.79$，有效支持与流体动力核的长时间稳定耦合。
- **全球水文与无测站流域洪涝演进 (Caravan & GlobalFlood)**：在涵盖全球 5,680 个水文站的统一评测中，传统基于物理的全球数值水文模式（GloFAS）的中位数纳什效率系数（NSE）仅为 0.35（Day 1）与 0.26（Day 5）；而融合河道拓扑汇流路由的实体感知 LSTM（EA-LSTM）在 Day 1 达到 0.74，在 Day 5 达到 0.62，实现了对无资料流域（Ungauged Basins）5天预警精度超越传统模式在第0天水平的跨越。
- **全球海洋动力学基准 (OceanBench)**：基于 Mercator GLORYS12 再分析数据，球面傅里叶神经算子与分层 Transformer（如 XiHe）将第 5 天海表面高度异常（SSH）误差由气候态基线的 $0.120\ \mathrm{m}$ 压低至 $0.054\ \mathrm{m}$，海表温度（SST）误差压低至 $0.32\ \mathrm{K}$。
- **全球地震连续波形拾取基准 (SeisBench)**：在 STEAD 与 INSTANCE 跨大洲台网标准化评测中，深度分层 Transformer（SeisT）与残差 U-Net（PhaseNet）将 P 波走时绝对误差降低至 $0.034\ \mathrm{s}$（经典 STA/LTA 为 $0.185\ \mathrm{s}$），震相识别 $F_1$ 分数突破 95.8%。
- **极端灾害重尾预报基准 (ExtremeCast EVT Benchmark)**：在 99% 分位数降水与极端阵风中，结合广义极值损失 Exloss 与 ExBooster 的模型将临界成功指数（CSI）提升至 0.278（传统回归为 0.142），且不增加常规预测的均方根误差。
- **极地冰冻圈海冰预测基准 (IceNet & IceBench)**：在北极 6 个月季节海冰范围推演中，IceNet 的非精确重叠误差（IIEE）相比 ECMWF SEAS5 降低 30% 以上；多源微波辐射与雷达融合使海冰漂移速度场相关性提升至 0.78。

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

### 3.6 神经变分数据同化与传感器-网格反演 (Neural Data Assimilation & Sensor Inversion)
传统大模型依赖国家级超算中心预先生成的离线网格化再分析场（ERA5）。本综述系统梳理了将原始非结构化、异步、稀疏传感器观测直接反演为物理协调网格场的最新同化架构（见论文 Section 4 与 Fig. 5）：
1. **展开式神经四维变分求解器 (Unrolled Neural 4D-Var)**：
   - 传统 4D-Var 求解依赖复杂庞大的切线性与伴随模式代码（Adjoint Models），计算开销占超算中心 80% 以上。
   - **4DVarNet**（Fablet et al., JAMES 2021）将变分极小化目标映射为循环展开神经网络：
     $$\mathbf{x}_0^{(i+1)} = \mathbf{x}_0^{(i)} - \boldsymbol{\Gamma}_\theta \left( \nabla_{\mathbf{x}_0} \mathcal{J}(\mathbf{x}_0^{(i)}), \mathbf{h}^{(i)} \right)$$
     利用神经网络自适应学习最优下降方向与动态背景误差协方差，在卫星沿轨测高数据反演中成功重建精细中尺度海洋涡旋。
   - **FengWu-4DVar**（Xiao et al., 2023）利用 FengWu 大气 Transformer 的全局可微性，将 24 小时同化窗内的真实异步探空与卫星辐射观测残差直接反向传播，实现初值分析与动力模式的端到端联合优化，同化速度由小时级提速至秒级。
2. **生成式得分扩散数据同化 (Score-Based & Diffusion DA)**：
   - **DiffDA**（Huang et al., 2024）与 **Score-based DA**（Rozet & Louppe, NeurIPS 2023）将同化形式化为稀疏物理约束下的条件生成反演：
     $$d\mathbf{x} = \left[ \mathbf{f}(\mathbf{x}, t) - g(t)^2 \left( \nabla_\mathbf{x} \log p_t(\mathbf{x}) + \nabla_\mathbf{x} \log p_t(\mathbf{y} \mid \mathbf{x}) \right) \right] dt + g(t) d\bar{\mathbf{w}}$$
     利用 Tweedie 公式解析推导观测似然梯度，无需手动假定高斯背景误差，即可在天气尺度直接从稀疏测站反演全局高保真大气锋面。

### 3.7 跨模态跨几何隐空间对齐三大范式 (Cross-Modal Latent Alignment Paradigms)
针对卫星高光谱、SAR 雷达、离散测站与连续网格场的几何差异，本综述提炼出三大多模态融合范式（见论文 Fig. 5）：
1. **策略 A：早期异构 Patch 投影与 4D 连续时空编码**（如 SatMAE, Presto, Galileo），引入基于地理坐标与物理时间的连续傅里叶位置编码 $\mathbf{PE}(x, y, z, t)$；
2. **策略 B：潜变量交叉注意力瓶颈 (Latent Cross-Attention Bottleneck)**（如 Aurora, SkySense 1.9B），设计固定容量的潜变量查询组 $\mathbf{Z} \in \mathbb{R}^{M \times D}$，通过交叉注意力吞吐任意密度的传感器 Token，实现计算复杂度与观测点数解耦；
3. **策略 C：连续物理波长动态超网络 (Dynamic Wavelength Hypernetworks)**（如 DOFA, AnySat），基于物理波长连续嵌入 $\lambda \in [400\text{ nm}, 14{,}000\text{ nm}]$ 动态生成卷积与线性投影权重，实现光学与雷达波段的零样本即插即用适配。

### 3.8 业务化长时漂移、概念漂移与极端气候异常应急协议 (Operational Reliability & Fail-Safe Protocols)
根据 ECMWF 官方首个业务化统计评估报告（Ben-Bouallegue et al., BAMS 2024），纯数据驱动大模型在投入真实业务预报生产中存在四大现实挑战与应对协议：
1. **业务分析初值与历史再分析的分布失配 (Analysis Discrepancy)**：在再分析（ERA5，含12小时对称双向观测窗口）上预训练的模型在直接输入截断时延的业务化初值（Operational Analysis）时，第 0 步误差会出现 10%--15% 的异常跳升，需引入业务化在线微调或自适应初值校正缓冲层。
2. **自回归长步长递推的能谱衰减与平滑效应**：$L_2$ 损失在 5 天以上外推时逐步丢失高频动能，致使锋面与局部大风结构模糊，需引入条件扩散扰动或自回归级联网络进行能谱补偿。
3. **未见历史极端事件中的物理幻觉风险 (Climate Non-Stationarity)**：面对全球变暖背景下未曾被历史数据覆盖的极端破纪录热穹顶、爆发性气旋或极涡崩溃，纯数据模型可能因支撑集外（Out-of-Distribution）导致动能或比湿不守恒，甚至出现负降水。
4. **混合双轨并行与安全应急回退机制 (Hybrid Blending & Fail-Safe Handoff)**：业务气象局确立了 AI 模式（如 AIFS）与经典物理数值模式（IFS HRES）并行运行机制，实时监控物理残差与守恒量；当扩散集合离散度或物理偏离度触发阈值时，自动平滑无缝切换回经典数值动力学求解器。

### 3.9 连续-离散物理不变量与流形几何深度学习 (Continuous-Discrete Physics Invariants & Geometric Deep Learning)
传统大模型在固定离散步长（如 $\Delta t = 6\text{ h}$）下进行自回归滚动推演，在数十个时间步后不可避免地积累离散截断误差与物理守恒偏离。
1. **连续流场神经常微分方程 (Neural ODE Flow & Advection PDE)**：
   **ClimODE**（Verma et al., ICLR 2024）突破了离散自回归架构的固有局限，将大气演化建模为连续动力系统。通过神经网络参数化速度场 $\mathbf{v}_\theta(\mathbf{x}, t)$，利用连续性方程显式约束质量守恒：
   $$\frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \mathbf{v}) = 0, \quad \frac{d\mathbf{z}(t)}{dt} = \mathbf{f}_\theta(\mathbf{z}(t), t)$$
   配合伴随敏感度法（Adjoint Sensitivity Method）进行反向传播，实现任意连续时间分辨率的无缝积分与能量守恒推演。
2. **球面黎曼流形与 $\mathrm{SO}(3)$ 旋转群对称性**：
   在球形几何体 $\mathbb{S}^2$ 上，**SFNO** 与 **ClimODE** 引入黎曼切空间度量张量 $g_{ij}$ 与离散球谐变换，确保模型在全局坐标旋转与坐标系变换下满足严格的李群旋转等变性。这种内嵌的几何物理先验使得 ClimODE 在仅有 0.3M 超轻量参数下即可逼近数千万参数基线模型的预报精度，展现了物理不变量对网络容量的巨大杠杆效应。

### 3.10 亚公里对流尺度仿真与生成式超分辨率降尺度 (Sub-Kilometer Convective-Scale Emulation & Generative Downscaling)
全球 0.25° 网格（~28 km）对于局地极端对流暴雨、突发下击暴流与超级单体龙卷风预警存在尺度盲区。近年来，亚公里级高分辨率临近预报与生成式降尺度取得里程碑式突破：
1. **深度生成雷达临近降水预警 (DGMR)**：
   **DGMR**（Ravuri et al., Nature 2021 / DeepMind）首次将时空生成对抗网络（GAN）应用于 1 km 分辨率、5–90 分钟的雷达反射率外推。通过双重鉴别器（空间内容与时间动态鉴别器）联合惩罚，在高阈值降水（$>8\ \mathrm{mm/h}$）下的临界成功指数（CSI）大幅超越经典数值光流法（PySTEPS）与循环卷积网络（ConvLSTM），并在空间功率谱密度（PSD）分析中首次彻底解决了传统回归模型的边缘模糊与能量耗散。
2. **多模态稠密对流尺度预报 (MetNet-3)**：
   **MetNet-3**（Andrychowicz et al., Science 2024 / Google）将空间雷达网、地面雨量站、GOES 静止卫星红外时序与数值模式物理先验深度对齐，在 1 km 网格下将强对流精准预报时效延伸至 24 小时，为城市应急防汛提供了高频（2 分钟级更新）的连续概率预报。
3. **残差扩散生成降尺度 (CorrDiff)**：
   **CorrDiff**（Mardani et al., IEEE TGRS 2024 / NVIDIA）基于条件扩散概率模型，将 25 km 低分辨率粗网格场实时超分辨率至 2 km，利用残差修正流精确捕获局地地形强迫抬升与非静力平衡中小尺度湍流，单次降尺度推理能耗比高分辨率物理数值模拟器（如 WRF）降低三个数量级（能耗降至 $0.005\ \mathrm{kWh}$）。

### 3.11 闭环自主科学发现与科研编码推理基准 (Closed-Loop Autonomous Scientific Discovery & Empirical Coding Benchmarks)
大语言模型正从“代码助手”向“自主完成全生命周期科学研究”跃迁：
1. **端到端自主科研闭环智能体 (The AI Scientist)**：
   **The AI Scientist**（Lu et al., Sakana AI / Oxford 2024）构建了全球首个全流程科研智能体生态：包含自主科学假设头脑风暴、文献检索（Semantic Scholar API 过滤去重）、实验代码自主编写与在 PyTorch 环境中的沙盒执行、结果可视化、自动撰写完整学术规范 LaTeX 论文（含章节结构与正文实验图表编排）、以及基于大语言模型的自主同行评审（Automated Reviewing Loop）。端到端单篇全自动论文产生成本低于 15 美元，开启了科学智能体规模化探索的新范式。
2. **高阶科学编码与数理推导基准 (SciCode)**：
   **SciCode**（Tian et al., ICML 2024）针对复杂物理科学与偏微分方程求解构建了最严苛的可执行基准，覆盖凝聚态物理、理论天体物理、量子化学等领域的 338 个多步数理子问题与 65 步因果长程依赖。在严格的数值单元测试下，顶级前沿模型（GPT-4o 与 Claude 3.5 Sonnet）的端到端完全解决率不足 40%，揭示了大模型在处理跨尺度物理解算与保真度数值积分时依然存在深层认知壁垒。

### 3.12 极值理论（EVT）与重尾物理损失（Extreme Value Theory & Heavy-Tailed Uncertainty Quantification）
针对百年一遇特大暴雨、超级气旋、破坏性极端阵风等重尾灾害，传统对称 $L_2$ 损失由于趋向条件后验均值 $\mathbb{E}[\mathbf{y}|\mathbf{x}]$，导致灾害峰值严重“幅值削平”。
1. **广义极值理论与 Fréchet 尾分布**：
   根据 Fisher-Tippett-Gnedenko 定理，物理场最大值极限分布服从广义极值分布（GEV）：
   $$G(z) = \exp\left\{ - \left[ 1 + \xi \left( \frac{z - \mu}{\sigma} \right) \right]^{-1/\xi} \right\}$$
   在极端降水与台风风速中，尾指数 $\xi > 0$（Fréchet 重尾分布），呈现明显的幂律衰减特征。
2. **Exloss 非对称极值损失与 ExBooster 扰动增强 (ExtremeCast)**：
   **ExtremeCast**（Xu et al., 2024）提出了结合极值理论的 Exloss 损失函数：
   $$\mathcal{L}_{\mathrm{Ex}}(\hat{\mathbf{y}}, \mathbf{y}) = \|\hat{\mathbf{y}} - \mathbf{y}\|_2^2 + \lambda \sum_{i} \mathbf{1}_{\{y_i > u\}} \cdot w(y_i) (\hat{y}_i - y_i)^2$$
   其中 $u$ 为基于广义帕累托分布（GPD）确定的极值阈值，$w(y_i) \propto (y_i - u)^\xi$ 为重尾自适应权重。结合测试阶段的极值扰动增强模块 ExBooster，模型在 99% 分位数极端天气下的临界成功指数（CSI）从 0.142 飙升至 0.278（提升近 100%），同时保持天气尺度均方根误差稳定，突破了传统 AI 气象模型“报得准常规、报不准极值”的结构性瓶颈。

### 3.13 高阶张量分解与量子-经典混合神经算子 (High-Order Tensor Operators & Quantum Parameterized Circuits)
在三维高分辨率地球物理动力学（如三维湍流、地震弹性动力波场反演）中，稠密傅里叶神经算子（FNO）的谱权重张量 $\mathcal{W} \in \mathbb{C}^{K_1 \times K_2 \times K_3 \times d_{\mathrm{in}} \times d_{\mathrm{out}}}$ 遭遇严重的显存爆炸限制。
1. **多重网格张量化傅里叶神经算子 (MG-TFNO)**：
   **MG-TFNO**（Kossaifi et al., 2024）引入高阶 Tucker 张量分解与张量网络压缩：
   $$\mathcal{W} = \mathcal{G} \times_1 \mathbf{U}^{(1)} \times_2 \mathbf{U}^{(2)} \times_3 \mathbf{U}^{(3)} \times_4 \mathbf{U}^{(4)} \times_5 \mathbf{U}^{(5)}$$
   将谱权重参数量压缩 $150\times$ 至 $300\times$，并在多重网格层级间实现空间几何自适应传递。在 Navier-Stokes 多尺度湍流解算中，在单张商用 GPU 上即可直接处理 $1024^2$ 网格，推理速度超越经典伪谱求解器两个数量级。
2. **复杂弹性介质波动力学求解 (WaveFNO)**：
   **WaveFNO**（Yang et al., SRL 2021）针对非均匀地壳中强各向异性速度场，求解连续弹性动力学二阶双曲偏微分方程：
   $$\rho \frac{\partial^2 \mathbf{u}}{\partial t^2} = \nabla \cdot \boldsymbol{\sigma} + \mathbf{f}, \quad \boldsymbol{\sigma} = \mathbf{C} : \boldsymbol{\varepsilon}(\mathbf{u})$$
   突破了有限差分与有限元网格剖分的 Courant-Friedrichs-Lewy (CFL) 稳定性时间步长限制，实现跨震源、跨频带波场走时的瞬时高保真正演。
3. **保哈密顿参数化量子神经算子 (PHQFNO)**：
   **PHQFNO**（Marcandelli et al., 2025）构建了由变分酉参数化量子线路（PQC）$U(\boldsymbol{\theta}) = \prod_{l=1}^L \exp\left( -i \theta_l H_l \right)$ 与傅里叶谱算子交替纠缠的混合架构，在量子比特态空间中模拟连续流体演化的酉时间演化，从理论与小规模模拟上验证了量子张量算子在强非线性物理流形上的表达潜力。

### 3.14 极地冰冻圈与海冰多模态动力学基准 (Polar Cryosphere & Sea Ice Dynamics Benchmarking)
全球极地冰冻圈是调控全球大洋热盐环流与地球反照率能量平衡的关键“冷源”，但由于极夜、多云雾及极端严寒，传统实地观测极端稀缺，遥感观测存在严重的盲区与噪声。
1. **概率海冰季节预测系统 (IceNet)**：
   **IceNet**（Andersson et al., Nature Communications 2021 / British Antarctic Survey）开创了结合大尺度动力气候模拟（CMIP6 跨年代推演）与极地卫星遥感时序（AMSR2 微波辐射计、OSI-SAF）的混合预训练体系。采用多尺度残差 U-Net 输出泛北极海冰密集度（SIC）在未来 6 个月的全概率分布，预测海冰边缘非精确重叠误差（IIEE）相比 ECMWF 季节数值预报模式 SEAS5 降低超 30%，在极值暖季融化预警中展现出强大的鲁棒性。
2. **极地多任务综合基准平台 (IceBench)**：
   **IceBench**（Taleghan et al., 2025）构建了涵盖海冰密集度（SIC）、海冰漂移速度矢量场（$u_i, v_i$）与多源微波散射计数据的跨年代综合评估基准平台。跨架构评测揭示：引入多传感器跨模态融合（微波辐射计 + SAR 反向散射）可将海冰短期漂移追踪相关系数由 0.42 提升至 0.78，为极地航道通航安全与极区气候反馈研究奠定了坚实的基准支撑。

### 3.15 地热能源与地下碳封存多相流大模型 (Geo-Energy & Multiphase Carbon Sequestration Foundations)
深地多孔介质渗流是地热开采、地下储氢与地质碳封存（GCS）的核心动力学基础。深部流体演化受强非线性多相达西-布林克曼（Darcy-Brinkman）方程支配：
$$\phi(\mathbf{x}) \frac{\partial (\rho_\alpha S_\alpha)}{\partial t} + \nabla \cdot (\rho_\alpha \mathbf{u}_\alpha) = q_\alpha, \quad \mathbf{u}_\alpha = -\frac{k_{r\alpha}(S_\alpha) \mathbf{K}(\mathbf{x})}{\mu_\alpha} \left( \nabla p_\alpha - \rho_\alpha \mathbf{g} \right)$$
其中 $\alpha \in \{\text{CO}_2, \text{brine}\}$ 为超临界二氧化碳与盐水两相，$\mathbf{K}(\mathbf{x})$ 为具有极强空间异质性的渗透率张量。传统数值油藏模拟器（如 CMG GEM, TOUGH2）解算单次 30 年三维羽流迁移需数小时至数天。
1. **多尺度 U-Net 增强傅里叶神经算子 (U-FNO)**：
   **U-FNO**（Wen et al., Advances in Water Resources 2022）针对传统 FNO 在非连续相饱和度激波前缘出现的高频吉布斯振荡（Gibbs Ringing）问题，创新性地将多尺度空间 U-Net 跳跃连接与频域傅里叶卷积相融合。在 30 年 $\text{CO}_2$ 羽流运移与压力积聚预测中，U-FNO 将相饱和度 RMSE 压低至 **0.028**，羽流轮廓 IoU 达到 **0.91**，相比商业数值模拟器实现超 **$10{,}000\times$ 加速**，且全域质量守恒误差控制在 0.8% 以内。
2. **全物理热力学状态方程深地建模套件 (CCSNet)**：
   **CCSNet**（Wen, Hay, and Benson, Advances in Water Resources 2021）针对工业级碳封存中超临界流体跨温压相变特性，将深度算子与数据驱动真实热力学状态方程（EOS）紧密耦合，支持在毫秒级时间内评估 50 年尺度下的结构捕获、残余毛细捕获与溶解捕获效率，为碳封存选址与注气方案动态优化提供了革命性工具。
3. **复杂断层与非欧几何流形求解 (Geo-FNO)**：
   **Geo-FNO**（Li et al., NeurIPS 2022）通过可学习的连续微分同胚坐标映射 $\boldsymbol{\phi}: \Omega \to [0, 1]^d$，将含复杂地质断层、倾斜地层的不规则三维储层域拉回至标准规范计算网格，克服了传统神经算子无法适应复杂非规则几何的致命局限。

### 3.16 辛流形与李-泊松几何保结构神经算子 (Symplectic Manifolds & Lie-Poisson Structure-Preserving Operators)
在保守地球物理流体、波动动力学与大气环流的超长时程推演中，传统无约束神经网络极易破坏底层辛几何结构，产生非物理的人工数值耗散或在数百步自回归推演后彻底发散。
1. **无穷维辛神经算子 (Symplectic Neural Operators, SNO)**：
   **SNO**（Makara et al., 2026）将经典辛积分几何推广至无穷维偏微分方程系统。通过构造保辛两形式 $\omega = \int \delta \mathbf{q} \wedge \delta \mathbf{p} \, dx$ 的生成泛函网络内核，证明其严格保相空间体积（李维尔定理）。在强色散非线性波动方程中，传统 FNO 在 500 步后即产生超 40% 的相对能量衰减，而 SNO 在长达 **$10^4$ 步自回归长程演化**中，相对能量漂移小于 **0.02%**，实现真正的零数值阻尼推演。
2. **李-泊松对称性与涡度卡西米尔守恒算子 (LPNets)**：
   **LPNets**（Eldred, Gay-Balmaz, Huraka, Putkaradze, 2023）针对旋转球面 $\mathbb{S}^2$ 上的非正则哈密顿流体（如二维不可压缩欧拉方程与正压浅水涡度方程），利用代数构建的反对称李-泊松矩阵算子参数化哈密顿泛函，不仅保证总能量守恒，更严格将所有**卡西米尔不变量（Casimir Invariants）**（如总环量与拟能）以及**开尔文环量定理（Kelvin's Circulation Theorem）**保真至机器精度（**0.0% 环量漂移**），彻底根除长期积分中人工虚假涡旋耗散与拟能级联塌缩。

### 3.17 极端稀疏条件下的生成式拉格朗日连续海洋数据同化 (Generative Lagrangian Continuous Ocean Data Assimilation)
全球海洋内部观测高度依赖由数千枚自主漂移浮标（Argo 浮标剖面阵列、表层漂流浮标、水下滑翔机）组成的拉格朗日漂移序列：
$$\frac{d\mathbf{X}_i(t)}{dt} = \mathbf{u}(\mathbf{X}_i(t), t) + \boldsymbol{\eta}_i(t)$$
由于实测轨迹在空间全域的覆盖率常年**低于 0.5%**，经典最优化插值（OI）与基于线化的 4D-Var 同化在重建中尺度涡旋与边界流时面临严重模糊与伴随求解瓶颈。
- **扩散拉格朗日同化 (LagDA)**（Asefi et al., 2025）引入基于连续分数匹配的条件扩散概率模型，以稀疏不规则轨迹序列为先验条件，直接对连续欧拉速度场 $(u, v)$、海表面高度（SSH）与相对涡度 $\zeta = \nabla \times \mathbf{u}$ 的全概率后验进行采样。在全盆地覆盖率不足 0.5% 的极端稀疏条件下，LagDA 将水平流速 RMSE 降至 **0.092 m/s**，涡动动能（EKE）恢复率由传统插值的 42.1% 提升至 **91.4%**，涡度空间相关系数高达 **0.86**，成功精确还原了墨西哥湾流等强边界流与亚细尺度涡旋脱落动力学。

### 3.18 跨模态多星座卫星遥感时序基础模型 (Cross-Modality Continuous Pretraining on Multi-Constellation Satellite Image Time Series)
现代对地观测体系由轨道特性、空间分辨率与光谱通道迥异的多星座传感器网络构成（如 Sentinel-1 SAR、Sentinel-2 多光谱光学、Landsat、PlanetScope 等）。不同传感器具有完全异步的重访周期（从日尺度至十数日尺度）与巨大的空间分辨率落差（从 0.2 m 到 500 m）。
1. **联合交叉注意力掩码自编码器 (CROMA)**：
   **CROMA**（Fuller et al., NeurIPS 2023）创新性地提出结合对比学习与交叉注意力掩码自编码（MAE）的双通道架构。单模态编码器利用 2D-ALiBi 连续距离注意力偏置学习本征特征，多模态融合块通过双向交叉注意力强行将 Sentinel-1 微波穿透性雷达信号与 Sentinel-2 丰富光谱特征在隐空间对齐。评测显示，CROMA 在土地覆盖分类与农业监测下游任务中显著超越单模态模型，且展现出极其强悍的零样本空间外推能力（Zero-shot 17.6$\times$ 空间外推无伪影），在云层大面积遮挡下仍能通过雷达通道重建高精度光学地表反射率。
2. **多尺度任意模态跨星座基础模型 (AnySat)**：
   **AnySat**（Astruc et al., CVPR 2025 Highlight）突破了传统遥感模型固定地面采样距离（GSD）的限制。基于联合嵌入预测架构（JEPA）与连续尺度自适应调制，AnySat 支持对 0.2 m（高空航测）、10 m（Sentinel-2）、30 m（Landsat）至 500 m（MODIS）跨越三个数量级分辨率的异构传感器时序进行联合自监督预训练。AnySat 首次构建了涵盖全球高光谱、多光谱与 SAR 的综合基准 GeoPlex，在跨传感器零样本检索与极值灾害地物变化检测中取得了高达 89.2% 的宏平均准确率。

### 3.19 异步海气-海冰耦合多智能体地球系统多年代仿真器 (Coupled Atmosphere-Ocean-Cryosphere Multi-Agent Earth System Emulation)
传统气象大模型（如 Pangu-Weather、GraphCast）通常将海表面温度（SST）和海冰密集度（SIC）设为固定静态边界条件或简单外推，无法再现厄尔尼诺-南方涛动（ENSO）、大西洋经向翻转环流（AMOC）等涉及多物理圈层深度非线性相互作用的长期气候演进。
1. **全耦合多年代地球系统仿真器 (DLESyM)**：
   **DLESyM**（Cresswell-Clay et al., AGU Advances 2025 / Allen Institute for AI）构建了包含大气模块（30 垂直层）、海洋模块（60 垂直层）、陆面与海冰模块的全球全耦合基础系统。针对大气（小时级响应）与深海（数十年级热惯性）的时间多尺度特性，DLESyM 设计了多速率异步可微时间步进求解器，通过海气通量边界层严格交换潜热、感热、长短波辐射与风应力动量。在长达 100 年的无外加漂移自由耦合积分中，DLESyM 成功稳定复现了真实的季节循环与年际 ENSO 动力震荡，全球年平均表面温度累积漂移 $< 0.12\ \mathrm{K}$，相比传统气候数值模式运算速度提高超 **$2{,}500\times$**。
2. **三维大洋环流基础模型与物理通量耦合 (SamudrACE)**：
   **SamudrACE**（Duncan et al., GRL 2025）针对全球三维大洋状态（温度、盐度、流速 $U/V/W$）构建了基于球形神经算子的深度仿真模型。通过与 ACE 大气模型端到端通量耦合，SamudrACE 准确再现了赤道开尔文波东传、温跃层起伏以及极区海冰冻结-消融的年际反馈，解除了以往纯大气大模型在 30 天以上预测时因缺乏动态海洋反馈而出现的环流崩溃问题。

### 3.20 次网格对流微物理参数化与机器精度质量/能量守恒闭环 (High-Resolution Subgrid Microphysics & Analytic Conservation Layers)
在全球气候推演中，云对流、降水相变与湍流输送发生于微米至百米尺度，无法被全球粗网格（$1^\circ \sim 0.25^\circ$）直接解析，传统数值气候模式严重依赖高度经验化的次网格参数化方案。
1. **解析硬约束机器精度物理守恒神经网络 (AC-NN)**：
   **AC-NN**（Beucler et al., Physical Review Letters 2021）针对次网格对流加热率与增湿率建模，通过矩阵投影将能量、总水分与动量平衡方程转化为神经网络输出层的显式零空间投影核 $\mathbf{P} = \mathbf{I} - \mathbf{A}^T (\mathbf{A}\mathbf{A}^T)^{-1}\mathbf{A}$。在任何权重扰动与输入极端异常下，模型输出均**严格满足逐网格机器精度守恒（相对守恒残差 $< 10^{-15}$）**，彻底根除了传统神经网络因能量微小泄漏而在数十年连续循环递推中导致的虚假变暖或失控爆炸。
2. **全柱干空气与水分守恒的高吞吐气候仿真基石 (ACE)**：
   **ACE**（Watt-Meyer et al., JAMES 2024 / Allen Institute for AI）作为首个实现全球气候多年代稳定推演的基础模型，在自回归迭代步进中内嵌全局干空气总质量守恒修正算子与全柱水汽质量积分修正器。在 100 年连续自由运行中，ACE 将全柱水汽质量漂移控制在 0.05% 以内，年平均降水与蒸发维持严格闭环平衡，在单台商用 GPU 上以每秒模拟 1.2 年气候态的速度，为全球气候变化情景评估提供了兼具物理严谨性与超高吞吐量的全新范式。

---

## 4. 关键挑战与未来前沿方向 (Open Challenges & Frontiers)

1. **多模态连续物理统一分词器 (Unified Continuous Physical Tokenization)**：打破结构化规整网格（ERA5）、稀疏离散测站（雨量计、水文计、地震台网）与异构非规则遥感影像（Sentinel/Landsat）的表征边界，构建具备空间连续内插、时间自适应采样与物理守恒先验的通用物理分词架构。
2. **硬性物理守恒约束与极端极值可靠性标定 (Hard Physical Invariants & Extreme Event Calibration)**：在网络底层深度嵌入连续流形几何算子（如球面谐波 SFNO、神经常微分方程 ClimODE、辛算子 SNO、李-泊松算子 LPNets、解析投影核 AC-NN）与流体动力保真核，解决深度学习在极端台风、暴雨重尾事件中的欠拟合与物理违背缺陷。
3. **跨尺度跨模态卫星星座自适应多任务对齐 (Cross-Modality Multi-Constellation Satellite Foundations)**：解决雷达（SAR）穿透性散射与光学光谱特征在不同轨道高度、倾角与异步重访周期下的隐式几何对齐难题，利用如 AnySat 的多尺度 JEPA 框架统一 0.2m 至 500m 分辨率全域遥感时序。
4. **多圈层异步耦合地球系统仿真器长时稳定性 (Coupled Earth System Multi-Agent Emulation & Climate Drift)**：在大气、海洋、海冰与陆面等异构子系统之间建立能量、水汽与动量严格守恒的边界通量耦合器，突破百年以上无漂移气候态模拟的稳定性难题。
5. **高效多尺度可扩展扩散集合系统 (Scalable Probabilistic Diffusion Ensembles)**：降低扩散反向采样求解高维地球物理场时的计算开销，融合流匹配（Flow Matching）与一致性模型（Consistency Models），实现秒级生成全球数十个高保真物理集合成员。
6. **自主科学推理智能体沙盒与闭环验证 (Autonomous Scientific Discovery Sandboxes & Verification Loops)**：推动大语言模型从简单 API 调用迈向挂载全套科学计算生态（`xarray`, `metpy`, `dask`, `obspy`）的有状态沙盒，建立具备假设生成、自动代码推演、物理自检纠错与实验闭环验证的自主科学探索助手。
