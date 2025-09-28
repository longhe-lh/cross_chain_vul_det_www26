# 跨链桥合约分析报告
## 跨链桥: Suter Bridge
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenRedeem2
- **rel_chain**: RelayMessage
- **det_chain**: TokenWithdraw1, TokenMint2
### src_chain: Ethereum
- **事件**: TokenDeposit1
  - 函数: transfer
  - 关键操作: require(_to != address(0));, require(_value <= balances[msg.sender]);, balances[msg.sender] = sub(balances[msg.sender],_value);, balances[_to] = add(balances[_to], _value);
- **事件**: TokenRedeem2
  - 函数: transferFrom
  - 关键操作: require(_to != address(0));, require(_value <= balances[_from]);, require(_value <= allowed[_from][msg.sender]);, balances[_from] = sub(balances[_from], _value);, balances[_to] = add(balances[_to], _value);, allowed[_from][msg.sender] = sub(allowed[_from][msg.sender], _value);
### rel_chain: Relay Chain
- **事件**: RelayMessage
  - 函数: relayMessage
### det_chain: Ethereum
- **事件**: TokenWithdraw1
  - 函数: transfer
  - 关键操作: require(!isBlacklist(msg.sender), "Token: caller in blacklist can't transfer");, require(!isBlacklist(to), "Token: not allow to transfer to recipient address in blacklist");, return super.transfer(to, value);
- **事件**: TokenMint2
  - 函数: _mint
  - 关键操作: require(account != address(0), "ERC20: mint to the zero address");, _totalSupply = _totalSupply.add(amount);, _balances[account] = _balances[account].add(amount);
---
