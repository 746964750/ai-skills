import PdaPage from './PdaPage.vue'
import './base.css'

// 宿主先安装 Element Plus 及其 CSS；PDA 使用 default 尺寸，locale 沿用宿主。
export function installPdaStyle(app, { translate = value => value } = {}) {
  if (!app.config.globalProperties.$tx) app.config.globalProperties.$tx = translate
  if (!app.component('PdaPage')) app.component('PdaPage', PdaPage)
}
