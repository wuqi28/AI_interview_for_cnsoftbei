<template>
    <div class="interview-report">
        <!-- <topNav /> -->
        <!-- 报告容器 -->
        <div class="report-container">
            <div class="report-wrapper">
                <!-- 页面标题 -->
                <div class="report-header">
                    <div class="header-content"
                        style="display: flex; justify-content: space-between; align-items: center;">

                        <!-- 左侧内容：标题 + 元信息 -->
                        <div>
                            <h1>{{ company }}-{{ position }} 面试评测报告</h1>
                            <div class="report-meta">
                                <div class="meta-item">
                                    <span class="meta-label">面试者</span>
                                    <span class="meta-value">{{ userStore.user.email }}</span>
                                </div>
                                <div class="meta-item">
                                    <span class="meta-label">面试编号</span>
                                    <span class="meta-value">{{ reportData.interview_id }}</span>
                                </div>
                                <div class="meta-item">
                                    <span class="meta-label">总轮次</span>
                                    <span class="meta-value">{{ reportData.total_rounds }}</span>
                                </div>
                                <div class="meta-item">
                                    <span class="meta-label">面试时间</span>
                                    <span class="meta-value">{{ time }}</span>
                                </div>
                            </div>
                        </div>

                        <!-- 右侧：返回按钮 -->
                        <t-button theme="primary" shape="square" size="large" @click="$router.push('/resume')"
                            style="width: 56px; height: 56px;">
                            <template #icon>
                                <t-icon name="rollback" size="24px" />
                            </template>
                        </t-button>
                    </div>
                </div>

                <!-- 分页导航 -->
                <div class="tab-navigation">
                    <div v-for="(tab, index) in tabs" :key="index"
                        :class="['tab-item', { active: activeTab === index }]" @click="activeTab = index">
                        <span class="tab-icon">{{ tab.icon }}</span>
                        <span class="tab-text">{{ tab.name }}</span>
                    </div>
                </div>

                <!-- 分页内容 -->
                <div class="tab-content">
                    <!-- 面试概要 -->
                    <div v-if="activeTab === 0" class="overview-section">
                        <div class="overview-grid">
                            <!-- 基础信息卡片 -->
                            <div class="td-card info-card">
                                <div class="card-header">
                                    <h3>基础信息</h3>
                                </div>
                                <div class="card-content">
                                    <div class="info-item">
                                        <span class="info-label">总体得分</span>
                                        <div class="score-display">
                                            <span class="score-number">{{ reportData.score }}</span>
                                            <div class="score-progress">
                                                <div class="score-track">
                                                    <div class="score-fill" :style="{ width: reportData.score + '%' }">
                                                    </div>
                                                </div>
                                                <span class="score-text">{{ reportData.score }}/100</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="info-item">
                                        <span class="info-label">MBTI类型</span>
                                        <div class="td-tag mbti-tag">{{ reportData.mbti?.split('。')[0] || 'N/A' }}</div>
                                        <span class="summary-text">{{ reportData.mbti?.split('。')[1] || '' }}</span>
                                    </div>
                                    <div class="info-item summary-item">
                                        <span class="info-label">总结评语</span>
                                        <p class="summary-text">{{ reportData.summary }}</p>
                                    </div>
                                </div>
                            </div>

                            <!-- 能力雷达图 -->
                            <div class="td-card chart-card">
                                <div class="card-header">
                                    <h3>能力评估雷达图</h3>
                                </div>
                                <div class="card-content">
                                    <div ref="radarChart" class="radar-chart"></div>
                                </div>
                            </div>

                            <!-- 高亮能力 -->
                            <div class="td-card abilities-card">
                                <div class="card-header">
                                    <h3>突出能力</h3>
                                </div>
                                <div class="card-content">
                                    <div class="abilities-list">
                                        <div v-for="ability in reportData.highlight_abilities" :key="ability.ability"
                                            class="ability-item">
                                            <div class="ability-header">
                                                <div class="td-tag ability-tag">{{ ability.ability }}</div>
                                            </div>
                                            <p class="ability-evidence">{{ ability.evidence }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <!-- 多模态表现摘要 -->
                            <div class="td-card multimodal-card">
                                <div class="card-header">
                                    <h3>多模态表现摘要</h3>
                                </div>
                                <div class="card-content">
                                    <div class="multimodal-grid">
                                        <div class="modal-item">
                                            <div class="modal-header">
                                                <span class="modal-icon">🎵</span>
                                                <span class="modal-title">音频表现</span>
                                            </div>
                                            <p class="modal-content">{{ reportData.multimodal_signal_summary?.audio }}
                                            </p>
                                        </div>
                                        <div class="modal-item">
                                            <div class="modal-header">
                                                <span class="modal-icon">📹</span>
                                                <span class="modal-title">视频表现</span>
                                            </div>
                                            <p class="modal-content">{{ reportData.multimodal_signal_summary?.video }}
                                            </p>
                                        </div>
                                        <div class="modal-item">
                                            <div class="modal-header">
                                                <span class="modal-icon">📝</span>
                                                <span class="modal-title">文本表现</span>
                                            </div>
                                            <p class="modal-content">{{ reportData.multimodal_signal_summary?.text }}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 问题分析 -->
                    <div v-if="activeTab === 1" class="rounds-section">
                        <div class="rounds-list">
                            <div v-for="(round, roundIndex) in reportData.round_analysis" :key="round.round"
                                class="td-card round-card">
                                <div class="card-header">
                                    <h4>第 {{ round.round }} 轮面试</h4>
                                    <audio v-if="round.audio_path" controls class="td-audio">
                                        <source :src="round.audio_path" type="audio/wav">
                                        您的浏览器不支持音频播放
                                    </audio>
                                </div>

                                <div class="card-content">
                                    <div class="qa-section">
                                        <div class="question-block">
                                            <div class="td-tag interviewer-tag">AI面试官</div>
                                            <div class="message-bubble interviewer-bubble">{{ round.ai_interviewer_text
                                            }}</div>
                                        </div>

                                        <div class="answer-block">
                                            <div class="td-tag candidate-tag">面试者</div>
                                            <div class="message-bubble candidate-bubble">{{ round.speaker_text }}</div>
                                        </div>

                                        <!-- 优化回答部分 -->
                                        <div class="optimized-answer-block">
                                            <div class="optimized-header">
                                                <div class="td-tag optimized-tag">优化回答</div>
                                                <button
                                                    v-if="!optimizedAnswers[roundIndex]?.loading && !optimizedAnswers[roundIndex]?.content"
                                                    class="td-button optimize-button"
                                                    @click="generateOptimizedAnswer(roundIndex, round)">
                                                    生成优化回答
                                                </button>
                                            </div>
                                            <div v-if="optimizedAnswers[roundIndex]?.loading" class="optimized-loading">
                                                <div class="loading-dots">
                                                    <span></span>
                                                    <span></span>
                                                    <span></span>
                                                </div>
                                                <span>正在生成优化回答...</span>
                                            </div>
                                            <div v-if="optimizedAnswers[roundIndex]?.content"
                                                class="message-bubble optimized-bubble">
                                                {{ optimizedAnswers[roundIndex].content }}
                                            </div>
                                        </div>
                                    </div>

                                    <!-- 问题知识点分析 -->
                                    <div v-if="round.question_analysis" class="question-analysis-section">
                                        <div class="analysis-header">
                                            <span class="analysis-icon">🧠</span>
                                            <span class="analysis-title">问题分析</span>
                                        </div>
                                        <div class="question-analysis-content">
                                            <p class="analysis-content">{{ round.question_analysis }}</p>
                                        </div>
                                    </div>

                                    <div class="analysis-section">
                                        <div class="analysis-grid">
                                            <div class="analysis-item">
                                                <div class="analysis-header">
                                                    <span class="analysis-icon">🎵</span>
                                                    <span class="analysis-title">音频分析</span>
                                                </div>
                                                <p class="analysis-content">{{ round.audio_analysis }}</p>
                                            </div>
                                            <div class="analysis-item">
                                                <div class="analysis-header">
                                                    <span class="analysis-icon">📹</span>
                                                    <span class="analysis-title">视频分析</span>
                                                </div>
                                                <p class="analysis-content">{{ round.video_analysis }}</p>
                                            </div>
                                            <div class="analysis-item">
                                                <div class="analysis-header">
                                                    <span class="analysis-icon">📝</span>
                                                    <span class="analysis-title">文本分析</span>
                                                </div>
                                                <p class="analysis-content">{{ round.text_analysis }}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 答案分析 - 新增的动态内容区域 -->
                    <div v-if="activeTab === 2 && interviewStore.job_type !== 0" class="answer-analysis-section">
                        <!-- 算法编程面试 (job_type = 1) -->
                        <div v-if="interviewStore.job_type === 1" class="algorithm-analysis">
                            <div class="section-header">
                                <h3>算法编程题目分析</h3>
                                <p class="section-description">基于您的算法编程面试表现，以下是详细的题目分析和解答思路</p>
                            </div>

                            <div class="algorithm-problems">
                                <!-- Two Sum 问题 -->
                                <div class="td-card problem-card">
                                    <div class="card-header">
                                        <div class="problem-header">
                                            <div class="td-tag difficulty-tag beginner">初级</div>
                                            <h4>Two Sum (两数之和)</h4>
                                        </div>
                                    </div>
                                    <div class="card-content">
                                        <div class="problem-content">
                                            <div class="problem-description">
                                                <h5>题目描述</h5>
                                                <p>给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出和为目标值 target
                                                    的那两个整数，并返回它们的数组下标。</p>
                                            </div>
                                            <div class="problem-solution">
                                                <h5>解题思路</h5>
                                                <ul>
                                                    <li>使用哈希表存储已遍历的数字及其索引</li>
                                                    <li>对于每个数字，检查 target - 当前数字 是否在哈希表中</li>
                                                    <li>时间复杂度：O(n)，空间复杂度：O(n)</li>
                                                </ul>
                                            </div>
                                            <div class="code-example">
                                                <h5>参考代码</h5>
                                                <pre class="code-block"><code>def twoSum(nums, target):
                                        hash_map = {}
                                        for i, num in enumerate(nums):
                                        complement = target - num
                                        if complement in hash_map:
                                        return [hash_map[complement], i]
                                        hash_map[num] = i
                                        return []</code></pre>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Maximum Subarray Sum 问题 -->
                                <div class="td-card problem-card">
                                    <div class="card-header">
                                        <div class="problem-header">
                                            <div class="td-tag difficulty-tag intermediate">中级</div>
                                            <h4>Maximum Subarray Sum (最大子数组和)</h4>
                                        </div>
                                    </div>
                                    <div class="card-content">
                                        <div class="problem-content">
                                            <div class="problem-description">
                                                <h5>题目描述</h5>
                                                <p>给你一个整数数组 nums，请你找出一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。</p>
                                            </div>
                                            <div class="problem-solution">
                                                <h5>解题思路</h5>
                                                <ul>
                                                    <li>使用动态规划（Kadane算法）</li>
                                                    <li>维护当前最大和与全局最大和</li>
                                                    <li>时间复杂度：O(n)，空间复杂度：O(1)</li>
                                                </ul>
                                            </div>
                                            <div class="code-example">
                                                <h5>参考代码</h5>
                                                <pre class="code-block"><code>def maxSubArray(nums):
                                        max_sum = nums[0]
                                        current_sum = nums[0]

                                        for i in range(1, len(nums)):
                                        current_sum = max(nums[i], current_sum + nums[i])
                                        max_sum = max(max_sum, current_sum)

                                        return max_sum</code></pre>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- Merge Two Sorted Lists 问题 -->
                                <div class="td-card problem-card">
                                    <div class="card-header">
                                        <div class="problem-header">
                                            <div class="td-tag difficulty-tag advanced">高级</div>
                                            <h4>Merge Two Sorted Lists (合并两个有序链表)</h4>
                                        </div>
                                    </div>
                                    <div class="card-content">
                                        <div class="problem-content">
                                            <div class="problem-description">
                                                <h5>题目描述</h5>
                                                <p>将两个升序链表合并为一个新的升序链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。</p>
                                            </div>
                                            <div class="problem-solution">
                                                <h5>解题思路</h5>
                                                <ul>
                                                    <li>使用双指针技术比较两个链表的节点</li>
                                                    <li>创建虚拟头节点简化边界处理</li>
                                                    <li>时间复杂度：O(m+n)，空间复杂度：O(1)</li>
                                                </ul>
                                            </div>
                                            <div class="code-example">
                                                <h5>参考代码</h5>
                                                <pre class="code-block"><code>def mergeTwoLists(list1, list2):
                                        dummy = ListNode(0)
                                        current = dummy

                                        while list1 and list2:
                                        if list1.val = list2.val:
                                        current.next = list1
                                        list1 = list1.next
                                        else:
                                        current.next = list2
                                        list2 = list2.next
                                        current = current.next

                                        current.next = list1 or list2
                                        return dummy.next</code></pre>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- DevOps/测试面试 (job_type = 2) -->
                        <div v-if="interviewStore.job_type === 2" class="devops-analysis">
                            <div class="section-header">
                                <h3>DevOps/测试场景分析</h3>
                                <p class="section-description">基于您的DevOps和测试面试表现，以下是关键场景的处理流程和决策分析</p>
                            </div>

                            <div class="devops-scenarios">
                                <!-- 服务器异常处理流程 -->
                                <div class="td-card scenario-card">
                                    <div class="card-header">
                                        <h4>🔧 服务器异常处理流程</h4>
                                    </div>
                                    <div class="card-content">
                                        <div class="process-flow">
                                            <div class="flow-step">
                                                <div class="step-number">1</div>
                                                <div class="step-content">
                                                    <h5>确认故障现象和影响范围</h5>
                                                    <p>评估业务影响，确定处理优先级</p>
                                                </div>
                                            </div>
                                            <div class="flow-arrow">↓</div>

                                            <div class="flow-step">
                                                <div class="step-number">2</div>
                                                <div class="step-content">
                                                    <h5>查看系统日志和监控数据</h5>
                                                    <p>分析日志文件，检查监控指标异常</p>
                                                </div>
                                            </div>
                                            <div class="flow-arrow">↓</div>

                                            <div class="flow-step">
                                                <div class="step-number">3</div>
                                                <div class="step-content">
                                                    <h5>定位故障根本原因</h5>
                                                    <p>结合日志与现象，找出具体原因点</p>
                                                </div>
                                            </div>
                                            <div class="flow-arrow">↓</div>

                                            <div class="flow-step">
                                                <div class="step-number">4</div>
                                                <div class="step-content">
                                                    <h5>制定应急处理方案</h5>
                                                    <p>根据影响范围和故障性质确定修复策略</p>
                                                </div>
                                            </div>
                                            <div class="flow-arrow">↓</div>

                                            <div class="flow-step">
                                                <div class="step-number">5</div>
                                                <div class="step-content">
                                                    <h5>执行故障修复操作</h5>
                                                    <p>根据分析结果执行相应的修复措施</p>
                                                </div>
                                            </div>
                                            <div class="flow-arrow">↓</div>

                                            <div class="flow-step">
                                                <div class="step-number">6</div>
                                                <div class="step-content">
                                                    <h5>验证修复效果</h5>
                                                    <p>确认业务恢复正常，指标恢复合理范围</p>
                                                </div>
                                            </div>
                                            <div class="flow-arrow">↓</div>

                                            <div class="flow-step">
                                                <div class="step-number">7</div>
                                                <div class="step-content">
                                                    <h5>编写故障处理报告</h5>
                                                    <p>记录故障现象、影响范围、初步分析结果</p>
                                                </div>
                                            </div>
                                            <div class="flow-arrow">↓</div>

                                            <div class="flow-step">
                                                <div class="step-number">8</div>
                                                <div class="step-content">
                                                    <h5>总结经验和改进措施</h5>
                                                    <p>制定预防措施，优化监控和告警</p>
                                                </div>
                                            </div>

                                        </div>
                                    </div>
                                </div>

                                <!-- 场景决策分析 -->
                                <div class="td-card scenario-card">
                                    <div class="card-header">
                                        <h4>🎯 关键场景决策分析</h4>
                                    </div>
                                    <div class="card-content">
                                        <div class="scenario-grid">
                                            <div class="scenario-item">
                                                <div class="scenario-header">
                                                    <span class="scenario-icon">💻</span>
                                                    <h5>CPU使用率过高</h5>
                                                </div>
                                                <div class="scenario-actions">
                                                    <div class="action-item priority-high">立即重启服务器</div>
                                                    <div class="action-item priority-medium">查看进程列表，定位高CPU占用进程</div>
                                                    <div class="action-item priority-medium">增加服务器配置</div>
                                                    <div class="action-item priority-low">适当用户系统维护</div>
                                                </div>
                                            </div>

                                            <div class="scenario-item">
                                                <div class="scenario-header">
                                                    <span class="scenario-icon">🗄️</span>
                                                    <h5>数据库连接异常</h5>
                                                </div>
                                                <div class="scenario-actions">
                                                    <div class="action-item priority-high">检查数据库服务状态</div>
                                                    <div class="action-item priority-high">验证网络连通性</div>
                                                    <div class="action-item priority-medium">检查连接池配置</div>
                                                    <div class="action-item priority-medium">查看数据库日志</div>
                                                    <div class="action-item priority-low">重启应用服务</div>
                                                </div>
                                            </div>

                                            <div class="scenario-item">
                                                <div class="scenario-header">
                                                    <span class="scenario-icon">💾</span>
                                                    <h5>磁盘空间不足</h5>
                                                </div>
                                                <div class="scenario-actions">
                                                    <div class="action-item priority-high">立即清理日志文件</div>
                                                    <div class="action-item priority-medium">申请扩容磁盘</div>
                                                    <div class="action-item priority-medium">迁移部分数据到其他服务器</div>
                                                    <div class="action-item priority-low">重启服务器释放缓存</div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 产品面试 (job_type = 3) -->
                        <div v-if="interviewStore.job_type === 3" class="product-analysis">
                            <div class="section-header">
                                <h3>产品设计分析</h3>
                                <p class="section-description">基于您的产品面试表现，以下是产品设计思路和功能规划的详细分析</p>
                            </div>

                            <div class="product-design">
                                <!-- 解决方案描述 -->
                                <div class="td-card solution-card">
                                    <div class="card-header">
                                        <h4>💡 解决方案描述</h4>
                                    </div>
                                    <div class="card-content">
                                        <div class="solution-content">
                                            <div class="solution-overview">
                                                <h5>老年人健康管理App设计方案</h5>
                                                <p>针对60+老年人群体，设计一款简单易用的健康管理应用，考虑老年人的使用习惯和身体特点，提供个性化的健康管理服务。</p>
                                            </div>

                                            <div class="design-principles">
                                                <h5>设计原则</h5>
                                                <div class="principles-grid">
                                                    <div class="principle-item">
                                                        <span class="principle-icon">👁️</span>
                                                        <div class="principle-content">
                                                            <h6>视觉友好</h6>
                                                            <p>大字体、高对比度、简洁界面</p>
                                                        </div>
                                                    </div>
                                                    <div class="principle-item">
                                                        <span class="principle-icon">🤏</span>
                                                        <div class="principle-content">
                                                            <h6>操作简单</h6>
                                                            <p>大按钮、少步骤、语音辅助</p>
                                                        </div>
                                                    </div>
                                                    <div class="principle-item">
                                                        <span class="principle-icon">🏥</span>
                                                        <div class="principle-content">
                                                            <h6>专业可靠</h6>
                                                            <p>医疗级数据、专家建议</p>
                                                        </div>
                                                    </div>
                                                    <div class="principle-item">
                                                        <span class="principle-icon">👨‍👩‍👧‍👦</span>
                                                        <div class="principle-content">
                                                            <h6>家庭关怀</h6>
                                                            <p>家属监护、紧急联系</p>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- 功能特性列表 -->
                                <div class="td-card features-card">
                                    <div class="card-header">
                                        <h4>⭐ 核心功能特性</h4>
                                    </div>
                                    <div class="card-content">
                                        <div class="features-grid">
                                            <div class="feature-category">
                                                <h5>健康监测</h5>
                                                <ul class="feature-list">
                                                    <li>血压、血糖、心率记录</li>
                                                    <li>用药提醒和记录</li>
                                                    <li>体重、睡眠质量跟踪</li>
                                                    <li>健康数据可视化图表</li>
                                                </ul>
                                            </div>

                                            <div class="feature-category">
                                                <h5>智能提醒</h5>
                                                <ul class="feature-list">
                                                    <li>服药时间提醒</li>
                                                    <li>体检预约提醒</li>
                                                    <li>运动建议推送</li>
                                                    <li>饮食营养建议</li>
                                                </ul>
                                            </div>

                                            <div class="feature-category">
                                                <h5>医疗服务</h5>
                                                <ul class="feature-list">
                                                    <li>在线问诊咨询</li>
                                                    <li>附近医院导航</li>
                                                    <li>电子病历管理</li>
                                                    <li>专家健康讲座</li>
                                                </ul>
                                            </div>

                                            <div class="feature-category">
                                                <h5>社交关怀</h5>
                                                <ul class="feature-list">
                                                    <li>家属健康共享</li>
                                                    <li>紧急联系功能</li>
                                                    <li>健康社区交流</li>
                                                    <li>志愿者服务对接</li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- 用户流程图 -->
                                <div class="td-card flowchart-card">
                                    <div class="card-header">
                                        <h4>📊 用户使用流程图</h4>
                                    </div>
                                    <div class="card-content">
                                        <div class="flowchart-container">
                                            <div class="flow-section">
                                                <h5>新用户注册流程</h5>
                                                <div class="flow-steps horizontal">
                                                    <div class="flow-step">
                                                        <div class="step-box">下载安装</div>
                                                    </div>
                                                    <div class="flow-arrow-right">→</div>
                                                    <div class="flow-step">
                                                        <div class="step-box">简单注册</div>
                                                    </div>
                                                    <div class="flow-arrow-right">→</div>
                                                    <div class="flow-step">
                                                        <div class="step-box">健康档案</div>
                                                    </div>
                                                    <div class="flow-arrow-right">→</div>
                                                    <div class="flow-step">
                                                        <div class="step-box">功能引导</div>
                                                    </div>
                                                </div>
                                            </div>

                                            <div class="flow-section">
                                                <h5>日常使用流程</h5>
                                                <div class="flow-steps horizontal">
                                                    <div class="flow-step">
                                                        <div class="step-box">打开应用</div>
                                                    </div>
                                                    <div class="flow-arrow-right">→</div>
                                                    <div class="flow-step">
                                                        <div class="step-box">查看提醒</div>
                                                    </div>
                                                    <div class="flow-arrow-right">→</div>
                                                    <div class="flow-step">
                                                        <div class="step-box">记录数据</div>
                                                    </div>
                                                    <div class="flow-arrow-right">→</div>
                                                    <div class="flow-step">
                                                        <div class="step-box">查看报告</div>
                                                    </div>
                                                </div>
                                            </div>

                                            <div class="flow-section">
                                                <h5>紧急情况处理</h5>
                                                <div class="flow-steps horizontal">
                                                    <div class="flow-step">
                                                        <div class="step-box">异常检测</div>
                                                    </div>
                                                    <div class="flow-arrow-right">→</div>
                                                    <div class="flow-step">
                                                        <div class="step-box">自动告警</div>
                                                    </div>
                                                    <div class="flow-arrow-right">→</div>
                                                    <div class="flow-step">
                                                        <div class="step-box">联系家属</div>
                                                    </div>
                                                    <div class="flow-arrow-right">→</div>
                                                    <div class="flow-step">
                                                        <div class="step-box">医疗救助</div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 知识点分析 -->
                    <div v-if="activeTab === 3" class="knowledge-section">
                        <div class="td-card knowledge-chart-card">
                            <div class="card-header">
                                <h3>知识点掌握程度分析</h3>
                            </div>
                            <div class="card-content">
                                <div ref="knowledgeChart" class="knowledge-chart"></div>
                            </div>
                        </div>

                        <div class="td-card knowledge-list-card">
                            <div class="card-header">
                                <h3>详细评分</h3>
                            </div>
                            <div class="card-content">
                                <div class="knowledge-list">
                                    <div v-for="knowledge in reportData.knowledge_analysis"
                                        :key="knowledge.knowledge_name" class="knowledge-item">
                                        <div class="knowledge-info">
                                            <span class="knowledge-name">{{ knowledge.knowledge_name }}</span>
                                            <span class="knowledge-score"
                                                :class="getScoreClass(knowledge.knowledge_num)">
                                                {{ knowledge.knowledge_num }}%
                                            </span>
                                        </div>
                                        <div class="td-progress">
                                            <div class="progress-track">
                                                <div class="progress-fill"
                                                    :class="getScoreClass(knowledge.knowledge_num)"
                                                    :style="{ width: knowledge.knowledge_num + '%' }"></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 智能建议 -->
                    <div v-if="activeTab === 4" class="suggestions-section">
                        <div class="suggestions-header">
                            <h3>智能改进建议</h3>
                            <div class="filter-group">
                                <button v-for="dimension in uniqueDimensions" :key="dimension"
                                    :class="['td-button', 'filter-button', { active: selectedDimension === dimension }]"
                                    @click="selectedDimension = selectedDimension === dimension ? '' : dimension">
                                    {{ dimension }}
                                </button>
                            </div>
                        </div>

                        <div class="suggestions-list">
                            <div v-for="(suggestion, index) in filteredSuggestions" :key="index"
                                class="td-card suggestion-card">
                                <div class="card-header">
                                    <div class="td-tag dimension-tag">{{ suggestion.dimension }}</div>
                                    <button class="td-button icon-button" @click="copySuggestion(suggestion)">
                                        📋
                                    </button>
                                </div>
                                <div class="card-content">
                                    <div class="suggestion-grid">
                                        <div class="suggestion-block issue-block">
                                            <div class="block-header">
                                                <span class="block-icon">🔍</span>
                                                <span class="block-title">发现问题</span>
                                            </div>
                                            <p class="block-content">{{ suggestion.issue }}</p>
                                        </div>
                                        <div class="suggestion-block solution-block">
                                            <div class="block-header">
                                                <span class="block-icon">💡</span>
                                                <span class="block-title">改进建议</span>
                                            </div>
                                            <p class="block-content">{{ suggestion.suggestion }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 学习路径规划 -->
                    <div v-if="activeTab === 5" class="learning-path-section">
                        <div class="learning-path-header">
                            <h3>个性化学习路径规划</h3>
                            <p class="learning-path-description">基于您的面试表现，为您量身定制的学习提升计划</p>
                        </div>

                        <div class="learning-stages">
                            <div v-for="(stage, index) in reportData.learning_path" :key="index"
                                class="td-card learning-stage-card">
                                <div class="card-header">
                                    <div class="stage-header">
                                        <div class="stage-number">{{ index + 1 }}</div>
                                        <h4>{{ stage.stage }}</h4>
                                    </div>
                                </div>
                                <div class="card-content">
                                    <div class="learning-content-grid">
                                        <!-- 目标技能 -->
                                        <div class="learning-block">
                                            <div class="block-header">
                                                <span class="block-icon">🎯</span>
                                                <span class="block-title">目标技能</span>
                                            </div>
                                            <div class="skill-tags">
                                                <div v-for="skill in stage.target_skills" :key="skill"
                                                    class="td-tag skill-tag">
                                                    {{ skill }}
                                                </div>
                                            </div>
                                        </div>

                                        <!-- 改进重点 -->
                                        <div class="learning-block">
                                            <div class="block-header">
                                                <span class="block-icon">📈</span>
                                                <span class="block-title">改进重点</span>
                                            </div>
                                            <ul class="improvement-list">
                                                <li v-for="improvement in stage.improvements" :key="improvement">
                                                    {{ improvement }}
                                                </li>
                                            </ul>
                                        </div>

                                        <!-- 推荐练习 -->
                                        <div class="learning-block">
                                            <div class="block-header">
                                                <span class="block-icon">💪</span>
                                                <span class="block-title">推荐练习</span>
                                            </div>
                                            <ul class="practice-list">
                                                <li v-for="practice in stage.recommended_practice" :key="practice">
                                                    {{ practice }}
                                                </li>
                                            </ul>
                                        </div>

                                        <!-- 学习资源 -->
                                        <div class="learning-block resources-block">
                                            <div class="block-header">
                                                <span class="block-icon">📚</span>
                                                <span class="block-title">学习资源</span>
                                            </div>
                                            <div class="resources-list">
                                                <div v-for="resource in stage.resources" :key="resource.name"
                                                    class="resource-item">
                                                    <a :href="resource.url" target="_blank" class="resource-link">
                                                        <span class="resource-name">{{ resource.name }}</span>
                                                        <span class="resource-icon">🔗</span>
                                                    </a>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 数据归档 -->
                    <div v-if="activeTab === 6" class="export-section">
                        <div class="export-grid">
                            <div class="td-card export-card">
                                <div class="card-header">
                                    <h3>📄 报告导出</h3>
                                </div>
                                <div class="card-content">
                                    <div class="export-actions">
                                        <button class="td-button primary-button" @click="exportToPDF"
                                            :disabled="isExporting">
                                            <span class="button-icon">📑</span>
                                            <span>{{ isExporting ? '生成中...' : '导出PDF报告' }}</span>
                                        </button>
                                        <button class="td-button secondary-button" @click="exportToJSON">
                                            <span class="button-icon">💾</span>
                                            <span>导出JSON数据</span>
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <div class="td-card audio-card">
                                <div class="card-header">
                                    <h3>🎵 音频文件</h3>
                                </div>
                                <div class="card-content">
                                    <div class="audio-list">
                                        <div v-for="(round, index) in reportData.round_analysis" :key="index"
                                            class="audio-item">
                                            <span class="audio-name">第{{ round.round }}轮录音</span>
                                            <a v-if="round.audio_path" :href="round.audio_path" download
                                                class="td-link">
                                                下载
                                            </a>
                                        </div>
                                    </div>
                                    <button class="td-button secondary-button full-width" @click="downloadAllAudio">
                                        <span class="button-icon">📦</span>
                                        <span>打包下载所有音频</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 隐藏的PDF内容 -->
        <div ref="pdfContent" class="pdf-content" style="position: absolute; left: -9999px; top: 0;">
            <div v-if="Object.keys(reportData).length > 0"
                style="width: 800px; background: white; padding: 40px; font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                <!-- PDF标题页 -->
                <div style="text-align: center; margin-bottom: 40px;">
                    <div
                        style="background: linear-gradient(135deg, #0052D9 0%, #1677FF 100%); color: white; padding: 40px 20px; border-radius: 8px; margin-bottom: 30px;">
                        <h1 style="margin: 0; font-size: 32px; font-weight: 600;">{{ company }}-{{ position }} 面试评测报告
                        </h1>
                        <div style="margin-top: 20px; font-size: 16px; opacity: 0.9;">
                            <div>面试者：{{ userStore.user.email }}</div>
                            <div>面试编号：{{ reportData.interview_id || 'N/A' }}</div>
                            <div>总轮次：{{ reportData.total_rounds || 'N/A' }}</div>
                            <div>面试时间：{{ time }}</div>
                        </div>
                    </div>

                    <div style="background: #f8f9fa; padding: 30px; border-radius: 8px; text-align: left;">
                        <h2 style="color: #0052D9; margin-bottom: 20px;">报告概要</h2>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                            <div>
                                <strong>总体得分：</strong>
                                <span style="font-size: 24px; color: #0052D9; font-weight: bold;">{{ reportData.score ||
                                    'N/A' }}/100</span>
                            </div>
                            <div>
                                <strong>MBTI类型：</strong>
                                <span
                                    style="background: #E7F3FF; color: #0052D9; padding: 4px 8px; border-radius: 4px;">{{
                                        (reportData.mbti || 'N/A').split('。')[0] }}</span>
                            </div>
                        </div>
                        <div>
                            <strong>总结评语：</strong>
                            <p style="margin: 10px 0; line-height: 1.8;">{{ reportData.summary || '暂无总结' }}</p>
                        </div>
                    </div>
                </div>

                <!-- 能力评估详情 -->
                <div style="margin-bottom: 40px; page-break-inside: avoid;">
                    <h2
                        style="color: #0052D9; border-bottom: 2px solid #0052D9; padding-bottom: 10px; margin-bottom: 20px;">
                        能力评估详情</h2>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div v-for="(value, key) in reportData.scores" :key="key"
                            style="background: #f8f9fa; padding: 15px; border-radius: 6px; border-left: 4px solid #0052D9;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-weight: 500;">{{ key }}</span>
                                <span style="font-weight: bold; color: #0052D9;">{{ value }}分</span>
                            </div>
                            <div
                                style="margin-top: 8px; height: 6px; background: #e0e0e0; border-radius: 3px; overflow: hidden;">
                                <div style="height: 100%; background: #0052D9; border-radius: 3px;"
                                    :style="{ width: value + '%' }"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 突出能力 -->
                <div style="margin-bottom: 40px; page-break-inside: avoid;">
                    <h2
                        style="color: #0052D9; border-bottom: 2px solid #0052D9; padding-bottom: 10px; margin-bottom: 20px;">
                        突出能力</h2>
                    <div v-for="ability in reportData.highlight_abilities" :key="ability.ability"
                        style="background: #f8f9fa; padding: 16px; margin-bottom: 12px; border-radius: 6px; border-left: 4px solid #00A870;">
                        <div style="font-weight: 600; color: #00A870; margin-bottom: 8px;">{{ ability.ability }}</div>
                        <p style="margin: 0; color: #666; line-height: 1.6;">{{ ability.evidence }}</p>
                    </div>
                </div>

                <!-- 知识点分析 -->
                <div style="margin-bottom: 40px; page-break-inside: avoid;">
                    <h2
                        style="color: #0052D9; border-bottom: 2px solid #0052D9; padding-bottom: 10px; margin-bottom: 20px;">
                        知识点掌握程度</h2>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                        <div v-for="knowledge in reportData.knowledge_analysis" :key="knowledge.knowledge_name"
                            style="background: #f8f9fa; padding: 12px; border-radius: 6px;">
                            <div
                                style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                <span style="font-weight: 500; font-size: 14px;">{{ knowledge.knowledge_name }}</span>
                                <span style="font-weight: bold; color: #0052D9;">{{ knowledge.knowledge_num }}%</span>
                            </div>
                            <div style="height: 6px; background: #e0e0e0; border-radius: 3px; overflow: hidden;">
                                <div style="height: 100%; background: #0052D9; border-radius: 3px;"
                                    :style="{ width: knowledge.knowledge_num + '%' }"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 多模态表现摘要 -->
                <div style="margin-bottom: 40px; page-break-inside: avoid;">
                    <h2
                        style="color: #0052D9; border-bottom: 2px solid #0052D9; padding-bottom: 10px; margin-bottom: 20px;">
                        多模态表现摘要</h2>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div style="background: #f8f9fa; padding: 16px; border-radius: 6px;">
                            <div style="font-weight: 600; color: #0052D9; margin-bottom: 8px;">🎵 音频表现</div>
                            <p style="margin: 0; line-height: 1.6;">{{ reportData.multimodal_signal_summary?.audio ||
                                '暂无音频分析' }}</p>
                        </div>
                        <div style="background: #f8f9fa; padding: 16px; border-radius: 6px;">
                            <div style="font-weight: 600; color: #0052D9; margin-bottom: 8px;">📹 视频表现</div>
                            <p style="margin: 0; line-height: 1.6;">{{ reportData.multimodal_signal_summary?.video ||
                                '暂无视频分析' }}</p>
                        </div>
                        <div style="background: #f8f9fa; padding: 16px; border-radius: 6px;">
                            <div style="font-weight: 600; color: #0052D9; margin-bottom: 8px;">📝 文本表现</div>
                            <p style="margin: 0; line-height: 1.6;">{{ reportData.multimodal_signal_summary?.text ||
                                '暂无文本分析' }}</p>
                        </div>
                    </div>
                </div>

                <!-- 智能建议 -->
                <div style="margin-bottom: 40px;">
                    <h2
                        style="color: #0052D9; border-bottom: 2px solid #0052D9; padding-bottom: 10px; margin-bottom: 20px;">
                        智能改进建议</h2>
                    <div v-for="(suggestion, index) in reportData.recommendations" :key="index"
                        style="background: #f8f9fa; padding: 20px; margin-bottom: 16px; border-radius: 6px; page-break-inside: avoid;">
                        <div style="margin-bottom: 16px;">
                            <span
                                style="background: #0052D9; color: white; padding: 4px 12px; border-radius: 16px; font-size: 12px; font-weight: 600;">{{
                                    suggestion.dimension }}</span>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                            <div style="background: white; padding: 16px; border-radius: 6px;">
                                <div style="font-weight: 600; color: #666; margin-bottom: 8px; font-size: 14px;">🔍 发现问题
                                </div>
                                <p style="margin: 0; line-height: 1.6;">{{ suggestion.issue }}</p>
                            </div>
                            <div style="background: white; padding: 16px; border-radius: 6px;">
                                <div style="font-weight: 600; color: #666; margin-bottom: 8px; font-size: 14px;">💡 改进建议
                                </div>
                                <p style="margin: 0; line-height: 1.6;">{{ suggestion.suggestion }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 问题分析摘要 -->
                <div style="margin-bottom: 40px;">
                    <h2
                        style="color: #0052D9; border-bottom: 2px solid #0052D9; padding-bottom: 10px; margin-bottom: 20px;">
                        面试问答摘要</h2>
                    <div v-for="round in (reportData.round_analysis || []).slice(0, 5)" :key="round.round"
                        style="background: #f8f9fa; padding: 16px; margin-bottom: 16px; border-radius: 6px; page-break-inside: avoid;">
                        <h4 style="margin: 0 0 12px 0; color: #333;">第 {{ round.round }} 轮</h4>
                        <div style="margin-bottom: 12px;">
                            <div
                                style="background: #E7F3FF; color: #0052D9; padding: 4px 8px; border-radius: 4px; font-size: 12px; display: inline-block; margin-bottom: 8px;">
                                AI面试官</div>
                            <div style="background: white; padding: 12px; border-radius: 6px; line-height: 1.6;">{{
                                round.ai_interviewer_text }}</div>
                        </div>
                        <div style="margin-bottom: 12px;">
                            <div
                                style="background: #E8F5E8; color: #00A870; padding: 4px 8px; border-radius: 4px; font-size: 12px; display: inline-block; margin-bottom: 8px;">
                                面试者</div>
                            <div style="background: white; padding: 12px; border-radius: 6px; line-height: 1.6;">{{
                                round.speaker_text }}</div>
                        </div>
                        <div style="background: white; padding: 12px; border-radius: 6px;">
                            <div style="font-size: 12px; color: #666;"><strong>文本分析：</strong>{{ round.text_analysis }}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 页脚 -->
                <div
                    style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #e0e0e0; color: #666; font-size: 12px;">
                    <p>本报告由AI面试系统自动生成 | 生成时间：{{ new Date().toLocaleString('zh-CN') }}</p>
                    <p>报告编号：{{ reportData.interview_id || 'N/A' }} | 版本：v1.0</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, watch, reactive } from 'vue'
import * as echarts from 'echarts'
import axiosLocal from '@/modules/axiosLocal'
import { useInterviewStore } from '@/stores/interviewStore'
import { useUserStore } from '@/stores/userStore'
import html2canvas from 'html2canvas'
import jsPDF from 'jspdf'

const userStore = useUserStore()
const interviewStore = useInterviewStore()

// 响应式数据
const reportData = ref({})
const activeTab = ref(0)
const selectedDimension = ref('')
const radarChart = ref(null)
const knowledgeChart = ref(null)
const isExporting = ref(false)
const pdfContent = ref(null)
const optimizedAnswers = reactive({})

// 分页配置 - 更新分页，在知识点分析前插入答案分析
const tabs = [
    { name: '面试概要', icon: '📊' },
    { name: '问题分析', icon: '💬' },
    { name: '答案分析', icon: '🎯' },
    { name: '知识点分析', icon: '📚' },
    { name: '智能建议', icon: '💡' },
    { name: '学习路径', icon: '🎯' },
    { name: '数据归档', icon: '📁' }
]

const parseInterviewId = (str) => {
    if (!str) return { company: '', position: '', time: '' }

    const parts = str.split('-')
    if (parts.length < 3) return { company: '', position: '', time: '' }

    const company = parts[0]
    const position = parts.slice(1, parts.length - 1).join('-')
    const rawTime = parts[parts.length - 1]

    const time = `${rawTime.slice(0, 4)}-${rawTime.slice(4, 6)}-${rawTime.slice(6, 8)} ` +
        `${rawTime.slice(8, 10)}:${rawTime.slice(10, 12)}:${rawTime.slice(12, 14)}`

    return { company, position, time }
}

const { company, position, time } = parseInterviewId(interviewStore.current_interview_id)

// 计算属性
const uniqueDimensions = computed(() => {
    if (!reportData.value.recommendations) return []
    return [...new Set(reportData.value.recommendations.map(r => r.dimension))]
})

const filteredSuggestions = computed(() => {
    if (!reportData.value.recommendations) return []
    if (!selectedDimension.value) return reportData.value.recommendations
    return reportData.value.recommendations.filter(r => r.dimension === selectedDimension.value)
})

// 获取分数等级样式
const getScoreClass = (score) => {
    if (score >= 80) return 'excellent'
    if (score >= 60) return 'good'
    return 'poor'
}

// 初始化雷达图
const initRadarChart = () => {
    if (!radarChart.value || !reportData.value.scores) return

    const chart = echarts.init(radarChart.value)
    const scores = reportData.value.scores

    const option = {
        tooltip: {
            trigger: 'item',
            formatter: (params) => {
                const labels = Object.keys(scores)
                const values = params.value
                return labels.map((label, idx) => `${label}：${values[idx]}`).join('<br/>')
            },
            backgroundColor: '#ffffff',
            borderColor: '#ccc',
            borderWidth: 1,
            textStyle: {
                color: '#333'
            }
        },
        radar: {
            indicator: Object.keys(scores).map(key => ({
                name: key,
                max: 100
            })),
            radius: '70%',
            name: {
                textStyle: {
                    color: '#333333',
                    fontSize: 14
                }
            },
            splitLine: {
                lineStyle: {
                    color: '#E7E7E7'
                }
            },
            axisLine: {
                lineStyle: {
                    color: '#E7E7E7'
                }
            }
        },
        series: [{
            type: 'radar',
            data: [{
                value: Object.values(scores),
                name: '能力评估',
                areaStyle: {
                    color: 'rgba(0, 82, 217, 0.1)'
                },
                lineStyle: {
                    color: '#0052D9',
                    width: 2
                },
                itemStyle: {
                    color: '#0052D9'
                }
            }]
        }]
    }

    chart.setOption(option)
}

// 初始化知识点图表
const initKnowledgeChart = () => {
    if (!knowledgeChart.value || !reportData.value.knowledge_analysis) return

    const chart = echarts.init(knowledgeChart.value)
    const knowledge = reportData.value.knowledge_analysis

    const getColorGradient = (score) => {
        if (score >= 90) {
            return new echarts.graphic.LinearGradient(1, 0, 0, 0, [
                { offset: 0, color: '#00D98C' },
                { offset: 1, color: '#0CA678' }
            ])
        } else if (score >= 75) {
            return new echarts.graphic.LinearGradient(1, 0, 0, 0, [
                { offset: 0, color: '#478EFF' },
                { offset: 1, color: '#7450FF' }
            ])
        } else if (score >= 60) {
            return new echarts.graphic.LinearGradient(1, 0, 0, 0, [
                { offset: 0, color: '#FFB547' },
                { offset: 1, color: '#FF8052' }
            ])
        } else {
            return new echarts.graphic.LinearGradient(1, 0, 0, 0, [
                { offset: 0, color: '#FF7A7A' },
                { offset: 1, color: '#D94063' }
            ])
        }
    }

    const option = {
        grid: {
            left: '20%',
            right: '8%',
            top: '10%',
            bottom: '10%'
        },
        tooltip: {
            trigger: 'item',
            formatter: (params) => `${params.name}<br/>掌握度：${params.value}%`
        },
        xAxis: {
            type: 'value',
            max: 100,
            axisLabel: {
                formatter: '{value}%',
                color: '#666',
                fontSize: 12
            },
            axisLine: {
                lineStyle: { color: '#E7E7E7' }
            },
            splitLine: {
                lineStyle: { color: '#F3F3F3' }
            }
        },
        yAxis: {
            type: 'category',
            data: knowledge.map(k => k.knowledge_name),
            axisLabel: {
                interval: 0,
                fontSize: 13,
                color: '#333'
            },
            axisLine: {
                lineStyle: { color: '#E7E7E7' }
            }
        },
        series: [{
            type: 'bar',
            data: knowledge.map(k => ({
                value: k.knowledge_num,
                name: k.knowledge_name,
                label: {
                    show: true,
                    position: 'right',
                    color: '#333',
                    formatter: '{c}%'
                },
                itemStyle: {
                    borderRadius: [0, 6, 6, 0],
                    color: getColorGradient(k.knowledge_num)
                }
            })),
            barWidth: '60%'
        }]
    }

    chart.setOption(option)
}

// 生成优化回答
const generateOptimizedAnswer = async (roundIndex, round) => {
    if (!optimizedAnswers[roundIndex]) {
        optimizedAnswers[roundIndex] = { loading: false, content: '' }
    }

    optimizedAnswers[roundIndex].loading = true

    try {
        let resp_data = ''
        await axiosLocal.post('/interview/optimize_answer', {
            answer: round.speaker_text,
        }).then(resp => {
            // console.log(resp.data)
            if (resp.data.code === 200) {
                resp_data = resp.data.data
            }
        })

        // 模拟流式响应
        let optimizedAnswer = ''
        // const fullAnswer = getOptimizedAnswerExample(round.ai_interviewer_text, round.speaker_text)
        const fullAnswer = resp_data

        for (let i = 0; i < fullAnswer.length; i += 3) {
            await new Promise(resolve => setTimeout(resolve, 30))
            optimizedAnswer += fullAnswer.substring(i, Math.min(i + 3, fullAnswer.length))
            optimizedAnswers[roundIndex].content = optimizedAnswer
        }

    } catch (error) {
        console.error('获取优化回答失败:', error)
        optimizedAnswers[roundIndex].content = '获取优化回答失败，请稍后重试。'
    } finally {
        optimizedAnswers[roundIndex].loading = false
    }
}

// 复制建议
const copySuggestion = (suggestion) => {
    const text = `维度：${suggestion.dimension}\n问题：${suggestion.issue}\n建议：${suggestion.suggestion}`
    navigator.clipboard.writeText(text).then(() => {
        alert('建议已复制到剪贴板')
    })
}

// 导出PDF
const exportToPDF = async () => {
    try {
        if (!pdfContent.value) {
            console.error('PDF内容未找到')
            return
        }

        const dom = pdfContent.value
        const canvas = await html2canvas(dom, {
            scale: 2,
            useCORS: true,
            allowTaint: true,
            backgroundColor: '#ffffff'
        })

        const imgData = canvas.toDataURL('image/jpeg', 1.0)
        const pdf = new jsPDF('p', 'mm', 'a4')
        const pageWidth = pdf.internal.pageSize.getWidth()
        const pageHeight = pdf.internal.pageSize.getHeight()
        const imgWidth = pageWidth
        const imgHeight = (canvas.height * pageWidth) / canvas.width

        let position = 0
        let remainingHeight = imgHeight

        while (remainingHeight > 0) {
            pdf.addImage(imgData, 'JPEG', 0, position, imgWidth, imgHeight)
            remainingHeight -= pageHeight
            if (remainingHeight > 0) {
                pdf.addPage()
                position = -remainingHeight
            }
        }

        pdf.save(`面试评测报告_${new Date().toLocaleDateString()}.pdf`)
    } catch (err) {
        console.error('导出PDF失败:', err)
    }
}

// 导出JSON
const exportToJSON = () => {
    const dataStr = JSON.stringify(reportData.value, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `interview_report_${reportData.value.interview_id}.json`
    link.click()
    URL.revokeObjectURL(url)
}

// 下载所有音频
const downloadAllAudio = () => {
    alert('音频打包下载功能开发中...')
}

// 监听activeTab变化，重新渲染图表
const handleTabChange = async () => {
    await nextTick()
    if (activeTab.value === 0) {
        initRadarChart()
    } else if (activeTab.value === 3) {
        initKnowledgeChart()
    }
}

// 监听activeTab变化
watch(() => activeTab.value, handleTabChange)

// 组件挂载
onMounted(() => {
    // console.log(interviewStore.current_interview_id)
    axiosLocal.get('/interview/get_interview_report', {
        params: {
            email: userStore.user.email,
            current_interview_id: interviewStore.current_interview_id
        }
    }).then((res) => {
        if (res.data.code == 200) {
            reportData.value = res.data.data
            console.log(reportData.value)

            interviewStore.setJobType(Number(reportData.value.job_type));

            nextTick(() => {
                initRadarChart()
            })
        }
    })
})
</script>

<style scoped>
/* TDesign 基础变量 */
:root {
    --td-brand-color: #0052D9;
    --td-brand-color-light: #E7F3FF;
    --td-success-color: #00A870;
    --td-warning-color: #ED7B2F;
    --td-error-color: #E34D59;
    --td-text-color-primary: #000000;
    --td-text-color-secondary: #666666;
    --td-text-color-placeholder: #BBBBBB;
    --td-bg-color-page: #F3F3F3;
    --td-bg-color-container: #FFFFFF;
    --td-border-color: #E7E7E7;
    --td-border-radius: 6px;
    --td-shadow-1: 0 1px 10px rgba(0, 0, 0, 0.05);
    --td-shadow-2: 0 3px 14px 2px rgba(0, 0, 0, 0.05);
    --td-shadow-3: 0 6px 30px 5px rgba(0, 0, 0, 0.05);
}

.report-container {
    padding: 0;
    min-height: calc(100vh);
    background-color: var(--td-bg-color-page);
}

.report-wrapper {
    width: 100%;
    min-width: 1400px;
    margin: 0 auto;
    background: var(--td-bg-color-container);
    border-radius: 0 0 var(--td-border-radius) var(--td-border-radius);
    box-shadow: var(--td-shadow-2);
    overflow: hidden;
}

.report-header {
    padding: 32px 24px;
    background: linear-gradient(135deg, var(--td-brand-color) 0%, #1677FF 100%);
    color: white;
}

.header-content h1 {
    margin: 0 0 16px 0;
    font-size: 28px;
    font-weight: 600;
    line-height: 1.2;
}

.report-meta {
    display: flex;
    gap: 32px;
    flex-wrap: wrap;
}

.meta-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.meta-label {
    font-size: 12px;
    opacity: 0.8;
    font-weight: 400;
}

.meta-value {
    font-size: 14px;
    font-weight: 500;
}

/* TDesign 分页导航 */
.tab-navigation {
    display: flex;
    background: var(--td-bg-color-container);
    border-bottom: 1px solid var(--td-border-color);
}

.tab-item {
    flex: 1;
    padding: 16px 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    border-bottom: 2px solid transparent;
    color: var(--td-text-color-secondary);
    font-weight: 400;
}

.tab-item:hover {
    background: var(--td-brand-color-light);
    color: var(--td-brand-color);
}

.tab-item.active {
    background: var(--td-bg-color-container);
    border-bottom-color: var(--td-brand-color);
    color: var(--td-brand-color);
    font-weight: 500;
}

.tab-icon {
    font-size: 16px;
}

.tab-text {
    font-size: 14px;
}

.tab-content {
    padding: 24px;
}

/* TDesign 卡片样式 */
.td-card {
    background: var(--td-bg-color-container);
    border-radius: var(--td-border-radius);
    border: 1px solid var(--td-border-color);
    box-shadow: var(--td-shadow-1);
    overflow: hidden;
}

.card-header {
    padding: 16px 20px;
    border-bottom: 1px solid var(--td-border-color);
    background: #FAFAFA;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.card-header h3,
.card-header h4 {
    margin: 0;
    font-size: 16px;
    font-weight: 500;
    color: var(--td-text-color-primary);
}

.card-content {
    padding: 20px;
}

/* TDesign 标签样式 */
.td-tag {
    display: inline-flex;
    align-items: center;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 12px;
    font-weight: 400;
    line-height: 20px;
}

.mbti-tag {
    background: var(--td-brand-color-light);
    color: var(--td-brand-color);
}

.ability-tag {
    background: #E8F5E8;
    color: var(--td-success-color);
}

.interviewer-tag {
    background: var(--td-brand-color-light);
    color: var(--td-brand-color);
    margin-bottom: 8px;
}

.candidate-tag {
    background: #E8F5E8;
    color: var(--td-success-color);
    margin-bottom: 8px;
}

.optimized-tag {
    background: #FFF3E0;
    color: #ED7B2F;
    margin-bottom: 8px;
}

.dimension-tag {
    background: var(--td-brand-color);
    color: white;
}

.skill-tag {
    background: #E7F3FF;
    color: var(--td-brand-color);
    margin: 4px;
}

/* 答案分析新增样式 */
.answer-analysis-section {
    max-width: 1200px;
    margin: 0 auto;
}

.section-header {
    text-align: center;
    margin-bottom: 32px;
}

.section-header h3 {
    margin: 0 0 8px 0;
    color: var(--td-text-color-primary);
    font-size: 24px;
    font-weight: 600;
}

.section-description {
    margin: 0;
    color: var(--td-text-color-secondary);
    font-size: 16px;
    line-height: 1.5;
}

/* 算法编程样式 */
.algorithm-problems {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.problem-card {
    margin-bottom: 0;
}

.problem-header {
    display: flex;
    align-items: center;
    gap: 12px;
}

.difficulty-tag {
    padding: 4px 8px;
    font-size: 11px;
    font-weight: 500;
}

.difficulty-tag.beginner {
    background: #E8F5E8;
    color: var(--td-success-color);
}

.difficulty-tag.intermediate {
    background: #FFF3E0;
    color: var(--td-warning-color);
}

.difficulty-tag.advanced {
    background: #FFE7E7;
    color: var(--td-error-color);
}

.problem-content {
    display: grid;
    gap: 20px;
}

.problem-description h5,
.problem-solution h5,
.code-example h5 {
    margin: 0 0 8px 0;
    color: var(--td-text-color-primary);
    font-size: 14px;
    font-weight: 500;
}

.problem-description p {
    margin: 0;
    color: var(--td-text-color-secondary);
    line-height: 1.6;
}

.problem-solution ul {
    margin: 0;
    padding-left: 16px;
    color: var(--td-text-color-secondary);
    line-height: 1.6;
}

.problem-solution li {
    margin-bottom: 4px;
}

.code-block {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 16px;
    border-radius: var(--td-border-radius);
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 13px;
    line-height: 1.4;
    overflow-x: auto;
    margin: 0;
}

/* DevOps样式 */
.devops-scenarios {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.scenario-card {
    margin-bottom: 0;
}

.process-flow {
    display: flex;
    flex-direction: column;
    gap: 16px;
    align-items: center;
}

.flow-step {
    display: flex;
    align-items: center;
    gap: 16px;
    background: #FAFAFA;
    padding: 16px;
    border-radius: var(--td-border-radius);
    border: 1px solid #F3F3F3;
    width: 100%;
    max-width: 600px;
}

.step-number {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--td-brand-color);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 14px;
    flex-shrink: 0;
}

.step-content h5 {
    margin: 0 0 4px 0;
    color: var(--td-text-color-primary);
    font-size: 14px;
    font-weight: 500;
}

.step-content p {
    margin: 0;
    color: var(--td-text-color-secondary);
    font-size: 13px;
    line-height: 1.4;
}

.flow-arrow {
    color: var(--td-brand-color);
    font-size: 20px;
    font-weight: bold;
}

.scenario-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
}

.scenario-item {
    background: #FAFAFA;
    padding: 16px;
    border-radius: var(--td-border-radius);
    border: 1px solid #F3F3F3;
}

.scenario-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}

.scenario-icon {
    font-size: 16px;
}

.scenario-header h5 {
    margin: 0;
    color: var(--td-text-color-primary);
    font-size: 14px;
    font-weight: 500;
}

.scenario-actions {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.action-item {
    padding: 8px 12px;
    border-radius: var(--td-border-radius);
    font-size: 12px;
    line-height: 1.4;
    border-left: 3px solid;
}

.action-item.priority-high {
    background: #FFE7E7;
    border-left-color: var(--td-error-color);
    color: var(--td-error-color);
}

.action-item.priority-medium {
    background: #FFF3E0;
    border-left-color: var(--td-warning-color);
    color: var(--td-warning-color);
}

.action-item.priority-low {
    background: #E8F5E8;
    border-left-color: var(--td-success-color);
    color: var(--td-success-color);
}

/* 产品设计样式 */
.product-design {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.solution-content {
    display: grid;
    gap: 20px;
}

.solution-overview h5 {
    margin: 0 0 8px 0;
    color: var(--td-text-color-primary);
    font-size: 16px;
    font-weight: 500;
}

.solution-overview p {
    margin: 0;
    color: var(--td-text-color-secondary);
    line-height: 1.6;
}

.design-principles h5 {
    margin: 0 0 16px 0;
    color: var(--td-text-color-primary);
    font-size: 14px;
    font-weight: 500;
}

.principles-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
}

.principle-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: #FAFAFA;
    padding: 12px;
    border-radius: var(--td-border-radius);
    border: 1px solid #F3F3F3;
}

.principle-icon {
    font-size: 16px;
    flex-shrink: 0;
}

.principle-content h6 {
    margin: 0 0 4px 0;
    color: var(--td-text-color-primary);
    font-size: 13px;
    font-weight: 500;
}

.principle-content p {
    margin: 0;
    color: var(--td-text-color-secondary);
    font-size: 12px;
    line-height: 1.4;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.feature-category h5 {
    margin: 0 0 12px 0;
    color: var(--td-text-color-primary);
    font-size: 14px;
    font-weight: 500;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--td-brand-color);
}

.feature-list {
    margin: 0;
    padding-left: 16px;
    color: var(--td-text-color-secondary);
    line-height: 1.6;
}

.feature-list li {
    margin-bottom: 6px;
    font-size: 13px;
}

.flowchart-container {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.flow-section h5 {
    margin: 0 0 16px 0;
    color: var(--td-text-color-primary);
    font-size: 14px;
    font-weight: 500;
    text-align: center;
}

.flow-steps.horizontal {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    flex-wrap: wrap;
}

.step-box {
    background: var(--td-brand-color-light);
    color: var(--td-brand-color);
    padding: 8px 12px;
    border-radius: var(--td-border-radius);
    font-size: 12px;
    font-weight: 500;
    white-space: nowrap;
    border: 1px solid #CCE7FF;
}

.flow-arrow-right {
    color: var(--td-brand-color);
    font-size: 16px;
    font-weight: bold;
}

/* TDesign 按钮样式 */
.td-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 8px 16px;
    border: 1px solid var(--td-border-color);
    border-radius: var(--td-border-radius);
    background: var(--td-bg-color-container);
    color: var(--td-text-color-primary);
    font-size: 14px;
    font-weight: 400;
    cursor: pointer;
    transition: all 0.2s ease;
    text-decoration: none;
}

.td-button:hover {
    border-color: var(--td-brand-color);
    color: var(--td-brand-color);
}

.primary-button {
    background: var(--td-brand-color);
    border-color: var(--td-brand-color);
    color: white;
}

.primary-button:hover {
    background: #1677FF;
    border-color: #1677FF;
    color: white;
}

.secondary-button {
    background: var(--td-bg-color-container);
    border-color: var(--td-border-color);
    color: var(--td-text-color-primary);
}

.optimize-button {
    background: #FFF3E0;
    border-color: #ED7B2F;
    color: #ED7B2F;
    font-size: 12px;
    padding: 6px 12px;
}

.optimize-button:hover {
    background: #ED7B2F;
    border-color: #ED7B2F;
    color: white;
}

.icon-button {
    padding: 8px;
    min-width: auto;
}

.filter-button {
    padding: 6px 12px;
    font-size: 12px;
}

.filter-button.active {
    background: var(--td-brand-color);
    border-color: var(--td-brand-color);
    color: white;
}

.full-width {
    width: 100%;
}

/* 概要页面样式 */
.overview-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}

.info-item {
    display: flex;
    align-items: flex-start;
    margin-bottom: 16px;
    gap: 16px;
}

.summary-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
}

.info-label {
    font-weight: 500;
    color: var(--td-text-color-secondary);
    min-width: 80px;
    font-size: 14px;
}

.score-display {
    display: flex;
    align-items: center;
    gap: 16px;
    flex: 1;
}

.score-number {
    font-size: 32px;
    font-weight: 600;
    color: var(--td-brand-color);
    line-height: 1;
}

.score-progress {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 8px;
}

.score-track {
    flex: 1;
    height: 8px;
    background: #F3F3F3;
    border-radius: 4px;
    overflow: hidden;
}

.score-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--td-error-color), var(--td-warning-color), var(--td-success-color));
    transition: width 0.3s ease;
    border-radius: 4px;
}

.score-text {
    font-size: 12px;
    color: var(--td-text-color-secondary);
    font-weight: 500;
}

.summary-text {
    margin: 0;
    line-height: 1.6;
    color: var(--td-text-color-primary);
    font-size: 14px;
}

.radar-chart,
.knowledge-chart {
    height: 300px;
    width: 100%;
}

.abilities-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.ability-item {
    padding: 16px;
    background: #FAFAFA;
    border-radius: var(--td-border-radius);
    border: 1px solid #F3F3F3;
}

.ability-header {
    margin-bottom: 8px;
}

.ability-evidence {
    margin: 0;
    color: var(--td-text-color-secondary);
    font-size: 14px;
    line-height: 1.5;
}

.multimodal-grid {
    display: grid;
    gap: 16px;
}

.modal-item {
    padding: 16px;
    background: #FAFAFA;
    border-radius: var(--td-border-radius);
    border: 1px solid #F3F3F3;
}

.modal-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--td-text-color-primary);
}

.modal-icon {
    font-size: 16px;
}

.modal-title {
    font-size: 14px;
}

.modal-content {
    margin: 0;
    color: var(--td-text-color-secondary);
    font-size: 14px;
    line-height: 1.5;
}

/* 问题分析样式 */
.rounds-list {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.td-audio {
    height: 32px;
}

.qa-section {
    margin-bottom: 20px;
}

.question-block,
.answer-block,
.optimized-answer-block {
    margin-bottom: 16px;
}

.optimized-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}

.optimized-loading {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    background: #FFF3E0;
    border-radius: var(--td-border-radius);
    border: 1px solid #FFE0B2;
    color: #ED7B2F;
    font-size: 14px;
}

.loading-dots {
    display: flex;
    gap: 4px;
}

.loading-dots span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #ED7B2F;
    animation: loading 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) {
    animation-delay: -0.32s;
}

.loading-dots span:nth-child(2) {
    animation-delay: -0.16s;
}

@keyframes loading {

    0%,
    80%,
    100% {
        transform: scale(0);
    }

    40% {
        transform: scale(1);
    }
}

.message-bubble {
    background: #FAFAFA;
    padding: 12px 16px;
    border-radius: var(--td-border-radius);
    line-height: 1.6;
    color: var(--td-text-color-primary);
    font-size: 14px;
    border: 1px solid #F3F3F3;
}

.interviewer-bubble {
    background: var(--td-brand-color-light);
    border-color: #CCE7FF;
}

.candidate-bubble {
    background: #E8F5E8;
    border-color: #CCE7CC;
}

.optimized-bubble {
    background: #FFF3E0;
    border-color: #FFE0B2;
    white-space: pre-wrap;
}

/* 问题知识点分析样式 */
.question-analysis-section {
    background: #F0F8FF;
    border-radius: var(--td-border-radius);
    padding: 16px;
    margin-bottom: 16px;
    border: 1px solid #CCE7FF;
}

.question-analysis-content {
    background: var(--td-bg-color-container);
    padding: 12px;
    border-radius: var(--td-border-radius);
    border: 1px solid var(--td-border-color);
}

.analysis-section {
    background: #FAFAFA;
    border-radius: var(--td-border-radius);
    padding: 16px;
    border: 1px solid #F3F3F3;
}

.analysis-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 16px;
}

.analysis-item {
    background: var(--td-bg-color-container);
    padding: 12px;
    border-radius: var(--td-border-radius);
    border: 1px solid var(--td-border-color);
}

.analysis-header {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--td-text-color-primary);
}

.analysis-icon {
    font-size: 14px;
}

.analysis-title {
    font-size: 12px;
}

.analysis-content {
    margin: 0;
    font-size: 12px;
    line-height: 1.5;
    color: var(--td-text-color-secondary);
}

/* 知识点分析样式 */
.knowledge-section {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 24px;
}

.knowledge-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.knowledge-item {
    padding: 16px;
    background: #FAFAFA;
    border-radius: var(--td-border-radius);
    border: 1px solid #F3F3F3;
}

.knowledge-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.knowledge-name {
    font-weight: 500;
    color: var(--td-text-color-primary);
    font-size: 14px;
}

.knowledge-score {
    font-weight: 600;
    font-size: 14px;
}

.knowledge-score.excellent {
    color: var(--td-success-color);
}

.knowledge-score.good {
    color: var(--td-warning-color);
}

.knowledge-score.poor {
    color: var(--td-error-color);
}

.td-progress {
    width: 100%;
}

.progress-track {
    width: 100%;
    height: 6px;
    background: #F3F3F3;
    border-radius: 3px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    transition: width 0.3s ease;
    border-radius: 3px;
}

.progress-fill.excellent {
    background: var(--td-success-color);
}

.progress-fill.good {
    background: var(--td-warning-color);
}

.progress-fill.poor {
    background: var(--td-error-color);
}

/* 建议页面样式 */
.suggestions-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.suggestions-header h3 {
    margin: 0;
    color: var(--td-text-color-primary);
    font-size: 18px;
    font-weight: 500;
}

.filter-group {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.suggestions-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.suggestion-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.suggestion-block {
    background: #FAFAFA;
    padding: 16px;
    border-radius: var(--td-border-radius);
    border: 1px solid #F3F3F3;
}

.block-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--td-text-color-primary);
}

.block-icon {
    font-size: 14px;
}

.block-title {
    font-size: 14px;
}

.block-content {
    margin: 0;
    line-height: 1.6;
    color: var(--td-text-color-secondary);
    font-size: 14px;
}

/* 学习路径样式 */
.learning-path-section {
    max-width: 1200px;
    margin: 0 auto;
}

.learning-path-header {
    text-align: center;
    margin-bottom: 32px;
}

.learning-path-header h3 {
    margin: 0 0 8px 0;
    color: var(--td-text-color-primary);
    font-size: 24px;
    font-weight: 600;
}

.learning-path-description {
    margin: 0;
    color: var(--td-text-color-secondary);
    font-size: 16px;
    line-height: 1.5;
}

.learning-stages {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.learning-stage-card {
    position: relative;
}

.stage-header {
    display: flex;
    align-items: center;
    gap: 16px;
}

.stage-number {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: var(--td-brand-color);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 16px;
}

.stage-header h4 {
    margin: 0;
    color: var(--td-text-color-primary);
    font-size: 18px;
    font-weight: 500;
}

.learning-content-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

.learning-block {
    background: #FAFAFA;
    padding: 16px;
    border-radius: var(--td-border-radius);
    border: 1px solid #F3F3F3;
}

.resources-block {
    grid-column: 1 / -1;
}

.skill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 8px;
}

.improvement-list,
.practice-list {
    margin: 8px 0 0 0;
    padding-left: 16px;
    color: var(--td-text-color-secondary);
    font-size: 14px;
    line-height: 1.6;
}

.improvement-list li,
.practice-list li {
    margin-bottom: 4px;
}

.resources-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 12px;
    margin-top: 8px;
}

.resource-item {
    background: var(--td-bg-color-container);
    border-radius: var(--td-border-radius);
    border: 1px solid var(--td-border-color);
    overflow: hidden;
    transition: all 0.2s ease;
}

.resource-item:hover {
    border-color: var(--td-brand-color);
    box-shadow: var(--td-shadow-1);
}

.resource-link {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    text-decoration: none;
    color: var(--td-text-color-primary);
    transition: all 0.2s ease;
}

.resource-link:hover {
    color: var(--td-brand-color);
}

.resource-name {
    font-size: 14px;
    font-weight: 500;
}

.resource-icon {
    font-size: 12px;
    opacity: 0.6;
}

/* 导出页面样式 */
.export-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}

.json-card {
    grid-column: 1 / -1;
}

.export-actions {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.audio-list {
    margin-bottom: 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.audio-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    background: #FAFAFA;
    border-radius: var(--td-border-radius);
    border: 1px solid #F3F3F3;
}

.audio-name {
    font-size: 14px;
    color: var(--td-text-color-primary);
}

.td-link {
    color: var(--td-brand-color);
    text-decoration: none;
    font-size: 12px;
    font-weight: 500;
}

.td-link:hover {
    text-decoration: underline;
}

.json-viewer {
    background: #FAFAFA;
    border-radius: var(--td-border-radius);
    padding: 16px;
    max-height: 400px;
    overflow: auto;
    border: 1px solid #F3F3F3;
}

.json-viewer pre {
    margin: 0;
    font-size: 12px;
    line-height: 1.4;
    color: var(--td-text-color-secondary);
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.button-icon {
    font-size: 14px;
}

/* PDF内容样式 */
.pdf-content {
    font-family: Arial, sans-serif !important;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .report-container {
        padding: 0;
    }

    .overview-grid {
        grid-template-columns: 1fr;
    }

    .knowledge-section {
        grid-template-columns: 1fr;
    }

    .export-grid {
        grid-template-columns: 1fr;
    }

    .suggestion-grid {
        grid-template-columns: 1fr;
    }

    .analysis-grid {
        grid-template-columns: 1fr;
    }

    .learning-content-grid {
        grid-template-columns: 1fr;
    }

    .resources-list {
        grid-template-columns: 1fr;
    }

    .tab-navigation {
        flex-wrap: wrap;
    }

    .tab-item {
        flex: none;
        min-width: 120px;
    }

    .report-meta {
        gap: 16px;
    }

    .filter-group {
        flex-direction: column;
        align-items: stretch;
    }

    .features-grid {
        grid-template-columns: 1fr;
    }

    .principles-grid {
        grid-template-columns: 1fr;
    }

    .flow-steps.horizontal {
        flex-direction: column;
        gap: 8px;
    }

    .flow-arrow-right {
        transform: rotate(90deg);
    }

    .scenario-grid {
        grid-template-columns: 1fr;
    }
}
</style>