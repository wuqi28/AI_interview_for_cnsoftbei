<template>
    <div class="interview-report">
        <!-- <topNav /> -->
        <!-- 报告容器 -->
        <div class="report-container">
            <div class="report-wrapper">
                <!-- 页面标题 -->
                <div class="report-header">
                    <div class="header-content">
                        <h1>{{ company }}-{{ position }}  面试评测报告</h1>
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
                                            <div class="message-bubble interviewer-bubble">{{ round.ai_interviewer_text }}</div>
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
                                                    @click="generateOptimizedAnswer(roundIndex, round)"
                                                >
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
                                            <div 
                                                v-if="optimizedAnswers[roundIndex]?.content" 
                                                class="message-bubble optimized-bubble"
                                            >
                                                {{ optimizedAnswers[roundIndex].content }}
                                            </div>
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

                    <!-- 知识点分析 -->
                    <div v-if="activeTab === 2" class="knowledge-section">
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
                    <div v-if="activeTab === 3" class="suggestions-section">
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

                    <!-- 数据归档 -->
                    <div v-if="activeTab === 4" class="export-section">
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

                            <div class="td-card json-card">
                                <div class="card-header">
                                    <h3>🔍 原始数据预览</h3>
                                </div>
                                <div class="card-content">
                                    <div class="json-viewer">
                                        <pre>{{ JSON.stringify(reportData, null, 2) }}</pre>
                                    </div>
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
                        <h1 style="margin: 0; font-size: 32px; font-weight: 600;">{{ company }}-{{ position }} 面试评测报告</h1>
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
                    <div style="display: grid; grid-template-columns: 1fr; gap: 16px;">
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

// 分页配置
const tabs = [
    { name: '面试概要', icon: '📊' },
    { name: '问题分析', icon: '💬' },
    { name: '知识点分析', icon: '📚' },
    { name: '智能建议', icon: '💡' },
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
    } else if (activeTab.value === 2) {
        initKnowledgeChart()
    }
}

// 监听activeTab变化
watch(() => activeTab.value, handleTabChange)

// const { company, position, time } = parseInterviewId(interviewStore.current_interview_id)

// 组件挂载
onMounted(() => {
    axiosLocal.get('/interview/get_interview_report', {
        params: {
            email: userStore.user.email,
            current_interview_id: interviewStore.current_interview_id
        }
    }).then((res) => {
        if (res.data.code == 200) {
            reportData.value = res.data.data
            console.log(reportData.value)

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
    0%, 80%, 100% {
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
}
</style>