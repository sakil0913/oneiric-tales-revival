# server —— 本地服务端

> 状态：待实现（见 `docs/03-mvp-plan.md` 的 M0）

## 目标

在不动客户端的前提下，接管 `api.oneirictales.com` 的 98 个接口，
让原版客户端能登录、编队、打关、育成、抽卡。

```
Android 客户端 ──(hosts → 127.0.0.1)──► 本服务 ──► SQLite
```

## 技术选型（建议）

| 项 | 选择 | 理由 |
|---|---|---|
| 语言 | Python 3.11 + FastAPI | 迭代快，JSON 处理直接 |
| 存储 | SQLite | 单机单人，零部署 |
| TLS | 自签证书 | 客户端可能不校验证书（待验证） |
| 配置 | `.env` + `config.yaml` | 端口、证书路径、初始资源量 |

## 目录规划

```
server/
  app/
    main.py            入口与路由注册
    api/               按域拆分（user / tutor / shop / growth / mainline）
    models/            Pydantic 模型，对应 Server.Json 的 DTO
    data/              主数据加载（读 data/*.csv，转成客户端 JSON）
    store/             SQLite 存档层
  certs/               自签证书（不入库）
  tests/
```

## 实现顺序

1. **M0** —— `data/config` + `user/login` 桩数据，先让客户端过启动链路
2. **M1** —— 账号、session、存档
3. **M2** —— 主数据生成（`data/*.csv` → `tutors[]` / `skills[]`）
4. **M3** —— 关卡与战斗握手
5. **M4** —— 育成
6. **M5** —— 抽卡与商店

## 未验证的前提

**客户端是否接受自签证书，决定整个方案是否成立。**
M0 第一件事就是验证这一点；不成立则要改走「改包」或「Android 6 + 系统 CA」。
