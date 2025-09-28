# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TokenLock1
- **det_chain**: TokenUnlock1
### src_chain: Goerli
- **事件**: TokenLock1
  - 函数: lockTokensForOptimism
  - 关键操作: if (msg.value != 1003 ) { revert msgValueNot1003(); }, enqueue();, payable(Owner).transfer(msg.value);
### rel_chain: 
- 无事件
### det_chain: Optimism
- **事件**: TokenUnlock1
  - 函数: ownerUnlockGoerliETH
  - 关键操作: if (msg.sender != Owner) { revert notOwnerAddress(); }, address userToBridge = optimismBridgeInstance.queue(optimismBridgeInstance.last());, optimismBridgeInstance.dequeue();, payable(userToBridge).transfer(1000);
---
