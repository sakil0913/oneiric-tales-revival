# data —— 从公开维基整理的结构化数据

## 来源

全部来自 [夢界物語繁中維基](https://oneirictales.fandom.com/zh/wiki/)
通过 MediaWiki API 抓取（`tools/wiki_dump.py`），再解析 `Template:` 命名空间下的 infobox 得到。

| 文件 | 内容 | 行数 |
|---|---|---|
| `tutors.csv` | 导灵表：编号 / 名称 / 稀有度 / 属性 / 类型 / 主被动技能 / 性别 / 可培养 / 来源 | 215 |
| `skills_active.csv` | 主动技能：6 级效果 + 每级 MP + 归属卡牌 | 110 |
| `skills_passive.csv` | 被动技能：记忆空间 + 5 级效果 + 归属卡牌 | 103 |
| `growth_events.csv` | 育成事件：事件 / 选项 / 体力 / 结果 / 触发条件 | 779 |

## 字段说明

### tutors.csv

```
id,name,rare,attr,type,skill,ps1..ps6,gender,inter,source,sublimate,tos
001,桑安,N,木,速度,盤根,攻擊成長,吸引力,火屬剋星,,,,一般召喚,女,可,,
```

- 大多数角色有 **N/R 两个编号**（如 001/002 都是「桑安」），技能与被动相同
- `attr`：木 / 火 / 水 / 光 / 暗
- `type`：攻擊 / 防禦 / 速度 / 萬能
- `inter`：可培养（是否能在梦域育成）

### skills_active.csv

```
name,card,l1..l6,mp1..mp6
盤根,001|002,對敵方夢偶做成1次攻擊3倍木屬傷害,...,30,28,26,24,22,20
```

### growth_events.csv

```
card,event,choose,stamina,result,note,color
001,花占,不相信,-25,獲得吸引力,,/
```

- `note` 里的 `觸發條件：…` 是事件的触发前提（好感度、约会次数等）
- `color=P` 表示粉色档事件（通常是灵魂伴侣线）

## 已知缺口

- 9 个主动技能、2 个被动技能被引用但没有模板页
- 133 张卡没有育成事件页
- **基础数值 hp/atk/spd 不在维基中**，需另寻来源或自造
- 5 个编号（128/132/136/140/144）在图鉴网格里有位但页面与模板都缺

## 许可

这些是游戏数据的结构化转录，原始内容著作权归 Madhead。
以 CC BY-NC-SA 4.0 提供，仅供非商业的研究与学习用途。
