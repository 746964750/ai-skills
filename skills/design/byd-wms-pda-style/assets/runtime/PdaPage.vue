<template>
  <el-container class="pda-page" direction="vertical">
    <el-header class="pda-page__header" height="auto">
      <el-page-header :title="$tx('返回首页')" @back="$emit('back')">
        <template #content>
          <h1>{{ title }}</h1>
        </template>
      </el-page-header>
      <span class="pda-page__badge" aria-hidden="true">PDA</span>
    </el-header>
    <el-main class="body pda-page__body">
      <el-card class="pda-page__panel" shadow="never">
        <slot />
      </el-card>
    </el-main>
    <el-footer
      v-if="$slots.actions"
      class="subBtn pda-page__actions"
      height="auto"
    >
      <div class="pda-page__action-inner">
        <slot name="actions" />
      </div>
    </el-footer>
  </el-container>
</template>
<script>
export default {
  name: 'PdaPage',
  props: { title: { type: String, required: true }},
  emits: ['back']
}
</script>
