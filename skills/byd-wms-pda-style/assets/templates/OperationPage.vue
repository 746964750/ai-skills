<template>
  <PdaPage :title="title" @back="$emit('back')">
    <div class="itemLine">
      <span class="itemName">{{ $tx('工装车编码:') }}</span>
      <el-input
        ref="trayCode"
        v-model="trayCode"
        :aria-label="$tx('工装车编码:')"
        :placeholder="$tx('请扫描工装车编码')"
        clearable
        @keyup.enter="$emit('scan-tray', trayCode)"
      />
    </div>
    <div class="itemLine">
      <span class="itemName">{{ $tx('物料条码:') }}</span>
      <el-input
        ref="barcode"
        v-model="barcode"
        :aria-label="$tx('物料条码:')"
        :placeholder="$tx('请扫描物料条码')"
        clearable
        @keyup.enter="$emit('scan-material', barcode)"
      />
    </div>
    <div class="itemDivBig">
      <el-empty v-if="!details.length" :image-size="64" :description="$tx('暂无明细，请先扫码或查询')" />
      <el-card v-for="item in details" :key="item.id" class="itemDiv" shadow="never">
        <div class="itemLine">
          <span class="itemName">{{ $tx('物料编号:') }}</span>
          <span>{{ item.code }}</span>
        </div>
        <div class="itemLine">
          <span class="itemName">{{ $tx('物料名称:') }}</span>
          <span>{{ item.name }}</span>
        </div>
        <div class="itemLine">
          <span class="itemName">{{ $tx('物料条码:') }}</span>
          <span>{{ item.barcode }}</span>
        </div>
      </el-card>
    </div>
    <template #actions>
      <el-button @click="$emit('back')">{{ $tx('返回首页') }}</el-button>
      <el-button :loading="busy" type="primary" @click="confirm">{{ $tx('确认') }}</el-button>
    </template>
  </PdaPage>
</template>
<script>
export default {
  name: 'PdaOperationTemplate',
  props: {
    title: { type: String, required: true },
    busy: { type: Boolean, default: false },
    details: { type: Array, default: () => [] }
  },
  emits: ['back', 'scan-tray', 'scan-material', 'confirm'],
  data: () => ({ trayCode: '', barcode: '' }),
  mounted() { this.$refs.trayCode.focus() },
  methods: {
    confirm() {
      if (!this.busy) this.$emit('confirm', { trayCode: this.trayCode, barcode: this.barcode })
    }
  }
}
</script>
