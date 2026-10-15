<template>
  <PdaPage :title="title" @back="$emit('back')">
    <div class="itemLine">
      <el-input
        ref="query"
        v-model="query"
        :aria-label="$tx('请输入物料编号')"
        :placeholder="$tx('请输入物料编号')"
        clearable
        @keyup.enter="search(1)"
      />
      <el-button :loading="loading" type="primary" @click="search(1)">{{ $tx('查询') }}</el-button>
    </div>
    <div class="table-box">
      <el-table v-loading="loading" :data="rows" stripe border>
        <el-table-column type="index" :label="$tx('序号')" width="60" />
        <el-table-column prop="code" :label="$tx('物料编号')" min-width="120" />
        <el-table-column prop="name" :label="$tx('物料名称')" min-width="160" />
        <el-table-column prop="qty" :label="$tx('数量')" min-width="80" />
      </el-table>
      <el-pagination
        :current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        :disabled="loading"
        background
        layout="total, prev, jumper, next"
        @update:current-page="search"
      />
    </div>
    <template #actions>
      <el-button @click="$emit('back')">{{ $tx('返回首页') }}</el-button>
    </template>
  </PdaPage>
</template>
<script>
export default {
  name: 'PdaQueryTemplate',
  props: {
    title: { type: String, required: true },
    loading: { type: Boolean, default: false },
    rows: { type: Array, default: () => [] },
    total: { type: Number, default: 0 },
    currentPage: { type: Number, default: 1 },
    pageSize: { type: Number, default: 5 }
  },
  emits: ['back', 'search', 'update:currentPage'],
  data: () => ({ query: '' }),
  mounted() { this.$refs.query.focus() },
  methods: {
    search(page = 1) {
      if (this.loading) return
      this.$emit('update:currentPage', page)
      this.$emit('search', { query: this.query, page, size: this.pageSize })
    }
  }
}
</script>
