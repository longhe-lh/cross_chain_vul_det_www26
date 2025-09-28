# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Transfer1, Approval2
- **det_chain**: Transfer1, Approval2
### src_chain: Ethereum
- **事件**: Transfer1
  - 函数: transfer
  - 关键操作: _transfer(sender, recipient, amount), require(sender != address(0), "ERC20: transfer from the zero address"), require(recipient != address(0), "ERC20: transfer to the zero address")
- **事件**: Approval2
  - 函数: approve
  - 关键操作: _approve(owner, spender, amount)
### rel_chain: 
- 无事件
### det_chain: Ethereum
- **事件**: Transfer1
  - 函数: _mint
  - 关键操作: _totalSupply = _totalSupply.add(amount), _balances[account] = _balances[account].add(amount)
- **事件**: Approval2
  - 函数: _approve
  - 关键操作: _allowances[owner][spender] = amount
---
