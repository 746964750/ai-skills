// 将此函数表达式整体传给浏览器 evaluate；只读 DOM，不改页面/状态。
() => {
  const findings = []
  const visible = el => {
    const box = el.getBoundingClientRect()
    const style = getComputedStyle(el)
    return box.width > 0 && box.height > 0 && style.display !== 'none' && style.visibility !== 'hidden'
  }
  const near = (a, b) => Math.abs(a - b) <= 1
  const value = (el, name) => getComputedStyle(el).getPropertyValue(name).trim()
  const page = document.querySelector('.pda-page')
  const metrics = { viewport: { width: innerWidth, height: innerHeight }, documentWidth: document.documentElement.scrollWidth }
  if (metrics.documentWidth > innerWidth + 1) findings.push('Document overflows horizontally')
  const expectedTokens = { '--pda-ink': '#20334a', '--pda-muted': '#61748b', '--pda-bg': '#f0f4f8', '--pda-line': '#dce5ef', '--pda-navy': '#173553', '--el-color-primary': '#1769ba' }
  for (const [key, expected] of Object.entries(expectedTokens)) {
    if (value(document.documentElement, key).toLowerCase() !== expected) findings.push('Root token differs: ' + key)
  }
  const controls = [...document.querySelectorAll('.body .el-input__wrapper, .body .el-select__wrapper, .el-button, .language-switcher .el-select__wrapper, .loginbox .el-input__wrapper')].filter(visible)
  for (const el of controls) {
    const height = el.getBoundingClientRect().height
    const minimum = el.closest('.pda-page__actions') ? 46 : el.matches('.loginbox .el-input__wrapper, .loginbox .btn .el-button') ? 48 : el.matches('.menu-entry') ? 106 : 44
    if (height < minimum - 1) findings.push('Control too short: ' + el.className + ' (' + height + 'px)')
  }
  if (page) {
    const header = page.querySelector('.pda-page__header')
    const body = page.querySelector('.pda-page__body')
    const panel = page.querySelector('.pda-page__panel')
    const footer = page.querySelector('.pda-page__actions')
    if (!header || !body || !panel) findings.push('Missing canonical page regions')
    if (header) {
      if (value(header, 'background-color') !== 'rgb(23, 53, 83)') findings.push('Header background differs')
      if (!near(parseFloat(value(header, 'border-bottom-width')), 3)) findings.push('Header accent width differs')
    }
    if (panel && panel.getBoundingClientRect().width > 761) findings.push('Content panel exceeds 760px')
    if (footer && body) {
      const bounds = footer.getBoundingClientRect()
      metrics.footer = { top: bounds.top, bottom: bounds.bottom, height: bounds.height }
      if (bounds.bottom > innerHeight + 1 || bounds.top < 0) findings.push('Footer is outside viewport')
      if (body.getBoundingClientRect().bottom > bounds.top + 1) findings.push('Body overlaps footer')
      if (value(footer, 'position') === 'fixed') findings.push('Footer should use flex layout')
    }
    metrics.bodyScroll = body ? { height: body.clientHeight, scrollHeight: body.scrollHeight } : null
  }
  for (const dialog of [...document.querySelectorAll('.el-dialog')].filter(visible)) {
    const box = dialog.getBoundingClientRect()
    if (box.left < 15 || box.right > innerWidth - 15 || box.width > 481) findings.push('Dialog violates responsive width')
  }
  return { status: findings.length ? 'failed' : 'passed', findings, metrics, scope: 'Current viewport and rendered state only; compare screenshots and test interactions separately.' }
}
