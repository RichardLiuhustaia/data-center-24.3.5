# data-center-24.3.5

24.3.5 更新基础数据及参数文件

update 24.3.6. 更新参数文件，修改部分基础数据，完成数据中心调度模型建模及求解

包含：基本调度，功率平衡，数据中心各项约束，体现转移批处理负荷的能力考虑新能源利用及绿色证书

后面完善picture.py，美化优化结果

后期考虑将辅助服务与数据中心结合

数据中心模型来自英文文献，绿证来自中文文献

3.19 update:

仿真应该不需要大改了，本周应基本完成文档编写

设置了四个场景：电能量市场，电能量市场+绿证，电能量市场+调频市场，电能量市场+调频市场+绿证

可看出以下结论：该场景中可再生能源购电成本较高，使用绿证能够刺激数据中心系统完成对光伏能源的更多消纳，并提升经济效益。

但绿证只能部分提升该系统运行经济效益，而参与调频辅助服务市场则能够显著提升收入。
