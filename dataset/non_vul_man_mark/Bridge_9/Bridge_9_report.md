# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Transfer1
- **det_chain**: Transfer1
### src_chain: source_chain
- **事件**: Transfer1
  - 函数: burn
  - 关键操作: token.burn(to,tokenId);, nonce++;
### rel_chain: 
- 无事件
### det_chain: destination_chain
- **事件**: Transfer1
  - 函数: mint
  - 关键操作: require(processedNonces[otherChainNonce] == false, 'transfer already processed');, processedNonces[otherChainNonce] = true;, token.mint(to);, nonce++;
---
