# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Transfer1
- **rel_chain**: Mint, Burn
- **det_chain**: Transfer1
### src_chain: source_chain
- **事件**: Transfer1
  - 函数: transfer
  - 关键操作: balanceOf[from] = balanceOf[from].sub(value), balanceOf[to] = balanceOf[to].add(value)
### rel_chain: relay_chain
- **事件**: Mint
  - 函数: mint
  - 关键操作: totalSupply = totalSupply.add(value), balanceOf[to] = balanceOf[to].add(value)
- **事件**: Burn
  - 函数: burn
  - 关键操作: balanceOf[from] = balanceOf[from].sub(value), totalSupply = totalSupply.sub(value)
### det_chain: destination_chain
- **事件**: Transfer1
  - 函数: transfer
---
