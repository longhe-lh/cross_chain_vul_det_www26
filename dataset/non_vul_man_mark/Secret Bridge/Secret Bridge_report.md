# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1
- **rel_chain**: mint, burn
- **det_chain**: TokenWithdraw1
### src_chain: Ethereum
- **事件**: TokenDeposit1
  - 函数: _transfer
  - 关键操作: if (hasRole(MINTER_ROLE, sender)) {
            _mint(recipient, amount);
        } else if (hasRole(MINTER_ROLE, recipient)) {
            _burn(sender, amount);
        } else {
            super._transfer(sender, recipient, amount);
        }
### rel_chain: RelayChain
- **事件**: mint
  - 函数: _mint
  - 关键操作: _beforeTokenTransfer(address(0), account, amount);

        _totalSupply = _totalSupply.add(amount);
        _balances[account] = _balances[account].add(amount);
        emit Transfer(address(0), account, amount);
- **事件**: burn
  - 函数: _burn
  - 关键操作: _beforeTokenTransfer(account, address(0), amount);

        _balances[account] = _balances[account].sub(amount, "ERC20: burn amount exceeds balance");
        _totalSupply = _totalSupply.sub(amount);
        emit Transfer(account, address(0), amount);
### det_chain: SecretNetwork
- **事件**: TokenWithdraw1
  - 函数: _transfer
  - 关键操作: if (hasRole(MINTER_ROLE, sender)) {
            _mint(recipient, amount);
        } else if (hasRole(MINTER_ROLE, recipient)) {
            _burn(sender, amount);
        } else {
            super._transfer(sender, recipient, amount);
        }
---
