// Isolated visual fixture. No application router, authentication or HTTP client.
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import 'element-plus/dist/index.css'
import 'lib-flexible/flexible'
import '../runtime/native-management.scss'
import '../runtime/portable-layout.scss'
import Preview from './Preview.vue'
createApp(Preview).use(ElementPlus, { size: 'small', locale: zhCn }).mount('#app')
