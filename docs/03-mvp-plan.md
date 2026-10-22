# 单人私服 MVP 工作计划

> 完整版见工作区 `梦界物语_单人私服MVP_工作计划.xlsx`（7 个 sheet）。

基线：v2.43（versionCode 14387，Unity 5.5.2f1，IL2CPP metadata v22）。

## MVP 定义

只做「一个人能从头玩到一局结束」的最小闭环：

| # | 场景 | 验收 |
|---|---|---|
| ① | 进游戏 | 过版本校验、热更、公告，进主界面 |
| ② | 有角色 | 背包能看到导灵，能编队并保存 |
| ③ | 打一关 | 选关、进战斗、打完、体力正确扣除 |
| ④ | 育成一只 | 进梦域、触发事件、产出梦偶 |
| ⑤ | 抽一次卡 | 抽到卡，写进背包 |
| ⑥ | 存档 | 杀进程重进，数据都在 |

## 总量：83 人日（区间 75–95）

| 阶段 | 任务 | 人日 | 累计 |
|---|---|---|---|
| M0 | 本地服务骨架 + 接管启动链路 | 9 | 9 |
| M1 | 账号与 SQLite 存档 | 6 | 15 |
| M2 | 主数据生成 + 背包编队 | 17 | 32 |
| M3 | 关卡构造 + 战斗握手 | 16 | 48 |
| M4 | 育成闭环 | 8 | 56 |
| M5 | 抽卡商店 + 解密表 | 13 | 69 |
| M6 | 联调验收 | 10 | 79 |

## MVP 接口子集（17 个，从 98 个裁出）

```
data/config
user/register · user/login · user/portfolio
user/save_hero_team · user/save_tutor_team
tutor/buy · v2/tutor/sell · v2/tutor/upgrade
shop/list_item · shop/buy_item · shop/list_luckydraw · shop/draw_card
growth/enter · growth/complete
mainline/enter · mainline/complete · mainline/fail
data/watchdog
```

公会 / 排行 / PvP / 任务 / 邮件 / 活动一律不做。

## 工作分解

| # | 任务 | 内容 | 人日 |
|---|---|---|---|
| W1 | 本地服务骨架 | HTTP/HTTPS、路由、JSON、请求日志 | 3 |
| W2 | 接管启动链路 | hosts、自签证书、config、版本校验、assethash 伪造 | 6 |
| W3 | 账号与存档 | 游客注册、登录、session、SQLite | 6 |
| W4 | 主数据生成器 | 维基数据 → 客户端 JSON 字符串数组 | 6 |
| W5 | 数值补全 | hp/atk/spd 公式、技能 arguments、成长曲线 | 10 |
| W6 | 背包与编队 | 列表、编队保存、卖卡 | 5 |
| W7 | 关卡构造 | 3 区域 30 层，敌方用现有 4 套 Spine | 10 |
| W8 | 战斗握手 | mainline enter/complete/fail | 6 |
| W9 | 育成闭环 | 779 条事件编成服务端序列 | 8 |
| W10 | 抽卡与商店 | 卡池、概率、保底、买道具 | 7 |
| W11 | 加密表解密 | 定位密钥并批量导出 | 6 |
| W12 | 联调验收 | 六场景逐一过 | 10 |

## 资料清单

| # | 资料 | 现状 | 来源 |
|---|---|---|---|
| D1 | 导灵定义 215 条 | ✅ 已有 | 已解析（`data/tutors.csv`） |
| D2 | 技能 213 条 | ✅ 已有 | 已解析（`data/skills_*.csv`） |
| D3 | 技能 arguments | ❌ 缺 | 文字描述要提取成数值 |
| D4 | hp/atk/spd | ❌ 缺 | 套公式自造，或解密 CardLevelBonus 推 |
| D5 | 育成事件 779 条 | ✅ 已有 | `data/growth_events.csv` |
| D6 | 关卡 zones/floors | ❌ 缺 | 自造；战场复用包内 41 份明文泡泡布局 |
| D7 | ItemSetting | ⏳ 待解密 | 包内 2.4 KB |
| D8 | Localization | ⏳ 待解密 | 包内 413 KB |
| D9 | CardLevelBonus / CardFamilyBonus | ⏳ 待解密 | 包内 66 / 4 KB |
| D10 | GrowthCard / GrowthChapter | ⏳ 待解密 | 包内 |
| D11 | 抽卡概率 | ❌ 缺 | 自定 |
| D12 | 初始存档 | ❌ 缺 | 自定 |
| D13 | 立绘 200 张 | ✅ 已有 | 从公开维基下载（不入库） |
| D14 | 加密表密钥 | ❌ 缺 | Ghidra / Frida |
| D15 | 客户端可接管性 | ❓ 未验证 | POC 优先 |

## 风险

| 风险 | 影响 | 应对 |
|---|---|---|
| 客户端强校验 TLS | M0 卡死，方案要改 | 先做 POC；不行则改包或换 Android 6 |
| team/tutors 的 JSON 格式猜错 | 解析崩溃或空列表 | 从 `Tutor.FromJson` 反向确认；单条试 |
| 加密表解不开 | 文本空白、道具缺失 | Frida 兜底；文本可用维基顶上 |
| 关卡数据缺失 | 无可玩内容 | 自造 30 层 |
| 数值缺失 | 能进战斗但打不动 | 先套公式跑通，再调平衡 |

## 待决

- 是否保留育成闭环（砍掉省 8 人日）
- 数值是否要接近原版（+10 人日）
- 是否做 PvP / 公会（各 +10–30 人日）
- 跑在 PC 模拟器还是真机（建议 x86 模拟器）
