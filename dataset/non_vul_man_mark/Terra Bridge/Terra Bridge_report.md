# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Deposit1, Borrow2
- **rel_chain**: Mint, burn
- **det_chain**: Withdraw1, Repay2
### src_chain: Ethereum
- **事件**: Deposit1
  - 函数: deposit
  - 关键操作: _balances[sender] = oldAccountBalance.sub(amount, "ERC20: transfer amount exceeds balance");, _balances[recipient] = _balances[recipient].add(amount);
- **事件**: Borrow2
  - 函数: borrow
  - 关键操作: _balances[sender] = oldAccountBalance.sub(amount, "ERC20: transfer amount exceeds balance");, _balances[recipient] = _balances[recipient].add(amount);
### rel_chain: RelayChain
- **事件**: Mint
  - 函数: mint
  - 关键操作: _balances[user] = _balances[user].add(amount.rayDiv(index));, emit Transfer(address(0), user, amount);
- **事件**: burn
  - 函数: burn
  - 关键操作: _burn(user, amountScaled);, IERC20(_underlyingAsset).safeTransfer(receiverOfUnderlying, amount);
### det_chain: Terra
- **事件**: Withdraw1
  - 函数: withdraw
  - 关键操作: _balances[sender] = _balances[sender].sub(amount, "ERC20: transfer amount exceeds balance");, _balances[recipient] = _balances[recipient].add(amount);
- **事件**: Repay2
  - 函数: repay
  - 关键操作: _balances[sender] = _balances[sender].sub(amount, "ERC20: transfer amount exceeds balance");, _balances[recipient] = _balances[recipient].add(amount);
---
