# macOS 数据布局与分级参考

分析 macOS 扫描结果时读这份。讲"东西存在哪、怎么辨认、归哪一级"。

## 关键目录

| 目录 | 装什么 | 典型分级 |
|---|---|---|
| `~/Library/Caches` | 应用/系统缓存 | 🟢（可再生） |
| `~/Library/Caches/pip`、`uv`、浏览器 Cache | 开发/浏览器缓存 | 🟢 |
| `~/Library/Developer/Xcode/DerivedData` | Xcode 构建产物 | 🟢 |
| `~/Library/Developer/CoreSimulator` | iOS 模拟器数据 | 🟢 / 🟡（含自定义 App 数据时） |
| `~/Library/Developer/Xcode/iOS DeviceSupport` | 真机符号/支持文件 | 🟢（可再下） |
| `~/.npm`、`~/.pnpm-store`、`~/.gradle`、`~/.m2`、`~/.cargo`、`~/.cache`、`~/.docker` | 开发缓存 | 🟢 |
| `~/Library/Containers/<UUID>` | 沙盒 App 数据（常含离线视频/文档） | 🟡（先查所属 App） |
| `~/Library/Group Containers` | App 组共享数据 | 🟡 |
| `~/Library/Application Support` | 应用持久数据 | 🟡 |
| `~/Downloads` 的 `.dmg` / `.pkg` / `.zip` 安装包 | 安装包残留 | 🟢 |
| `/Applications`、`~/Applications` | 应用本体 | 🔴 仅重复/想卸时上灯，否则归蓝色 |
| `~/.Trash` | 废纸篓 | 🟡 提示用户清空 |

## 神秘大目录（UUID Container）

`~/Library/Containers/` 下大量 UUID 文件夹。占用大时必须追查归属：

1. 读 `Container.plist` / 看内部 `Data/Library` 结构，或对照 `~/Library/Application Support`、App 显示名。
2. 常见大户：视频 App 离线缓存（如 Bilibili 的 `.Downloads`）、设计工具缓存、聊天附件。
3. **有核实过的安全子路径**（删了不破坏 App）→ 给 `trash_paths`（橙灯只准移废纸篓）。
4. **App 托管、无安全子路径** → 只给「在访达打开」，不给 trash_paths；可用 `open_note` 说明内部结构不便手动挑。

## 系统占用（不上灯，归蓝色"系统及其他"，间接释放写 long_term）

- APFS 快照 / Time Machine 本地快照：不手删；`tmutil listlocalsnapshots /` 了解，策略写 long_term
- 可清除空间（purgeable）：系统自动回收，报告里可说明，勿当可删用户文件
- swap / sleepimage：重启可间接释放，写 long_term
- `/System`、`/Library` 系统目录：绝不能手删

间接释放建议素材：系统设置 > 通用 > 储存空间；`brew cleanup`；清空废纸篓；外置盘 / iCloud 归档大文件。

## 删除机制

`server.py` 在 macOS 用 `osascript` 调访达「移到废纸篓」。首次可能弹自动化授权，用户点允许即可。🟢 项的 `trash_paths` 应在 `$HOME` 内，便于白名单校验通过。
