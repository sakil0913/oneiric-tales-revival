# 协议契约（字段级）

来源：v2.43 的 `dump.cs`（Il2CppDumper 6.7.46）。

## 传输层

- 全部接口为 **POST**，基址 `https://api.oneirictales.com/`
- 客户端用 BestHTTP 发送，`Server.Json` 命名空间下的 DTO 反序列化
- 公共响应字段见 `BaseJson`

```csharp
public class BaseJson {
    public int respond;              // 1 = 成功
    public string result;
    public string serverTime;        // 必须回真实时间，否则体力/冷却错乱
    public ErrorDetailJson errorDetail;
    public string phash;             // 防重放签名
}
```

## 实体模型

客户端用 `Tutor.FromJson` / `ToJson` 收发实体，所以 **实体是 JSON 字符串**。

```csharp
public class Tutor : Card {          // 玩家拥有的一只导灵
    public uint id;                  // 实例 id
    public int monsterId;            // 对应主数据里的编号（001–247）
    public int level;
    public int extendedMaxLevel;
    public int numDuplicatedCards;
    public int createTime;
}
```

```csharp
public class TutorInfo {             // 服务端下发的静态定义（主数据）
    public int monsterId;
    public string name, nameForGrowth;
    public int maxLevel, expType, groupId;
    public int buyCost, sellCost, sellFragment;
    public Rare rare;                // N / R / SR / UR
    public Role role;                // 攻击 / 防御 / 速度 / 万能
    public Element mainElement;      // 火 / 水 / 木 / 光 / 暗
    public Gender gender;
    public int imageId;              // 对应立绘编号
    public CardLuckBonusInfo levelBonusInfo;
    public int defaultLevelBonusId;
    public List<CardFamilyBonusInfo> familyBonusInfos;
    public bool canDating;
    public int appearAtTraining;
    public int[] trainingExps;
    public TutorGrowthInfo growthInfo;
    public AvatarInfo avatarInfo;
    public WarriorData warriorData;
}
```

`Tutor.hp / atk / spd` 是**计算属性**，由 `TutorInfo` + `level` + `levelBonusInfo` 推出来，
所以基础数值实际藏在 `growthInfo` / `levelBonusInfo` 里——这两部分很可能就是包内
`GrowthCard` / `CardLevelBonus` 加密表的内容。

```csharp
public class ActiveSkillData {
    public ActiveSkillInfo info;
    public string name, details, buffDetails;
    public int skillMP;
    public int timeFactor;
    public Long[] arguments;         // 客户端用这组参数算效果
    public int argOffset;
}

public class PassiveSkillData {
    public PassiveSkillInfo info;
    public string name, details, buffDetails;
    public Long[] arguments;
    public int argOffset;
}
```

## 登录响应

```csharp
public class LoginJson {
    public DataJson data;            // 39 组主数据
    public UserDataJson userData;    // 偏好、收藏、已完成剧情
}

public class DataJson {
    public string[] tutors;          // ← TutorInfo 的 JSON 数组
    public string[] activeSkills;
    public string[] passiveSkills;
    public string[] bossActiveSkills, bossPassiveSkills;
    public string[] zones, floors;              // 关卡
    public string[] dungeonFloors, mainlineFloors;  // v2.43 新增
    public string[] growthChapters, growthStories;
    public string growthEventBonus;
    public string tutorBaseExpSettings;
    public string[] banners, notification;
    public string[] dailyLoginReward, eventLoginReward;  // 及 current/claimed
    public string[] pvpRankingRewards;
    public PvpScore pvpScore;
    public EventPvpScore eventPvpScore;
    // …共 39 个字段
}
```

```csharp
public class UserJson {              // 56 个字段
    public string uid, name, sessionId;
    public int coin, diamond, soulRoll, fragment;
    public int currentStamina, maxStamina, currentTicket, maxTicket;
    public Timestamp lastStaminaRecharge, lastTicketRecharge;
    public string[] heroTeamList, tutorTeamList;   // JSON 字符串
    public int teamSize, teamNumber, heroCount;
    public bool tutorialFinished;
    public bool hasPassword;
    public string keyCode;
    public int growthRemainCount, pvpRemainCount;
    // …
}
```

## 请求头

客户端在请求里带 `uid` / `session` / 时间戳 / `phash`。
私服可以先一律放行，但 `serverTime` 必须回填真实时间。

## 待确认

以下三处的**内部编码格式**还没有实证，需要在 POC 里用最小数据试：

1. `tutors[]` 里每个元素是直接的 `TutorInfo` JSON，还是再包一层？
2. `tutorTeamList[]` 的元素结构（`UserTutorTeam.ToTutorJson()` 的实际输出）
3. `floors[]` / `zones[]` 的字段与嵌套（包里完全没有样本）

确认方法：抓一次客户端发出的真实请求（本地服务记录即可），
或从 `Tutor.FromJson` 的反编译结果反推键名。
