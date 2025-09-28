# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TokensLocked1
- **det_chain**: TokensBridged1
### src_chain: main_chain
- **事件**: TokensLocked1
  - 函数: lockTokens
  - 关键操作: IERC20(ethToken).burn(msg.sender , _bridgedAmount)
### rel_chain: 
- 无事件
### det_chain: side_chain
- **事件**: TokensBridged1
  - 函数: bridgeTokens
  - 关键操作: IERC20(bnbToken).mint(_requester, aaamount)
---
