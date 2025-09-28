# 跨链桥合约分析报告
## 跨链桥: SolarBeam Bridge
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenRedeem2
- **rel_chain**: mint, withdraw
- **det_chain**: TokenWithdraw1, TokenMint2
### src_chain: Ethereum
- **事件**: TokenDeposit1
  - 函数: depositPool
  - 关键操作: require(_pid < numberPools, "pool does not exist");, require(poolInfo[_pid].offeringAmount > 0 && poolInfo[_pid].raisingAmount > 0, "Pool not set");, for (uint8 i=0; i<numberPools; i++) { if (i != _pid) { require(userInfo[msg.sender][i].amount == 0, "already commited in another pool"); } }, lpToken.safeTransferFrom(address(msg.sender), address(this), _amount);, user.amount += _amount;, if (poolInfo[_pid].baseLimitInLP == 0) { ... } else { ... }, poolInfo[_pid].totalAmountPool += _amount;
- **事件**: TokenRedeem2
  - 函数: harvestPool
  - 关键操作: require(_pid < numberPools, "pool does not exist");, require(_harvestPeriod < HARVEST_PERIODS, "harvest period out of range");, require(block.number > harvestReleaseBlocks[_harvestPeriod], "not harvest time");, require(userInfo[msg.sender][_pid].amount > 0, "did not participate");, require(!userInfo[msg.sender][_pid].claimed[_harvestPeriod], "harvest for period already claimed");, userInfo[msg.sender][_pid].claimed[_harvestPeriod] = true;, if (userTaxOverflow > 0 && !userInfo[msg.sender][_pid].isRefunded) { ... }, if (refundingTokenAmount > 0 && !userInfo[msg.sender][_pid].isRefunded) { ... }, offeringToken.safeTransfer(address(msg.sender), offeringTokenAmountPerPeriod);
### rel_chain: Solana
- **事件**: mint
  - 函数: mint
  - 关键操作: require(_value > 0, "deposit: invalid amount");, require(locked[_addr].amount > 0, "deposit: no lock for this address");, IBoringERC20(lockedToken).permit(_msgSender(), address(this), _value, deadline, v, r, s);, require(_value >= minLockedAmount, "create: less than min amount");, require(_days >= MINDAYS, "create: less than min amount of 7 days");, require(_days <= MAXDAYS, "create: voting lock can be 4 years max");
- **事件**: withdraw
  - 函数: withdraw
  - 关键操作: require(_locked.amount > 0, "withdraw: nothing to withdraw");, require(_now >= _locked.end, "withdraw: user still locked");, IBoringERC20(lockedToken).safeTransfer(_msgSender(), _amount);
### det_chain: BSC
- **事件**: TokenWithdraw1
  - 函数: withdrawPool
  - 关键操作: require(_pid < 2, "invalid pid");, require(!userInfo[msg.sender][_pid].claimed[_harvestPeriod], "harvest for period already claimed");, lpToken.safeTransfer(address(msg.sender), _amount);
- **事件**: TokenMint2
  - 函数: harvestPool
  - 关键操作: require(_pid < 2, "invalid pid");, require(block.timestamp > eclipseV2.harvestReleaseTimestamps(_harvestPeriod), "not harvest time");, require(!userInfo[msg.sender][_pid].claimed[_harvestPeriod], "harvest for period already claimed");, offeringToken.safeTransfer(address(msg.sender), offeringTokenAmountPerPeriod);
---
