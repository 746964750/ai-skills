<template>
  <el-drawer
    :model-value="modelValue"
    :title="labels.title"
    :size="'min(720px, calc(100vw - 24px))'"
    class="wms-drawer"
    @update:model-value="value => emit('update:modelValue', value)"
  >
    <section class="wms-detail-section">
      <h3 class="wms-detail-title">{{ labels.basic }}</h3>
      <el-descriptions :column="1" border>
        <el-descriptions-item :label="labels.code">{{ record.code }}</el-descriptions-item>
        <el-descriptions-item :label="labels.name">{{ record.name }}</el-descriptions-item>
      </el-descriptions>
    </section>
    <section class="wms-detail-section">
      <h3 class="wms-detail-title">{{ labels.details }}</h3>
      <el-table :data="details" size="small" border stripe>
        <el-table-column type="index" :label="labels.index" width="40" align="center" header-align="center" class-name="wms-index-column" />
        <el-table-column prop="code" :label="labels.code" min-width="180" />
        <el-table-column prop="name" :label="labels.name" min-width="240" show-overflow-tooltip />
      </el-table>
    </section>
    <template #footer>
      <div class="dialog-footer"><el-button size="default" @click="emit('update:modelValue', false)">{{ labels.close }}</el-button></div>
    </template>
  </el-drawer>
</template>

<script setup>
defineProps({
  modelValue: Boolean,
  record: { type: Object, default: () => ({}) },
  details: { type: Array, default: () => [] },
  labels: { type: Object, default: () => ({ title: '详情', basic: '基础信息', details: '明细', code: '编号', name: '名称', index: '序号', close: '关闭' }) }
})
const emit = defineEmits(['update:modelValue'])
</script>
