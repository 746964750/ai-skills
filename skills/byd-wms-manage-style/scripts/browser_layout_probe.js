// Read-only expression for a browser tool's DOM evaluate. No application state,
// request, cookie, storage or credential access. Does not scroll or change UI.
(() => {
  const rect = element => {
    const r = element.getBoundingClientRect()
    return { x: r.x, y: r.y, width: r.width, height: r.height, bottom: r.bottom }
  }
  const visible = element => {
    const r = element.getBoundingClientRect()
    return r.width > 0 && r.height > 0 && getComputedStyle(element).visibility !== 'hidden'
  }
  const search = [...document.querySelectorAll('.wms-search')].filter(visible).map(root => ({
    bounds: rect(root),
    body: [...root.querySelectorAll('.SearchcardBody')].filter(visible).map(e => ({ ...rect(e), padding: getComputedStyle(e).padding })),
    fields: [...root.querySelectorAll('.formDiv > .el-form > .el-row > .el-col')].filter(visible).map(e => ({ ...rect(e), padding: getComputedStyle(e).padding }))
  }))
  const scopes = ':is(.wms-management, .wms-dialog, .wms-drawer)'
  const columns = [...document.querySelectorAll(scopes + ' .el-table-column--selection, ' + scopes + ' th.wms-index-column, ' + scopes + ' td.wms-index-column, ' + scopes + ' th.document-index-column, ' + scopes + ' td.document-index-column')].filter(visible).map(e => {
    const cell = e.querySelector('.cell')
    const checkbox = e.querySelector('.el-checkbox__inner')
    const c = rect(e)
    const b = checkbox && rect(checkbox)
    return {
      bounds: c,
      align: getComputedStyle(e).textAlign,
      text: checkbox ? undefined : cell?.textContent.trim(),
      contentAlign: cell && getComputedStyle(cell).textAlign,
      clipped: cell ? cell.scrollWidth > cell.clientWidth : undefined,
      checkboxCenterError: b ? { x: Math.abs(c.x + c.width / 2 - b.x - b.width / 2), y: Math.abs(c.y + c.height / 2 - b.y - b.height / 2) } : undefined
    }
  })
  const buttons = [...document.querySelectorAll('.wms-management .card-btn .el-button, .wms-dialog .el-button, .wms-drawer .el-button')].filter(visible).map(e => ({
    text: e.textContent.trim(), ariaLabel: e.getAttribute('aria-label'), classes: e.className, ...rect(e)
  }))
  const overlays = [...document.querySelectorAll('.el-dialog.wms-dialog, .el-drawer.wms-drawer')].filter(visible).map(e => {
    const footer = e.querySelector('.el-dialog__footer, .el-drawer__footer')
    return { bounds: rect(e), footer: footer && rect(footer), footerWithinViewport: footer ? rect(footer).bottom <= innerHeight : undefined }
  })
  return { viewport: [innerWidth, innerHeight], pageOverflowX: document.documentElement.scrollWidth > innerWidth, search, columns, buttons, overlays }
})()
