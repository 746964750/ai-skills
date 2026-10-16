<template>
  <main class="wms-page">
    <section class="wms-search">
      <el-card class="wms-card" shadow="never">
        <template #header>
          <div class="card_header">
            <div class="left"><h2 class="card-title">{{ title }}</h2></div>
            <div class="card-btn">
              <el-button size="small" type="primary" :icon="Search" :loading="loading" @click="emit('search')">{{ labels.search }}</el-button>
              <el-button size="small" :icon="Refresh" :disabled="loading" @click="emit('reset')">{{ labels.reset }}</el-button>
            </div>
          </div>
        </template>
        <div class="SearchcardBody card_body">
          <div class="formDiv">
            <el-form :model="query" inline size="default">
              <el-row>
                <el-col v-for="field in fields" :key="field.key">
                  <div class="el-col-div">
                    <el-form-item :label="field.label" :prop="field.key" size="default">
                      <el-select
                        v-if="field.options"
                        :model-value="query[field.key]"
                        size="default"
                        clearable
                        popper-class="wms-popper"
                        :placeholder="field.placeholder"
                        @update:model-value="value => updateQuery(field.key, value)"
                      >
                        <el-option v-for="option in field.options" :key="typeof option.value + ':' + String(option.value)" :label="option.label" :value="option.value" />
                      </el-select>
                      <el-input
                        v-else
                        :model-value="query[field.key]"
                        size="default"
                        clearable
                        :placeholder="field.placeholder"
                        @update:model-value="value => updateQuery(field.key, value)"
                        @keyup.enter="emit('search')"
                      />
                    </el-form-item>
                  </div>
                </el-col>
              </el-row>
            </el-form>
          </div>
        </div>
      </el-card>
    </section>
    <section class="wms-grid">
      <el-card class="wms-card" shadow="never">
        <template #header>
          <div class="card_header">
            <div class="left"><h2 class="card-title">{{ labels.table }}</h2></div>
            <div class="card-btn">
              <el-button
                v-for="action in visibleActions"
                :key="action.key || action.pkId"
                size="small"
                :type="typeFor(action)"
                :icon="iconFor(action)"
                :loading="action.loading"
                :disabled="action.disabled"
                @click="emit('action', action)"
              >{{ labelFor(action) }}</el-button>
            </div>
          </div>
        </template>
        <div class="card_body">
          <el-table
            ref="tableRef"
            v-loading="loading"
            :data="rows"
            :row-key="rowKey"
            size="small"
            stripe
            border
            @selection-change="value => emit('selection-change', value)"
            @sort-change="value => emit('sort-change', value)"
          >
            <el-table-column v-if="selectable" type="selection" width="40" align="center" header-align="center" fixed="left" />
            <el-table-column v-if="showIndex" :label="labels.index" type="index" width="40" align="center" header-align="center" class-name="wms-index-column" fixed="left" />
            <el-table-column
              v-for="column in columns"
              :key="column.prop"
              :prop="column.prop"
              :label="column.label"
              :min-width="column.width || 140"
              :align="column.align || 'left'"
              :sortable="column.sortable || false"
              :show-overflow-tooltip="true"
            />
            <template #empty><el-empty :description="labels.empty" /></template>
          </el-table>
          <el-pagination
            :current-page="page"
            :page-size="pageSize"
            :total="total ?? 0"
            :page-sizes="pageSizes"
            layout="total, sizes, prev, pager, next, jumper"
            background
            popper-class="wms-popper"
            @update:current-page="value => emit('update:page', value)"
            @update:page-size="value => emit('update:pageSize', value)"
          />
        </div>
      </el-card>
    </section>
  </main>
</template>

<script setup>
import { computed, ref } from 'vue'
import { Search, Refresh } from '@element-plus/icons-vue'

const props = defineProps({
  title: { type: String, required: true },
  query: { type: Object, required: true },
  fields: { type: Array, required: true },
  columns: { type: Array, required: true },
  rows: { type: Array, default: () => [] },
  actions: { type: Array, default: () => [] },
  labelFor: { type: Function, default: action => action.label || '' },
  typeFor: { type: Function, default: action => action.type || 'primary' },
  iconFor: { type: Function, default: action => action.icon },
  rowKey: { type: String, default: 'id' },
  selectable: { type: Boolean, default: false },
  showIndex: { type: Boolean, default: true },
  loading: { type: Boolean, default: false },
  total: { type: Number, default: 0 },
  page: { type: Number, default: 1 },
  pageSize: { type: Number, default: 20 },
  pageSizes: { type: Array, default: () => [10, 20, 50, 100] },
  labels: { type: Object, default: () => ({ search: '查询', reset: '重置', table: '数据表格', index: '序号', empty: '暂无数据' }) }
})
const emit = defineEmits(['update:query', 'search', 'reset', 'action', 'selection-change', 'sort-change', 'update:page', 'update:pageSize'])
const visibleActions = computed(() => props.actions.filter(action => typeof props.labelFor(action) === 'string' && props.labelFor(action).trim()))
const tableRef = ref()
const updateQuery = (key, value) => emit('update:query', { ...props.query, [key]: value })
// Parent owns data fetching, permissions, validation and paging reset semantics.
defineExpose({ tableRef })
</script>
