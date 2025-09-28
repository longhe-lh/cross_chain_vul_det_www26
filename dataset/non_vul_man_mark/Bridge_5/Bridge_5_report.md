# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Transfer1
- **rel_chain**: mint
- **det_chain**: Transfer1
### src_chain: BSC
- **事件**: Transfer1
  - 函数: burn
  - 关键操作: require(processedNonces[msg.sender][nonce] == false, "transfer already processed");, token._burn(msg.sender, amount);
### rel_chain: Relay Chain
- **事件**: mint
  - 函数: mint
  - 关键操作: require(recoverSigner(message, signature) == from, "wrong signature");, require(processedNonces[from][nonce] == false, 'transfer already processed');, processedNonces[from][nonce] = true;, token._mint(to, amount);
### det_chain: Ethereum
- **事件**: Transfer1
  - 函数: mint
  - 关键操作: require(recoverSigner(message, signature) == from, "wrong signature");, require(processedNonces[from][nonce] == false, 'transfer already processed');, processedNonces[from][nonce] = true;, token._mint(to, amount);
---
