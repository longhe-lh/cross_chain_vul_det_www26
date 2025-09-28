# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Transfer1
- **det_chain**: Transfer1
### src_chain: BSC
- **事件**: Transfer1
  - 函数: burn
  - 关键操作: configToken.burnToken(msg.sender, _amount), processedTxNonce[msg.sender][_nonce] = true
### rel_chain: 
- 无事件
### det_chain: ETH
- **事件**: Transfer1
  - 函数: mint
  - 关键操作: require(recoverSigner(message, _signature) == _from, "wrong signature"), require(processedTxNonce[_from][_nonce] == false, "transfer has already been processed"), processedTxNonce[_from][_nonce] = true, configToken.mintToken(_to, _amount)
---
