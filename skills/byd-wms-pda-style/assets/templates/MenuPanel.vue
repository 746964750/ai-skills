<template>
  <el-container class="menubox" direction="vertical">
    <el-header class="menuheader" height="auto">
      <div class="menu-brand">
        <div class="menu-caption">WMS / PDA</div>
        <h1>{{ title }}</h1>
      </div>
      <slot name="language" />
    </el-header>
    <el-main class="menubody">
      <div class="menu-content">
        <div class="menu-intro">
          <h2>{{ $tx('选择作业') }}</h2>
          <el-tag type="info" effect="plain">{{ $tx('手持终端') }}</el-tag>
        </div>
        <el-skeleton v-if="loading" :rows="6" :aria-label="$tx('正在加载菜单')" animated />
        <div v-else-if="error" class="menu-state" role="alert">
          <el-result icon="warning" :title="$tx('菜单加载失败')" :sub-title="$tx('请检查网络后重试')" />
          <el-button type="primary" @click="$emit('retry')">{{ $tx('重新加载') }}</el-button>
        </div>
        <div v-else-if="items.length" class="menu-grid">
          <el-button v-for="item in items" :key="item.id" class="menu-entry" @click="$emit('select', item)">
            <el-icon aria-hidden="true"><component :is="item.icon || Grid" /></el-icon>
            <span class="item_text">{{ item.name }}</span>
          </el-button>
        </div>
        <el-empty v-else :description="$tx('暂无可用作业，请联系管理员')" />
      </div>
    </el-main>
  </el-container>
</template>
<script>
import { markRaw } from 'vue'
import { Grid } from '@element-plus/icons-vue'

export default {
  name: 'PdaMenuTemplate',
  props: {
    title: { type: String, required: true },
    items: { type: Array, default: () => [] },
    loading: { type: Boolean, default: false },
    error: { type: Boolean, default: false }
  },
  emits: ['retry', 'select'],
  data: () => ({ Grid: markRaw(Grid) })
}
</script>
