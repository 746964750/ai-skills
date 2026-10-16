<template>
  <div class="loginbox">
    <div class="login">
      <div class="login-toolbar">
        <span class="login-mark">WMS / PDA</span>
        <slot name="language" />
      </div>
      <div class="loginheader">
        <img v-if="logo" class="logo" :src="logo" :alt="title" />
        <h1>{{ title }}</h1>
        <p>{{ $tx('登录后开始仓库作业') }}</p>
      </div>
      <div class="loginbody">
        <el-form label-position="top" @submit.prevent="submit">
          <el-form-item :label="$tx('用户名')">
            <el-input
              v-model="username"
              :prefix-icon="User"
              :aria-label="$tx('用户名')"
              :placeholder="$tx('请输入用户名')"
              autocomplete="username"
              clearable
              @keyup.enter="submit"
            />
          </el-form-item>
          <el-form-item :label="$tx('密码')">
            <el-input
              v-model="password"
              :prefix-icon="Lock"
              :aria-label="$tx('密码')"
              :placeholder="$tx('请输入密码')"
              autocomplete="current-password"
              show-password
              clearable
              @keyup.enter="submit"
            />
          </el-form-item>
        </el-form>
      </div>
      <div class="btn">
        <el-button :loading="busy" type="primary" @click="submit">{{ $tx('登 录') }}</el-button>
      </div>
    </div>
  </div>
</template>
<script>
import { markRaw } from 'vue'
import { User, Lock } from '@element-plus/icons-vue'

export default {
  name: 'PdaLoginTemplate',
  props: {
    title: { type: String, required: true },
    logo: { type: String, default: '' },
    busy: { type: Boolean, default: false }
  },
  emits: ['submit'],
  data: () => ({ username: '', password: '', User: markRaw(User), Lock: markRaw(Lock) }),
  methods: {
    submit() {
      if (!this.busy) this.$emit('submit', { username: this.username, password: this.password })
    }
  }
}
</script>
