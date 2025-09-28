# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: NewExpatriation1, NewExpatriation2
- **rel_chain**: NewClaim, NewChallenge, FinishedClaim
- **det_chain**: NewRepatriation1, NewRepatriation2
### src_chain: Export
- **事件**: NewExpatriation1
  - 函数: transferToForeignChain
  - 关键操作: receiveStakeAsset(amount), emit NewExpatriation(msg.sender, amount, reward, foreign_address, data)
- **事件**: NewExpatriation2
  - 函数: claim
  - 关键操作: receiveMoneyInClaim(stake, paid_amount), Export(bridgeAddress).claim{value: tokenAddress == address(0) ? total : 0}(txid, txts, amount, reward, required_stake, sender_address, recipient_address, data)
### rel_chain: Counterstake
- **事件**: NewClaim
  - 函数: claim
  - 关键操作: require(req.amount > 0, "0 claim"), require(req.stake >= req.required_stake, "the stake is too small"), require(block.timestamp >= req.txts + settings.min_tx_age, "too early"), emit NewClaim(...)
- **事件**: NewChallenge
  - 函数: challenge
  - 关键操作: require(block.timestamp < c.expiry_ts, "the challenging period has expired"), require(stake_on != c.current_outcome, "this outcome is already current"), emit NewChallenge(...)
- **事件**: FinishedClaim
  - 函数: finish
  - 关键操作: require(block.timestamp > c.expiry_ts, "challenging period is still ongoing"), emit FinishedClaim(...)
### det_chain: Import
- **事件**: NewRepatriation1
  - 函数: transferToHomeChain
  - 关键操作: _burn(msg.sender, amount), emit NewRepatriation(msg.sender, amount, reward, home_address, data)
- **事件**: NewRepatriation2
  - 函数: onReceivedFromClaim
  - 关键操作: _mint(to_address, paid_claimed_amount), require(IERC20(settings.tokenAddress).transfer(to_address, won_stake), "failed to send the won stake")
---
