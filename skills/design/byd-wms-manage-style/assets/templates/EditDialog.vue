<template>
  <el-dialog
    :model-value="modelValue"
    :title="labels.title"
    width="640px"
    class="wms-dialog"
    :close-on-click-modal="false"
    @update:model-value="value => emit('update:modelValue', value)"
    @closed="emit('closed')"
  >
    <el-form ref="formRef" :model="model" :rules="rules" label-position="top" size="default" class="wms-edit-form">
      <el-form-item :label="labels.code" prop="code" size="default">
        <el-input :model-value="model.code" size="default" :readonly="readOnly" @update:model-value="value => update('code', value)" />
      </el-form-item>
      <el-form-item :label="labels.name" prop="name" size="default">
        <el-input :model-value="model.name" size="default" :readonly="readOnly" @update:model-value="value => update('name', value)" />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button size="default" :disabled="saving" @click="emit('update:modelValue', false)">{{ labels.cancel }}</el-button>
        <el-button v-if="!readOnly" size="default" type="primary" :loading="saving" @click="submit">{{ labels.save }}</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({
  modelValue: Boolean,
  model: { type: Object, required: true },
  rules: { type: Object, default: () => ({}) },
  readOnly: Boolean,
  saving: Boolean,
  labels: { type: Object, default: () => ({ title: '编辑信息', code: '编号', name: '名称', cancel: '取消', save: '保存' }) }
})
const emit = defineEmits(['update:modelValue', 'update:model', 'save', 'closed'])
const formRef = ref()
const update = (key, value) => emit('update:model', { ...props.model, [key]: value })
async function submit() {
  if (!formRef.value || props.saving || props.readOnly) return
  try {
    if (await formRef.value.validate()) emit('save', props.model)
  } catch {
    // Keep the native field errors visible; parent alone performs the save.
  }
}
defineExpose({ formRef })
</script>
