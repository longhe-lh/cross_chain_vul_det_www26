# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Transfer1
- **rel_chain**: mint, burn
- **det_chain**: Transfer1
### src_chain: BSC
- **事件**: Transfer1
  - 函数: burn
  - 关键操作: token.burn(msg.sender, amount), nonce++
### rel_chain: RelayChain
- **事件**: mint
  - 函数: mint
  - 关键操作: require(msg.sender == admin, 'only admin'), require(processedNonces[otherChainNonce] == false, 'transfer already processed'), processedNonces[otherChainNonce] = true, token.mint(to, amount)
- **事件**: burn
  - 函数: burn
  - 关键操作: token.burn(msg.sender, amount), nonce++
### det_chain: ETH
- **事件**: Transfer1
  - 函数: mint
  - 关键操作: require(msg.sender == admin, 'only admin'), require(processedNonces[otherChainNonce] == false, 'transfer already processed'), processedNonces[otherChainNonce] = true, token.mint(to, amount)
---
