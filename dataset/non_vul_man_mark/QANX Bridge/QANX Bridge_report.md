# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TokenLocked1
- **det_chain**: TokenUnlocked1
### src_chain: source_chain
- **事件**: TokenLocked1
  - 函数: bridgeSend
  - 关键操作: require(_qanx.transferFrom(msg.sender, address(this), amount)), _nonces[msg.sender][block.chainid][withdrawChainId]++
### rel_chain: relay_chain
- 无事件
### det_chain: destination_chain
- **事件**: TokenUnlocked1
  - 函数: bridgeWithdraw
  - 关键操作: require(verifySignature(txid, signature, amount), "ERR_SIG"), feesCollected += fee, require(_qanx.transfer(beneficiary, amount - fee), "ERR_TXN")
---
