# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Transfer1
- **rel_chain**: mint, burn
- **det_chain**: Transfer1
### src_chain: AVAX
- **事件**: Transfer1
  - 函数: Burn
  - 关键操作: transfers[msg.sender] = transfers[msg.sender] + 1, token.burn(msg.sender, amount)
### rel_chain: RelayChain
- **事件**: mint
  - 函数: Mint
  - 关键操作: bytes32 messageHash = keccak256(abi.encodePacked(to, amount, nonce)), bytes32 message = ECDSA.toEthSignedMessageHash(messageHash), address signer = ECDSA.recover(message, signature), require(signer == from, "incorret Signature"), uint256 id = transfers[to], hasProcessed[to][id] = true, token.mint(to, amount)
- **事件**: burn
  - 函数: Burn
  - 关键操作: transfers[msg.sender] = transfers[msg.sender] + 1, token.burn(msg.sender, amount)
### det_chain: BSC
- **事件**: Transfer1
  - 函数: Mint
  - 关键操作: bytes32 messageHash = keccak256(abi.encodePacked(to, amount, nonce)), bytes32 message = ECDSA.toEthSignedMessageHash(messageHash), address signer = ECDSA.recover(message, signature), require(signer == from, "incorret Signature"), uint256 id = transfers[to], hasProcessed[to][id] = true, token.mint(to, amount)
---
