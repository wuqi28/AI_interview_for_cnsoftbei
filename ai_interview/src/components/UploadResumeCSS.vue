<template>
  <t-card>
    <template #header>
      <div class="upload-header">
        <div class="upload-icon">📤</div>
        <div class="upload-title">手动上传简历</div>
      </div>
    </template>

    <div class="upload-content">
      <div class="upload-description">
        已有简历？直接上传PDF文件，系统将自动解析并为您提供智能优化建议。
      </div>

      <div class="upload-wrapper">
      </div>

      <div class="upload-features">
        <div class="feature-item">
          <div class="feature-icon">🔍</div>
          <div class="feature-text">智能解析</div>
        </div>
        <div class="feature-item">
          <div class="feature-icon">🎯</div>
          <div class="feature-text">精准优化</div>
        </div>
        <div class="feature-item">
          <div class="feature-icon">📊</div>
          <div class="feature-text">简历画像</div>
        </div>
      </div>
    </div>
  </t-card>
</template>

<style scoped>
/* ------------------------------------------------------------手动上传简历------------------------------------------------------------ */
.upload-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.upload-icon {
  font-size: 20px;
}

.upload-title {
  font-size: 16px;
  font-weight: 600;
  color: #0052D9;
}

.upload-content {
  padding: 0;
}

.upload-description {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 20px;
  padding: 12px;
  background: linear-gradient(135deg, #fff8f0 0%, #fff2e8 100%);
  border-radius: 6px;
  border-left: 3px solid #ff7d00;
}

.upload-wrapper {
  margin-bottom: 20px;
}

.custom-upload {
  width: 100%;
}

.upload-drag-content {
  padding: 40px 20px;
  text-align: center;
  background: linear-gradient(135deg, #fafbff 0%, #f0f4ff 100%);
  border: 2px dashed #d0d7ff;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.upload-drag-content:hover {
  border-color: #0052D9;
  background: linear-gradient(135deg, #f8f9ff 0%, #e8f2ff 100%);
}

.upload-drag-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.8;
}

.upload-drag-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.upload-drag-subtitle {
  font-size: 14px;
  color: #666;
  margin-bottom: 16px;
}

.upload-drag-tips {
  display: flex;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.tip-item {
  font-size: 12px;
  color: #0052D9;
  background: rgba(0, 82, 217, 0.1);
  padding: 4px 8px;
  border-radius: 12px;
}

.upload-features {
  display: flex;
  justify-content: space-around;
  padding: 16px 0;
  border-top: 1px solid #eee;
}

.upload-features .feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.upload-features .feature-icon {
  font-size: 20px;
}

.upload-features .feature-text {
  font-size: 12px;
  color: #666;
  text-align: center;
}

/* 覆盖默认上传组件样式 */
:deep(.t-upload__dragger) {
  border: none !important;
  background: none !important;
  padding: 0 !important;
}

:deep(.t-upload__dragger-center) {
  display: none !important;
}

:deep(.t-upload__dragger-text) {
  display: none !important;
}

/* 上传成功状态 */
:deep(.t-upload--success .upload-drag-content) {
  border-color: #52c41a;
  background: linear-gradient(135deg, #f6ffed 0%, #f0f9e8 100%);
}

/* 上传错误状态 */
:deep(.t-upload--error .upload-drag-content) {
  border-color: #ff4d4f;
  background: linear-gradient(135deg, #fff2f0 0%, #ffece8 100%);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .upload-drag-content {
    padding: 30px 15px;
  }

  .upload-drag-icon {
    font-size: 36px;
  }

  .upload-drag-tips {
    flex-direction: column;
    gap: 8px;
  }

  .upload-features {
    flex-direction: column;
    gap: 12px;
  }

  .upload-features .feature-item {
    flex-direction: row;
    justify-content: flex-start;
  }

  .upload-features .feature-text {
    text-align: left;
  }
}
</style>
