# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Transfer1
- **det_chain**: Transfer1
### src_chain: source_chain
- **事件**: Transfer1
  - 函数: transfer
  - 关键操作: require(_to != address(0)), require(_to != contractAddress), balances[msg.sender] = balances[msg.sender].sub(_value), balances[_to] = balances[_to].add(_value)
### rel_chain: relay_chain
- 无事件
### det_chain: destination_chain
- **事件**: Transfer1
  - 函数: transfer
  - 关键操作: require(_to != address(0)), require(_to != contractAddress), balances[msg.sender] = balances[msg.sender].sub(_value), balances[_to] = balances[_to].add(_value)
---
