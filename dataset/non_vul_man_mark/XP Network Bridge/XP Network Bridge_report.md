# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Transfer1
- **det_chain**: Transfer1
### src_chain: source_chain
- **事件**: Transfer1
  - 函数: mint
  - 关键操作: require(ownerOf(id) == from, "You don't own this nft!"), _safeMint(to, id)
### rel_chain: relay_chain
- 无事件
### det_chain: destination_chain
- **事件**: Transfer1
  - 函数: burnFor
  - 关键操作: require(ownerOf(id) == from, "You don't own this nft!"), _burn(id)
---
