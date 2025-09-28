# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenRedeem2
- **rel_chain**: mint, burn
- **det_chain**: TokenWithdraw1, TokenMint2
### src_chain: Ethereum
- **事件**: TokenDeposit1
  - 函数: deposit
  - 关键操作: require(_value > 0, ERROR_DEPOSIT_VALUE_ZERO), if (_token == ETH) { require(msg.value == _value, ERROR_VALUE_MISMATCH); } else { require(ERC20(_token).safeTransferFrom(msg.sender, address(this), _value), ERROR_TOKEN_TRANSFER_FROM_REVERTED); }, emit VaultDeposit(_token, msg.sender, _value)
- **事件**: TokenRedeem2
  - 函数: withdraw
  - 关键操作: require(_value > 0, ERROR_TRANSFER_VALUE_ZERO), if (_token == ETH) { require(_to.send(_value), ERROR_SEND_REVERTED); } else { require(ERC20(_token).safeTransfer(_to, _value), ERROR_TOKEN_TRANSFER_REVERTED); }, emit VaultTransfer(_token, _to, _value)
### rel_chain: RelayChain
- **事件**: mint
  - 函数: _mint
  - 关键操作: require(account != address(0), 'ERC777: mint to the zero address'), _totalSupply = _totalSupply.add(amount), _balances[account] = _balances[account].add(amount), emit Minted(operator, account, amount, userData, operatorData)
- **事件**: burn
  - 函数: _burn
  - 关键操作: require(from != address(0), 'ERC777: burn from the zero address'), _balances[from] = _balances[from].sub(amount, 'ERC777: burn amount exceeds balance'), _totalSupply = _totalSupply.sub(amount), emit Burned(operator, from, amount, data, operatorData)
### det_chain: BinanceSmartChain
- **事件**: TokenWithdraw1
  - 函数: transfer
  - 关键操作: require(_value <= balances[msg.sender]), balances[msg.sender] = balances[msg.sender].sub(_value), balances[_to] = balances[_to].add(_value), emit Transfer(msg.sender, _to, _value)
- **事件**: TokenMint2
  - 函数: generateTokens
  - 关键操作: require(holder != address(0)), _totalSupply = _totalSupply.add(amount), _balances[holder] = _balances[holder].add(amount), emit Transfer(address(0), holder, amount)
---
