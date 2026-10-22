# 需要补全的清单

> 完整版见工作区 `梦界物语_复活补全清单_v2.43.xlsx`（9 个 sheet / 167 项 / 可勾选）。

## 分组概览

| 组 | 条目 | 人日 | 说明 |
|---|---|---|---|
| A 启动链路 | 8 | 21 | 不完成就进不到登录之后 |
| B 服务端接口 | 98 | 145 | P0 单人可玩 29 个 |
| C 主数据表 | 39 | 82 | 登录响应里必须灌进去的 39 组 |
| D 本地数据资产 | 6 | 10 | 解密回收，不是从零构造 |
| E 客户端改造 | 10 | 16 | hosts / TLS / 反作弊 / 支付 |
| F 资源缺口 | 9 | 26 | Live2D 缺口无上限 |

## A 启动链路（硬门槛）

1. `data/config` 握手 —— 返回合法 `ConfigJson`
2. 资源清单 `assethashserver` —— 让客户端认为已是最新
3. 版本/热更校验 —— 不弹强制更新
4. 注册/登录 —— 返回完整 `LoginJson`
5. 会话与签名 —— 回填真实 `serverTime`
6. watchdog 上报 —— 回 `respond=1`
7. 新手引导状态 —— `tutorialFinished=true`
8. 反作弊探测 —— 原包运行无需处理

## B 接口（按域）

user 12 / tutor+v2 9 / hero 2 / growth 3 / dungeon 12 / mainline 3 /
pvp 18 / guild 15 / shop 11 / reward 3 / mission 4 / fb 4 / data 2

MVP 只需 17 个，见 `03-mvp-plan.md`。

## C 主数据（登录时下发）

`tutors`、`activeSkills`、`passiveSkills`、`bossActiveSkills`、`bossPassiveSkills`、
`zones`、`floors`、`dungeonFloors`、`mainlineFloors`、`growthChapters`、`growthStories`、
`growthEventBonus`、`tutorBaseExpSettings`、各类奖励表、`banners`、`notification` 等 39 组。

其中 `zones/floors/dungeonFloors/mainlineFloors` 完全缺失，必须自造。

## D 本地数据资产

1,098 张加密 TextAsset（「!」+Base64，块加密）。含：

| 表 | 体积 | 用途 |
|---|---|---|
| Localization | 413 KB | 全部界面文本 |
| GrowthEvent | 178 KB | 育成事件 |
| CardLevelBonus | 66 KB | 卡牌等级加成 |
| GrowthCard | 9.8 KB | 卡牌成长 |
| ItemSetting | 2.4 KB | 道具表 |
| Talk_* × 1,078 | — | 剧情文本 |

密钥定位：Ghidra 静态（2–4 天）或模拟器 + Frida 动态 dump（1–2 天）。

## F 资源缺口

| 资产 | 情况 |
|---|---|
| UI 图集 | 完整（36 张） |
| 角色立绘 | 包内 0 张；**已从公开维基回收 200 张**（1333²，带水印） |
| Live2D 模型 | 缺失，且无替代（客户端只有 15 个着色器） |
| Spine 骨骼 | 包里仅 4 套（0001 / 4000 / GachaNPC / sheep_side2） |
| 音效 | 121 个，BGM 仅 1 首 |

Live2D 的替换面很小：客户端只有 `SimpleModel` + `DramaCharacter` 用到 `Live2DModelUnity`，
卡面用的是 Spine（`TutorCardView._spine`）。静态立绘替换约 3–5 人日。
