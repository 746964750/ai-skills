<template>
  <div id="total-layout" class="wms-management">
    <div class="preview-note">BYD WMS 管理端样式基准 · 演示数据 · 不连接业务后端</div>
    <QueryTablePage
      v-model:query="query"
      v-model:page="page"
      v-model:page-size="pageSize"
      title="基础信息查询"
      :fields="fields"
      :columns="columns"
      :rows="pageRows"
      :total="filtered.length"
      :actions="actions"
      selectable
      @search="search"
      @reset="reset"
      @action="handleAction"
    />
    <EditDialog v-model="editVisible" v-model:model="editModel" :rules="rules" @save="saveDemo" />
    <DetailDrawer v-model="drawerVisible" :record="records[0]" :details="records.slice(0, 4)" />
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { Plus, View, Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import QueryTablePage from '../templates/QueryTablePage.vue'
import EditDialog from '../templates/EditDialog.vue'
import DetailDrawer from '../templates/DetailDrawer.vue'
const query = ref({ code: '', name: '', enabled: '' })
const applied = ref({ ...query.value })
const page = ref(1)
const pageSize = ref(20)
const editVisible = ref(false)
const drawerVisible = ref(false)
const editModel = ref({ code: '', name: '' })
const records = Array.from({ length: 24 }, (_, i) => ({ id: i + 1, code: 'DEMO-' + String(i + 1).padStart(3, '0'), name: '演示信息 ' + (i + 1), enabled: i % 2 === 0, remark: '仅用于样式和交互演示' }))
const fields = [
  { key: 'code', label: '英文名称', placeholder: '请输入编号' },
  { key: 'name', label: '中文名称', placeholder: '请输入名称' },
  { key: 'enabled', label: '是否启用', options: [{ label: '启用', value: true }, { label: '停用', value: false }] }
]
const columns = [
  { prop: 'code', label: '英文名称', width: 180 },
  { prop: 'name', label: '中文名称', width: 220 },
  { prop: 'remark', label: '备注说明', width: 320 }
]
const actions = [
  { key: 'drawer', label: '查看演示抽屉', icon: View, type: 'primary' },
  { key: 'add', label: '新增', icon: Plus, type: 'primary' },
  { key: 'delete', label: '删除', icon: Delete, type: 'danger', disabled: true }
]
const filtered = computed(() => records.filter(row => row.code.includes(applied.value.code) && row.name.includes(applied.value.name) && (applied.value.enabled === '' || applied.value.enabled == null || row.enabled === applied.value.enabled)))
const pageRows = computed(() => filtered.value.slice((page.value - 1) * pageSize.value, page.value * pageSize.value))
const rules = { code: [{ required: true, message: '请输入编号', trigger: 'blur' }], name: [{ required: true, message: '请输入名称', trigger: 'blur' }] }
function search() { applied.value = { ...query.value }; page.value = 1 }
function reset() { query.value = { code: '', name: '', enabled: '' }; search() }
function handleAction(action) {
  if (action.key === 'drawer') drawerVisible.value = true
  if (action.key === 'add') { editModel.value = { code: '', name: '' }; editVisible.value = true }
}
function saveDemo() { ElMessage.success('演示校验通过，未提交业务数据'); editVisible.value = false }
</script>

<style>
html, body, #app { min-height: 100%; margin: 0; }
* { box-sizing: border-box; }
.preview-note { padding: 12px 16px; background: #1758a7; color: white; font: 14px "Microsoft YaHei", sans-serif; }
</style>
