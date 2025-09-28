# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TokenDeposit1
- **rel_chain**: mint
- **det_chain**: TokenWithdraw1
### src_chain: source_chain
- **事件**: TokenDeposit1
  - 函数: stake
  - 关键操作: require(amount > 0, "Cannot stake 0"), _totalSupply = _totalSupply.add(amount), _balances[msg.sender] = _balances[msg.sender].add(amount), stakeToken.safeTransferFrom(msg.sender, address(this), amount)
### rel_chain: relay_chain
- **事件**: mint
  - 函数: notifyRewardAmount
  - 关键操作: if (block.timestamp >= periodFinish) { rewardRate = reward.div(DURATION); }, else { uint256 remaining = periodFinish.sub(block.timestamp); uint256 leftover = remaining.mul(rewardRate); rewardRate = reward.add(leftover).div(DURATION); }, lastUpdateTime = block.timestamp, periodFinish = block.timestamp.add(DURATION)
### det_chain: destination_chain
- **事件**: TokenWithdraw1
  - 函数: unstake
  - 关键操作: require(amount > 0, "Cannot withdraw 0"), _totalSupply = _totalSupply.sub(amount), _balances[msg.sender] = _balances[msg.sender].sub(amount), stakeToken.safeTransfer(msg.sender, amount)
---
