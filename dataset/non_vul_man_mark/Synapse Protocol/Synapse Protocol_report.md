# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenDepositAndSwap2, TokenRedeem3, TokenRedeemAndSwap4, TokenRedeemAndRemove5
- **rel_chain**: mint, withdraw, mintAndSwap, withdrawAndRemove
- **det_chain**: TokenWithdraw1, TokenMintAndSwap2, TokenMint3, TokenMintAndSwap4, TokenWithdrawAndRemove5
### src_chain: source_chain
- **事件**: TokenDeposit1
  - 函数: deposit
  - 关键操作: token.safeTransferFrom(msg.sender, address(this), amount)
- **事件**: TokenDepositAndSwap2
  - 函数: depositAndSwap
  - 关键操作: token.safeTransferFrom(msg.sender, address(this), amount)
- **事件**: TokenRedeem3
  - 函数: redeem
  - 关键操作: token.burnFrom(msg.sender, amount)
- **事件**: TokenRedeemAndSwap4
  - 函数: redeemAndSwap
  - 关键操作: token.burnFrom(msg.sender, amount)
- **事件**: TokenRedeemAndRemove5
  - 函数: redeemAndRemove
  - 关键操作: token.burnFrom(msg.sender, amount)
### rel_chain: relay_chain
- **事件**: mint
  - 函数: mint
  - 关键操作: fees[address(token)] = fees[address(token)].add(fee), token.mint(address(this), amount), IERC20(token).safeTransfer(to, amount.sub(fee))
- **事件**: withdraw
  - 函数: withdraw
  - 关键操作: kappaMap[kappa] = true, fees[address(token)] = fees[address(token)].add(fee), token.safeTransfer(to, amount.sub(fee))
- **事件**: mintAndSwap
  - 函数: mintAndSwap
  - 关键操作: fees[address(token)] = fees[address(token)].add(fee), token.mint(address(this), amount), token.safeIncreaseAllowance(address(pool), amount), ISwap(pool).swap(tokenIndexFrom, tokenIndexTo, amount.sub(fee), minDy, deadline), swappedTokenTo.safeTransfer(to, finalSwappedAmount), IERC20(token).safeTransfer(to, amount.sub(fee))
- **事件**: withdrawAndRemove
  - 函数: withdrawAndRemove
  - 关键操作: kappaMap[kappa] = true, fees[address(token)] = fees[address(token)].add(fee), token.safeIncreaseAllowance(address(pool), amount.sub(fee)), ISwap(pool).removeLiquidityOneToken(amount.sub(fee), swapTokenIndex, swapMinAmount, swapDeadline), swappedTokenTo.safeTransfer(to, finalSwappedAmount), token.safeTransfer(to, amount.sub(fee))
### det_chain: destination_chain
- **事件**: TokenWithdraw1
  - 函数: withdraw
  - 关键操作: require(hasRole(NODEGROUP_ROLE, msg.sender), 'Caller is not a node group'), require(amount > fee, 'Amount must be greater than fee'), require(!kappaMap[kappa], 'Kappa is already present')
- **事件**: TokenMintAndSwap2
  - 函数: mintAndSwap
  - 关键操作: require(hasRole(NODEGROUP_ROLE, msg.sender), 'Caller is not a node group'), require(amount > fee, 'Amount must be greater than fee'), require(!kappaMap[kappa], 'Kappa is already present')
- **事件**: TokenMint3
  - 函数: mint
  - 关键操作: require(hasRole(NODEGROUP_ROLE, msg.sender), 'Caller is not a node group'), require(amount > fee, 'Amount must be greater than fee'), require(!kappaMap[kappa], 'Kappa is already present')
- **事件**: TokenMintAndSwap4
  - 函数: mintAndSwap
  - 关键操作: require(hasRole(NODEGROUP_ROLE, msg.sender), 'Caller is not a node group'), require(amount > fee, 'Amount must be greater than fee'), require(!kappaMap[kappa], 'Kappa is already present')
- **事件**: TokenWithdrawAndRemove5
  - 函数: withdrawAndRemove
  - 关键操作: require(hasRole(NODEGROUP_ROLE, msg.sender), 'Caller is not a node group'), require(amount > fee, 'Amount must be greater than fee'), require(!kappaMap[kappa], 'Kappa is already present')
---
