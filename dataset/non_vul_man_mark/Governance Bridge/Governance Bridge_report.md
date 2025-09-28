# 跨链桥合约分析报告
## 跨链桥: Governance Bridge
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenRedeem2
- **rel_chain**: MessageDelivered
- **det_chain**: TokenWithdraw1, TokenMint2
### src_chain: Ethereum
- **事件**: TokenDeposit1
  - 函数: sendMessage
  - 关键操作: require(msg.sender == _ethereumGovernanceExecutor, "UnauthorizedEthereumExecutor()");
- **事件**: TokenRedeem2
  - 函数: processMessageFromRoot
  - 关键操作: if (rootMessageSender != _fxRootSender) revert UnauthorizedRootOrigin();
### rel_chain: Arbitrum
- **事件**: MessageDelivered
  - 函数: enqueueSequencerMessage
### det_chain: Polygon
- **事件**: TokenWithdraw1
  - 函数: processMessageFromRoot
  - 关键操作: if (rootMessageSender != _fxRootSender) revert UnauthorizedRootOrigin();
- **事件**: TokenMint2
  - 函数: sendMessage
  - 关键操作: require(msg.sender == _ethereumGovernanceExecutor, "UnauthorizedEthereumExecutor()");
---
